"""The 36-criterion table for one claim, in the one format the supplement uses.

There were two formats before this: the hand-written IOI and SAE tables, which carry
validity-group divider rows and a totals line, and whatever got written by hand afterwards,
which did not. This generator is the single source, so a new claim cannot drift.

Rows come from data/criteria/<claim>.csv. Order is canonical regardless of the order the
CSV happens to be in, so a misplaced row is corrected rather than propagated.

Usage:  python make_criterion_table.py grokking
        python make_criterion_table.py --all
"""
import pathlib
from collections import Counter

import re

from mechval.audit import Audit
from mechval.paths import AUDITS, GENERATED, audit_file, claims


GREEK = {c: f"${{\\{n}}}$" for c, n in zip(
    "\u03b1\u03b2\u03b3\u03b4\u03b5\u03b6\u03b7\u03b8\u03ba\u03bb\u03bc\u03bd\u03c0\u03c1\u03c3\u03c4\u03c6\u03c7\u03c8\u03c9\u0393\u0394\u0398\u039b\u03a0\u03a3\u03a6\u03a8\u03a9",
    ["alpha","beta","gamma","delta","epsilon","zeta","eta","theta","kappa","lambda",
     "mu","nu","pi","rho","sigma","tau","phi","chi","psi","omega",
     "Gamma","Delta","Theta","Lambda","Pi","Sigma","Phi","Psi","Omega"])}


def tex(s: str) -> str:
    """Escape the characters that silently break a table row.

    A bare % comments out the rest of the line, so the row loses its \\ and merges with
    the next one --- which surfaces as "Extra alignment tab", far from the cause. Escape
    only %, & and #, and only when not already escaped: the short lines legitimately
    contain LaTeX ($\\alpha=0$, \\emph{}) that blanket escaping would destroy.
    """
    s = re.sub(r"(?<!\\)([%&#])", r"\\\1", s)
    return re.sub(r"[\u0370-\u03ff]", lambda m: GREEK.get(m.group(), m.group()), s)

GROUPS = [("Construct Validity", ["C%d" % i for i in range(1, 7)]),
          ("Measurement Validity", ["M%d" % i for i in range(1, 8)]),
          ("Internal Validity", ["I%d" % i for i in range(1, 13)]),
          ("External Validity", ["E%d" % i for i in range(1, 7)]),
          ("Interpretive Validity", ["V%d" % i for i in range(1, 6)])]
ORDER = [c for _, ids in GROUPS for c in ids]
NAMES = {"C": "Confirmed", "PC": "Partially confirmed", "I": "Inconclusive",
         "U": "Untested", "D": "Disconfirmed", "N/A": "Not applicable"}
TITLE = {"ioi": "the IOI circuit", "sae": "the SAE feature claim",
         "grokking": "Fourier multiplication in modular addition",
         "induction": "induction heads as in-context token copying",
         "workspace": "the global workspace / J-space claim",
         "greater_than": "the greater-than circuit",
         "copy_suppression": "copy suppression in negative attention heads",
         "superposition": "superposition in toy models",
         "refusal": "the refusal direction",
         "probing": "probing classifiers as mechanistic evidence",
         "knowledge_neurons": "the knowledge neuron claim",
         "induction_broad": "induction heads as the source of general in-context learning",
         "othello": "the Othello world-model claim",
         "successor_heads": "successor heads as ordinal incrementation",
         "docstring": "the Python docstring circuit",
         "gender": "the gender bias mediation claim"}
# Verdicts predate the verdict field in the audit record and are kept only for the five
# claims whose captions were written by hand; anything else reads its own record, so the
# verdict has one source.
VERDICT = {"ioi": "Causally Suggestive", "sae": "Causally Suggestive",
           "grokking": "Triangulated", "induction": "Triangulated",
           "workspace": "Mechanistically Supported"}


def _evidence_cell(crit, cap=130):
    """The one-line Evidence cell.

    `short` is hand-written and is used verbatim when present. Seven claims have
    none, and a blank cell reads as "no evidence" when the record in fact holds a
    full justification. So fall back to the first sentence of `reasoning`, marked
    with a trailing ellipsis when it is cut, and keep it short enough that the
    scorecard still fits a page. These fallbacks are derived, not authored: they
    should be replaced by a written `short` before the paper is final.
    """
    if (crit.short or "").strip():
        return crit.short
    text = (getattr(crit, "reasoning", "") or "").strip()
    if not text:
        return ""
    first = text.split(". ")[0].rstrip(".")
    if len(first) <= cap:
        return first
    return first[:cap].rsplit(" ", 1)[0] + "\\ldots"


def load(claim):
    """Rows from the verified audit record, not the unverified CSV.

    data/audits/<claim>.yaml is the single source: statuses resolved from the archive,
    evidence anchored to quotes that verify_quotes can re-check. The CSV it replaced
    carried a paraphrase with nothing behind it.
    """
    a = Audit.load(claim)
    return {c: {"criterion": a.criteria[c].name,
                "status": a.criteria[c].status.value,
                "evidence": tex(_evidence_cell(a.criteria[c])),
                "verified": a.criteria[c].verified} for c in ORDER}


def table(claim, rows):
    verdict = VERDICT.get(claim) or Audit.load(claim).verdict
    body = []
    for group, ids in GROUPS:
        body.append("\\midrule")
        body.append("\\multicolumn{4}{@{}l}{\\textit{%s}} \\\\" % group)
        for cid in ids:
            r = rows[cid]
            body.append(f"{cid:<4}& {r['criterion']:<26}& {r['status']:<4}& "
                        f"{r['evidence']} \\\\")
    cnt = Counter(r["status"].strip() for r in rows.values())
    tot = ", ".join(f"{cnt[k]} {NAMES[k]}" for k in
                    ["C", "PC", "I", "U", "D", "N/A"] if cnt[k])
    return f"""\\clearpage
\\vspace*{{-1.5em}}
{{\\footnotesize
\\renewcommand{{\\arraystretch}}{{1.0}}
\\begin{{longtable}}{{@{{}}llll>{{\\raggedright\\arraybackslash}}p{{6.5cm}}@{{}}}}
\\caption{{Full 36-criterion audit of {TITLE[claim]}. Status: \\textbf{{C}} = Confirmed,
\\textbf{{PC}} = Partially confirmed, \\textbf{{U}} = Untested, \\textbf{{I}} = Inconclusive,
\\textbf{{D}} = Disconfirmed, \\textbf{{N/A}} = Not applicable.}}\\\\
\\toprule
\\textbf{{ID}} & \\textbf{{Criterion}} & \\textbf{{Status}} & \\textbf{{Evidence}} \\\\
\\endfirsthead
\\toprule
\\textbf{{ID}} & \\textbf{{Criterion}} & \\textbf{{Status}} & \\textbf{{Evidence}} \\\\
\\endhead
{chr(10).join(body)}
\\midrule
\\multicolumn{{4}}{{@{{}}l}}{{\\textbf{{Total:}} {tot}}} \\\\
\\multicolumn{{4}}{{@{{}}l}}{{\\textbf{{Verdict: {verdict}}}}} \\\\
\\bottomrule
\\end{{longtable}}}}
"""


def write(claim: str) -> pathlib.Path:
    """The 36-criterion table for one claim."""
    rows = load(claim)
    out = GENERATED / f"{claim}_criterion_table.tex"
    GENERATED.mkdir(parents=True, exist_ok=True)
    out.write_text(table(claim, rows))
    return out
