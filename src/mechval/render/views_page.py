"""Views audit page for one claim, derived from its ACH matrix.

The matrix lives in data/audits/<claim>.yaml and is never surfaced in the paper. It is the
checkable source: one row per measurement, one column per rival hypothesis, cells C, I or
a dash. What the paper shows is this page, where each hypothesis carries the criteria it
established and the criteria that disconfirmed it.

Scoring is imported from score_hypotheses rather than repeated here. It was repeated here
once, and the copy kept the rule that a criterion tested by two rows takes the worse of
them --- so IOI's H1 was disconfirmed at M2 by the naive-circuit row while the copy-score
row confirming it was thrown away, and this page called the paper's own hypothesis
Excluded where its full audit says Causally Suggestive. Evidence pointing both ways is
Inconclusive, and keeping one implementation of that rule is the only way it stays one
rule.

Usage:  python make_views_page.py ioi
"""
import pathlib

from mechval.audit import Audit
from mechval.score import REQUIRED, score_rivals as score
from mechval.paths import AUDITS, GENERATED, audit_file, claims

ORDER = (["C%d" % i for i in range(1, 6)] + ["M%d" % i for i in range(1, 8)]
         + ["I%d" % i for i in range(1, 13)] + ["E%d" % i for i in range(1, 7)]
         + ["V%d" % i for i in range(1, 6)])


def read(claim):
    """From the audit record, not the CSV.

    The CSVs had no schema, and one of them carried an unquoted comma that shifted every
    field on a row by one column --- silently rendering a wrong table for weeks. The YAML
    is checked by the Pydantic models, which reject a cell naming an unknown hypothesis
    or a row missing one.
    """
    return Audit.load(claim)


def standing(st, n_rows, origin=False, audit_verdict=""):
    """Standing reflects what was established, not merely what escaped contradiction.

    An inconsistency count alone rewards a hypothesis nobody aimed at: it accumulates no
    contradictions and can finish first. Confirmed is the corrective --- it is awarded only
    where a measurement was designed for that hypothesis --- so a rival that survives
    without ever being tested reads Untouched rather than Live.

    Standing, not tier. MechVal tiers require specific criteria --- I1 and M2 for Causally
    Suggestive, I2/E1/I4 for Mechanistically Supported --- and an ACH matrix scores a
    handful of criteria rather than all 35, so a tier cannot be read off it.

    The origin hypothesis is the exception. It is the one the paper itself advanced, and it
    alone carries a full 35-criterion audit, which a subset of the same evidence cannot
    overturn. Where that audit places the claim above Disconfirmed, the page reads
    Contradicted repeatedly rather than Excluded.
    """
    d = [k for k, v in st.items() if v == "D"]
    c = sum(1 for v in st.values() if v == "C")
    if not d:
        if c == 0:
            # Every row pointed both ways. Tested is not the same as untouched.
            return "Tested, evidence mixed" if any(v == "I" for v in st.values()) else "Untouched"
        return "Live; nothing contradicts it" if c >= 3 else "Consistent, lightly tested"
    if c > len(d) or len(d) == 1:
        return "Weakened"                       # established more than it lost
    if len(d) >= n_rows * 0.5 and any(k in REQUIRED for k in d):
        if not (origin and audit_verdict != "Disconfirmed"):
            return "Excluded"
    return "Contradicted repeatedly"


def table(claim, a, per, caption):
    body, prev = [], None
    n_rows = len(a.views_evidence)
    for i, h in enumerate(a.hypotheses):
        st = per[h.id]
        est = ", ".join(c for c in ORDER if st.get(c) in ("C", "PC")) or "---"
        dis = ", ".join(c for c in ORDER if st.get(c) == "D") or "---"
        if prev and h.view != prev:
            body.append("\\addlinespace[2pt]")
        prev = h.view
        s = standing(st, n_rows, origin=(i == 0), audit_verdict=a.verdict)
        body.append(f"{h.view} & {h.label} & {est} & {dis} & {s} \\\\")
    return f"""\\begin{{table}}[H]
\\centering\\footnotesize
\\caption{{{caption}}}
\\label{{tab:{claim}-views}}
\\medskip
\\renewcommand{{\\arraystretch}}{{1.2}}\\setlength{{\\tabcolsep}}{{4pt}}
\\begin{{tabular}}{{@{{}}l>{{\\raggedright\\arraybackslash}}p{{3.7cm}}>{{\\raggedright\\arraybackslash}}p{{3.5cm}}>{{\\raggedright\\arraybackslash}}p{{2.3cm}}l@{{}}}}
\\toprule
\\textbf{{View}} & \\textbf{{Hypothesis}} & \\textbf{{Established}} & \\textbf{{Disconfirmed}} & \\textbf{{Standing}} \\\\
\\midrule
{chr(10).join(body)}
\\bottomrule
\\end{{tabular}}
\\end{{table}}
"""


def write(claim: str) -> pathlib.Path | None:
    """The rival-hypothesis standing table. None when a claim names no rivals."""
    a = read(claim)
    if not a.hypotheses or not a.views_evidence:
        return None
    per = score(a)
    cap = (f"Standing of {len(a.hypotheses)} rival hypotheses on the published evidence. "
           "The Established and Disconfirmed columns name the criteria themselves rather "
           "than counting them, so every verdict can be traced to the measurements that "
           "produced it.")
    out = GENERATED / f"{claim}_views_table.tex"
    GENERATED.mkdir(parents=True, exist_ok=True)
    out.write_text(table(claim, a, per, cap))
    return out
