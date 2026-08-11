"""Typed schema for audit records, with quote anchoring that can be mechanically checked.

Quotes are anchored the way the W3C Web Annotation Data Model anchors them: a
TextQuoteSelector, meaning `exact` plus enough `prefix` and `suffix` to disambiguate.
Character and line offsets are recorded as well, but they are advisory --- offsets move
when the extraction tool changes and the selector does not.

The point of the types is that an unsupported status cannot be written down accidentally.
A criterion may not be `verified` without quotes, a quote may not be empty, and a `short`
line long enough to be prose is rejected because the supplement layout depends on it
being about sixty characters.

    from audit_schema import Audit
    audit = Audit.from_yaml(path)          # raises on any violation
    audit.unsupported()                    # criteria asserting a status with no quote
"""
from __future__ import annotations

import hashlib
import unicodedata
import pathlib
import re
import subprocess
from enum import Enum
from typing import Literal

import yaml
from mechval.paths import PROJECT_ROOT, audit_file, claim_file
from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator

ORDER = (["C%d" % i for i in range(1, 6)] + ["M%d" % i for i in range(1, 8)]
         + ["I%d" % i for i in range(1, 13)] + ["E%d" % i for i in range(1, 7)]
         + ["V%d" % i for i in range(1, 6)])
SHORT_MAX = 90          # the two-page layout breaks above this; see SUPPLEMENT_FORMAT_SPEC
CACHE = pathlib.Path("/tmp/mechval_extracts")


def fold(s: str) -> str:
    """Normalise away the differences PDF extraction invents.

    A quote and its source disagree on things no reader would call a difference:
    combining diacritics (naive), smart quotes, the Unicode minus, spaces LaTeX puts
    inside math delimiters, and hyphenation across a line break. Folding these is what
    lets the gate fail on fabrication rather than on typography.
    """
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    for a, b in (("\u2018", "'"), ("\u2019", "'"), ("\u201c", '"'), ("\u201d", '"'),
                 ("\u2212", "-"), ("\u2013", "-"), ("\u2014", "-"), ("\u00a0", " "),
                 ("\u0131", "i"), ("\ufb01", "fi"), ("\ufb02", "fl"), ("_", "")):
        s = s.replace(a, b)   # dotless i survives NFKD; subscripts extract inconsistently
    s = re.sub(r"-", "", s)                 # hyphens break across lines unpredictably
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*([(){}\[\]|])\s*", r"\1", s)   # LaTeX pads math delimiters
    return s.strip().lower()


def skeleton(s: str) -> str:
    """Letters and digits only.

    A last resort. -layout hyphenates across line breaks, pads inline math, and drops
    subscripts to the baseline; none of those change what the paper says. Matching on the
    alphanumeric skeleton removes all of them at once, at the cost of no longer
    distinguishing operators --- ``a - b`` and ``a + b`` fold together. A match found only
    at this level is reported as loose so it is never mistaken for an exact one.
    """
    return re.sub(r"[^0-9a-z]", "", fold(s))


class Status(str, Enum):
    confirmed = "C"
    partial = "PC"
    inconclusive = "I"
    untested = "U"
    disconfirmed = "D"
    not_applicable = "N/A"


class Source(BaseModel):
    """A source pinned hard enough that a locator means something."""
    citation: str
    title: str = ""
    url: str | None = None
    local: str | None = None
    sha256: str | None = None
    extract_cmd: str = "pdftotext -layout"
    read_in_full: bool = False

    @model_validator(mode="after")
    def _checksum_requires_file(self):
        if self.sha256 and not self.local:
            raise ValueError("sha256 given with no local file to check it against")
        return self

    def text(self, root: pathlib.Path | None = None) -> str:
        """Extraction under the pinned command, checksum enforced."""
        root = root or PROJECT_ROOT
        if not self.local:
            raise ValueError(f"{self.citation}: no local source")
        pdf = root / self.local
        if self.sha256:
            got = hashlib.sha256(pdf.read_bytes()).hexdigest()
            if got != self.sha256:
                raise ValueError(f"{self.citation}: source changed "
                                 f"({self.sha256[:12]} -> {got[:12]})")
        if pdf.suffix == ".txt":
            return pdf.read_text(errors="replace")
        CACHE.mkdir(exist_ok=True)
        out = CACHE / (hashlib.sha256(str(pdf).encode()).hexdigest()[:16] + ".txt")
        if not out.exists():
            subprocess.run(self.extract_cmd.split() + [str(pdf), str(out)],
                           check=True, capture_output=True)
        return out.read_text(errors="replace")


class Quote(BaseModel):
    """A W3C TextQuoteSelector, plus advisory offsets."""
    exact: str = Field(min_length=12)
    prefix: str = ""
    suffix: str = ""
    section: str | None = None          # human locator: "§4.3", "Figure 6"
    page: int | None = None
    line: int | None = None             # valid only under Source.extract_cmd

    # No elision check. An ellipsis may be the authors' own notation --- Wang et al.
    # write the induction pattern as "[A] [B] ... [A]" --- and elision by the quoter is
    # already caught by resolve(), since elided text will not match the source.

    @model_validator(mode="after")
    def _has_a_locator(self):
        if self.section is None and self.page is None and self.line is None:
            raise ValueError("a quote needs at least one of section, page or line")
        return self

    def resolve(self, text: str) -> Literal["ok", "loose", "not found", "ambiguous"]:
        """Exact first, then the alphanumeric skeleton, so a loose match stays visible."""
        flat = fold(text)
        n = flat.count(fold(self.exact))
        if n == 1:
            return "ok"
        if n > 1:
            anchor = fold(self.prefix + self.exact + self.suffix)
            return "ok" if flat.count(anchor) == 1 else "ambiguous"
        bones = skeleton(text)
        k = bones.count(skeleton(self.exact))
        if k == 1:
            return "loose"
        if k > 1:
            return "ambiguous"
        return "not found"


class Ref(BaseModel):
    """Post-origin work bearing on a criterion, pinned so the gate can resolve it.

    This previously carried a citation and a loose `text` with no pointer to a document,
    so `check_quotes` had nothing to resolve refs against and never looked at them. The
    gate then reported zero failures because it examined zero items -- which is the same
    failure shape it exists to catch.

    `local` and `sha256` mirror `Source`. A ref without them resolves to "unpinned", which
    the gate reports rather than passes.
    """
    citation: str
    text: str = ""
    section: str | None = None
    page: int | None = None
    direction: Literal["raises", "lowers", "neutral"] = "neutral"
    local: str | None = None
    sha256: str | None = None
    extract_cmd: str = "pdftotext -layout"

    def as_source(self) -> "Source | None":
        if not self.local:
            return None
        return Source(citation=self.citation, local=self.local, sha256=self.sha256,
                      extract_cmd=self.extract_cmd)

    def resolve(self, root: pathlib.Path) -> str:
        """ok | loose | not found | ambiguous | unpinned | no text | missing source.

        A ref that will not resolve is repaired by splitting into adjacent fragments that
        reassemble the original, never by truncating to the longest matching prefix. A
        fragment ending in a dangling opener -- "(Figure", "(Appendix" -- is a truncation
        wearing a boundary's clothes, and the two repaired here both looked like clean
        splits until the text was read back.
        """
        if not self.local:
            return "unpinned"
        if len(self.text.strip()) < 12:
            return "no text"
        src = self.as_source()
        try:
            body = src.text(root)
        except Exception:                                          # noqa: BLE001
            return "missing source"
        return Quote(exact=self.text, section=self.section or "-").resolve(body)


class Reading(BaseModel):
    """One version of the claim, from the authors' statement to the field's citation.

    The readings table is where the strong and weak versions of a claim are separated,
    which is what lets one paper carry two verdicts. It was hand-written LaTeX until now,
    so nothing checked it --- four tables shipped with an unfilled [derive] placeholder.
    """
    statement: str = Field(min_length=10)
    verdict: str                      # a tier name, or Underdetermined/Insufficient/Disconfirmed
    missing: str = ""
    primary: bool = False

    @field_validator("verdict")
    @classmethod
    def _is_a_real_verdict(cls, v: str) -> str:
        ok = {"Proposed", "Causally Suggestive", "Mechanistically Supported",
              "Mech.\\ Supported", "Triangulated", "Validated",
              "Underdetermined", "Insufficient", "Disconfirmed"}
        if v not in ok:
            raise ValueError(f"{v!r} is not a verdict; placeholders like [derive] are rejected")
        return v


class Tier(BaseModel):
    """One rung of the ladder, and what blocks promotion past it."""
    name: Literal["Proposed", "Causally Suggestive", "Mechanistically Supported",
                  "Triangulated", "Validated"]
    requires: str
    missing: str = "---"


class Criterion(BaseModel):
    name: str
    status: Status
    short: str = ""
    verified: bool = False
    quotes: list[Quote] = []
    reasoning: str = ""
    refs: list[Ref] = []
    notes: dict[str, str] = {}

    @field_validator("short")
    @classmethod
    def _short_is_short(cls, v: str) -> str:
        if len(v) > SHORT_MAX:
            raise ValueError(f"short is {len(v)} chars, over the {SHORT_MAX} the "
                             f"two-page layout allows")
        return v

    @model_validator(mode="after")
    def _verified_needs_quotes(self):
        if self.verified and not self.quotes:
            raise ValueError("verified with no quotes; that is an assertion, not an audit")
        if self.verified and not self.reasoning.strip():
            raise ValueError("verified with no reasoning linking quotes to status")
        return self


class Hypothesis(BaseModel):
    """One rival account of the same phenomenon, stated within a single view."""
    id: str = Field(pattern=r"^H\d+$")
    view: str                          # Object, Role, Instrumental, Contrastive, ...
    label: str = Field(min_length=8)   # written out; no codes in the rendered prose


class ViewsEvidence(BaseModel):
    """One measurement, scored against every rival it bears on.

    `cells` maps a hypothesis id to C (consistent), I (inconsistent) or - (does not bear).
    `designed_for` names the hypotheses the measurement was built to test, which is what
    licenses Confirmed over Partially confirmed when the page is scored.
    """
    criterion: str = Field(pattern=r"^[CMIEV]\d+$")
    evidence: str = Field(min_length=15)
    cells: dict[str, Literal["C", "I", "-"]]
    designed_for: list[str] = []


class QuoteFailure(BaseModel):
    """One quote that did not resolve in its source."""
    criterion: str
    index: int
    reason: Literal["not found", "ambiguous", "no text", "missing source"]
    excerpt: str


class QuoteCheck(BaseModel):
    """What resolving one audit's quotes and refs returned.

    Refs are counted separately from quotes because they resolve against a different
    document -- post-origin work rather than the origin paper -- and because an unpinned
    ref is a distinct condition from a quote that does not match. Both are reported; a
    check that silently skipped unpinned refs would pass by examining nothing.
    """
    claim: str
    exact: int = 0
    loose: int = 0
    failures: list[QuoteFailure] = []
    ref_exact: int = 0
    ref_loose: int = 0
    ref_unpinned: int = 0
    ref_failures: list[QuoteFailure] = []

    @property
    def total(self) -> int:
        return self.exact + self.loose + len(self.failures)

    @property
    def refs_total(self) -> int:
        return self.ref_exact + self.ref_loose + self.ref_unpinned + len(self.ref_failures)

    @property
    def passed(self) -> bool:
        """Unpinned refs do not fail the gate yet; they are reported so the number is visible.

        Flip this to include `self.ref_unpinned` once the refs have been anchored, which is
        what turns the reporting into a gate.
        """
        return not self.failures and not self.ref_failures


class Audit(BaseModel):
    claim: str
    title: str = ""
    verdict: str = ""
    description: str = ""
    source: Source
    readings: list[Reading] = []
    hypotheses: list[Hypothesis] = []
    views_evidence: list[ViewsEvidence] = []
    tiers: list[Tier] = []
    criteria: dict[str, Criterion]

    @model_validator(mode="after")
    def _views_are_consistent(self):
        ids = {h.id for h in self.hypotheses}
        for e in self.views_evidence:
            unknown = set(e.cells) - ids
            if unknown:
                raise ValueError(f"{e.criterion}: cells name unknown hypotheses {unknown}")
            missing = ids - set(e.cells)
            if missing:
                raise ValueError(f"{e.criterion}: no cell for {missing}")
            bad = [d for d in e.designed_for if d not in ids]
            if bad:
                raise ValueError(f"{e.criterion}: designed_for names unknown {bad}")
        return self

    @model_validator(mode="after")
    def _one_primary_reading(self):
        if self.readings and sum(1 for r in self.readings if r.primary) != 1:
            raise ValueError("exactly one reading must be marked primary")
        return self

    @field_validator("criteria")
    @classmethod
    def _all_thirty_five(cls, v: dict[str, Criterion]) -> dict[str, Criterion]:
        missing = [c for c in ORDER if c not in v]
        unknown = [c for c in v if c not in ORDER]
        if missing:
            raise ValueError(f"missing criteria: {missing}")
        if unknown:
            raise ValueError(f"unknown criteria: {unknown}")
        return v

    @classmethod
    def load(cls, claim: str) -> "Audit":
        """Join the two halves of a record by claim name.

        What a paper says lives in `claims/`: the claim as stated, the pinned source, and every
        verbatim quotation with its section and page. What we concluded lives in `audits/`:
        statuses, verdicts, reasoning, rival hypotheses. The two are separate on disk because
        they have different standing --- the extraction is checkable by anyone holding the PDF
        and reusable by someone who rejects every verdict here, while the judgment is ours and
        contestable. Merging them in one file made that impossible to see, which is the exact
        conflation this project exists to argue against.

        They are rejoined here so callers keep working against one object. `verified` is a
        claim we make about having checked, so it sits on the judgment side.
        """
        judgment = yaml.safe_load(audit_file(claim).read_text()) or {}
        extraction = yaml.safe_load(claim_file(claim).read_text()) or {}
        merged = {**extraction, **judgment}
        merged.pop("evidence", None)
        crit = {cid: dict(c) for cid, c in (judgment.get("criteria") or {}).items()}
        for cid, ev in (extraction.get("evidence") or {}).items():
            if cid not in crit:
                raise ValueError(f"{claim}: claims/ carries evidence for {cid}, "
                                 f"which audits/ does not score")
            crit[cid].update(ev)
        merged["criteria"] = crit
        return cls.model_validate(merged)

    def save(self, claim: str | None = None) -> None:
        self.to_yaml(audit_file(claim or self.claim_id()))

    def claim_id(self) -> str:
        return self.source.citation.split("2")[0].rstrip("_")

    @classmethod
    def from_yaml(cls, path: pathlib.Path) -> "Audit":
        return cls.model_validate(yaml.safe_load(path.read_text()))

    def to_yaml(self, path: pathlib.Path) -> None:
        data = self.model_dump(mode="json", exclude_defaults=False)
        data["criteria"] = {c: data["criteria"][c] for c in ORDER}
        path.write_text(yaml.safe_dump(data, sort_keys=False, width=100,
                                       allow_unicode=True))

    def unsupported(self) -> list[str]:
        """Criteria asserting a status with nothing quoted behind it."""
        return [c for c in ORDER if not self.criteria[c].quotes]

    def check_quotes(self, root: pathlib.Path | None = None) -> "QuoteCheck":
        """Resolve every quote against the pinned extraction.

        Exact, loose and failing are counted separately. A loose match resolved only on the
        alphanumeric skeleton, which cannot tell `a - b` from `a + b`, so it is reported and
        not failed. An earlier version returned everything that was not exact and called it
        bad, which reported thirty failures for an audit that had none.
        """
        root = root or PROJECT_ROOT
        if not self.source.local:
            return QuoteCheck(claim=self.source.citation)
        text = self.source.text(root)
        exact = loose = 0
        failures: list[QuoteFailure] = []
        r_exact = r_loose = r_unpinned = 0
        r_failures: list[QuoteFailure] = []
        for cid in ORDER:
            c = self.criteria[cid]
            for k, q in enumerate(c.quotes):
                r = q.resolve(text)
                if r == "ok":
                    exact += 1
                elif r == "loose":
                    loose += 1
                else:
                    failures.append(QuoteFailure(criterion=cid, index=k, reason=r,
                                                 excerpt=q.exact[:80]))
            for k, ref in enumerate(c.refs):
                r = ref.resolve(root)
                if r == "ok":
                    r_exact += 1
                elif r == "loose":
                    r_loose += 1
                elif r == "unpinned":
                    r_unpinned += 1
                else:
                    r_failures.append(QuoteFailure(criterion=cid, index=k, reason=r,
                                                   excerpt=f"[{ref.citation}] {ref.text[:60]}"))
        return QuoteCheck(claim=self.source.citation, exact=exact, loose=loose,
                          failures=failures, ref_exact=r_exact, ref_loose=r_loose,
                          ref_unpinned=r_unpinned, ref_failures=r_failures)
