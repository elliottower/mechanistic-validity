"""Criteria to tier, for a claim and for each rival hypothesis it names.

One ladder, defined once. It was previously defined twice --- in `score_hypotheses.py` and
again in `score_rivals.py` --- and the two drifted, so a rival could be scored against
requirements the claim was not.

    mechval-score               # every claim and its rivals
    mechval-score ioi           # one
    mechval-score --rivals      # rival detail
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter

from pydantic import BaseModel

from mechval.audit import Audit
from mechval.paths import claims

# Each rung lists the criteria it requires. A tuple inside the list is a disjunction: E2 or
# E4 satisfies cross-distribution replication, depending on what the claim asserts.
LADDER: list[tuple[str, list[tuple[str, ...]]]] = [
    ("Proposed", [("C1",), ("C2",)]),
    ("Causally Suggestive", [("I1",), ("M2",)]),
    ("Mechanistically Supported", [("I2",), ("E1",), ("I4",)]),
    ("Triangulated", [("C3",), ("E2", "E4"), ("I6",)]),
    ("Validated", [("M1",), ("M2",), ("M3",), ("M4",), ("M5",), ("M6",),
                   ("V1",), ("V2",), ("V3",), ("V4",), ("V5",), ("E2",), ("E4",)]),
]

# C and PC both establish a criterion; PC means the measurement was not designed for this
# claim but is consistent with it.
ESTABLISHED = {"C", "PC"}

# The Validated rung asks a different question from the rungs below it. Its wording is
# "measurement calibration (M1--M6) explicitly addressed; interpretive validity (V1--V5)
# audited" -- addressed and audited, not established -- and the prose agrees: reaching it
# from Mechanistically Supported needs "no new experiments required, only systematic
# reporting". So a criterion at D or I has been addressed; only U and N/A have not. An
# earlier version required C or PC here, which was stricter than anything the paper says.
ADDRESSED_NOT_ESTABLISHED = {"Validated"}
UNADDRESSED = {"U", "N/A"}
EXCLUDED = {"N/A"}

# Three labels sit outside the hierarchy and replace the tier rather than accompanying it:
# too many explanations fit the claim, too little evidence exists to assess it, or it was
# tested and failed. A ladder walk cannot produce them -- they are judgments recorded in the
# audit -- so a record carrying one is not a disagreement with the computed tier.
REPLACEMENT_LABELS = {"Underdetermined", "Insufficient", "Disconfirmed"}

# Every criterion some rung below Validated requires. Derived from LADDER rather than
# restated, so it cannot drift from it. A disconfirmation here caps a claim; one at a
# criterion absent from this set damages it without blocking a tier.
REQUIRED: set[str] = {c for _, groups in LADDER[:4] for g in groups for c in g}


class TierResult(BaseModel):
    """Where a claim or hypothesis sits, and what stopped it going higher."""
    name: str
    tier: str
    blocked_by: list[str] = []
    counts: dict[str, int] = {}

    def line(self) -> str:
        blk = ("blocked at " + ", ".join(self.blocked_by)) if self.blocked_by else ""
        c = " ".join(f"{k}={v}" for k, v in sorted(self.counts.items()))
        return f"  {self.name:<22}{self.tier:<28}{c:<34}{blk}"


def tier_from_statuses(name: str, status: dict[str, str]) -> TierResult:
    """Walk the ladder, stopping at the first rung whose requirements are not met.

    A criterion excluded as N/A does not block: the framework treats a test the claim's
    structure cannot pose as information about the setting, not as a failure. A toy model
    trained on one task has no off-target behaviour, so specificity is unaskable there.
    """
    reached, blocked = "below Proposed", []
    for rung, groups in LADDER:
        bar = (lambda g: g not in UNADDRESSED) if rung in ADDRESSED_NOT_ESTABLISHED \
            else (lambda g: g in ESTABLISHED)
        missing = []
        for group in groups:
            got = [status.get(c, "U") for c in group]
            if all(g in EXCLUDED for g in got):
                continue
            if not any(bar(g) for g in got):
                missing.append("/".join(group) + "=" + ",".join(got))
        if missing:
            blocked = missing
            break
        reached = rung
    return TierResult(name=name, tier=reached, blocked_by=blocked,
                      counts=dict(Counter(status.values())))


def score_claim(a: Audit) -> TierResult:
    return tier_from_statuses(a.source.citation,
                              {c: v.status.value for c, v in a.criteria.items()})


def score_rivals(a: Audit) -> dict[str, dict[str, str]]:
    """Per rival hypothesis, the criteria its ACH row establishes or disconfirms.

    A cell marked C where the measurement was designed for that hypothesis establishes the
    criterion. A cell marked C where it was designed for something else is consistent only,
    which is PC. Rows pointing both ways give I, which the ladder does not accept -- an
    earlier version collapsed that to D and killed hypotheses on one adverse row.
    """
    seen: dict[str, dict[str, list[tuple[str, bool]]]] = {h.id: {} for h in a.hypotheses}
    for e in a.views_evidence:
        for hid, cell in e.cells.items():
            if cell == "-":
                continue
            seen[hid].setdefault(e.criterion, []).append((cell, hid in e.designed_for))
    out: dict[str, dict[str, str]] = {}
    for hid, crits in seen.items():
        out[hid] = {}
        for crit, rows in crits.items():
            against = any(c == "I" for c, _ in rows)
            for_ = [d for c, d in rows if c == "C"]
            if against and for_:
                out[hid][crit] = "I"
            elif against:
                out[hid][crit] = "D"
            elif any(for_):
                out[hid][crit] = "C"
            else:
                out[hid][crit] = "PC"
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("claims", nargs="*")
    ap.add_argument("--rivals", action="store_true", help="also score each rival hypothesis")
    args = ap.parse_args()

    for name in (args.claims or claims()):
        a = Audit.load(name)
        r = score_claim(a)
        if a.verdict in REPLACEMENT_LABELS:
            agrees = f"   [record: {a.verdict}, a label outside the ladder]"
        elif r.tier == a.verdict:
            agrees = ""
        else:
            agrees = f"   <-- DISAGREES: record says {a.verdict}"
        print(f"\n{name}{agrees}")
        print(r.line())
        if args.rivals:
            per = score_rivals(a)
            for h in a.hypotheses:
                hr = tier_from_statuses(f"{h.id} [{h.view}]", per[h.id])
                print(hr.line())
    return 0


if __name__ == "__main__":
    sys.exit(main())
