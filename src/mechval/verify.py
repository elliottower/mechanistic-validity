"""The gate: every claim backed by a quotation that resolves in its pinned source.

Three checks, in order. Schema first, because a record that will not load cannot be scored.
Then quote resolution against the source PDF. Then coverage, so a claim cannot pass by
having no criteria to fail.

This replaces two modules that did the same work twice --- `audit_check.py` for this repo
and `verify_claims.py` for anywhere else. One implementation, two entry points.

    mechval-verify                # every audit
    mechval-verify ioi sae        # named ones
    mechval-verify --strict       # exit 1 on any failure, for CI

What it catches is fabrication: quotations that do not exist, statuses unsupported by their
own source. What it cannot catch is misinterpretation --- a real, resolving quotation
attached to a claim it does not support. That distinction is why the audits also carry
`reasoning` and `readings`, which no gate can check.
"""
from __future__ import annotations

import argparse
import sys

from pydantic import BaseModel

from mechval.audit import ORDER, Audit, QuoteCheck
from mechval.paths import PROJECT_ROOT, claims


class ClaimReport(BaseModel):
    """One audit's standing across all three checks."""
    claim: str
    loaded: bool
    source_present: bool
    quotes: QuoteCheck | None = None
    criteria_verified: int = 0
    criteria_total: int = 0
    error: str | None = None

    @property
    def passed(self) -> bool:
        return (self.loaded and self.source_present
                and (self.quotes is None or self.quotes.passed))

    def line(self) -> str:
        if not self.loaded:
            return f"{self.claim:<20}{'LOAD FAILED':<12}{self.error}"
        q = self.quotes
        note = ""
        if q and q.loose:
            note = f"{q.loose} matched on the alphanumeric skeleton"
        if not self.source_present:
            note = "source missing"
        return (f"{self.claim:<20}{'yes' if self.source_present else 'NO':<8}"
                f"{self.criteria_verified:>4}/{self.criteria_total:<6}"
                f"{q.exact if q else 0:>6}{len(q.failures) if q else 0:>7}  {note}")


def check(claim: str) -> ClaimReport:
    try:
        a = Audit.load(claim)
    except Exception as e:                                        # noqa: BLE001
        return ClaimReport(claim=claim, loaded=False, source_present=False, error=str(e))

    present = bool(a.source.local) and (PROJECT_ROOT / a.source.local).exists()
    verified = sum(1 for c in ORDER if a.criteria[c].verified)
    if not present:
        return ClaimReport(claim=claim, loaded=True, source_present=False,
                           criteria_verified=verified, criteria_total=len(ORDER),
                           error=f"missing {a.source.local}")
    try:
        qc = a.check_quotes()
    except Exception as e:                                        # noqa: BLE001
        # A changed source raises here rather than resolving against the wrong text.
        return ClaimReport(claim=claim, loaded=True, source_present=True,
                           criteria_verified=verified, criteria_total=len(ORDER),
                           error=str(e))
    return ClaimReport(claim=claim, loaded=True, source_present=True, quotes=qc,
                       criteria_verified=verified, criteria_total=len(ORDER))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("claims", nargs="*", help="claim names; default is all")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any check fails")
    args = ap.parse_args()

    targets = args.claims or claims()
    print(f"{'claim':<20}{'source':<8}{'verified':>10}{'exact':>6}{'FAIL':>7}  notes")
    reports = [check(c) for c in targets]
    for r in reports:
        print(r.line())

    failing = [r for r in reports if not r.passed]
    n_bad = sum(len(r.quotes.failures) if r.quotes else 1 for r in failing)
    print(f"\n{n_bad} failing across {len(failing)} of {len(reports)} audits")
    if failing:
        for r in failing:
            for f in (r.quotes.failures if r.quotes else []):
                print(f"  {r.claim} {f.criterion}[{f.index}] {f.reason}: {f.excerpt}")
    return 1 if (args.strict and failing) else 0


if __name__ == "__main__":
    sys.exit(main())
