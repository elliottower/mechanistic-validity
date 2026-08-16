"""A whole claim section, generated from its audit record.

Everything the supplement renders for a claim now comes from data/audits/<claim>.yaml:
the description, the readings table, the tier ladder and the 36-criterion audit. The
readings and tier tables were hand-written LaTeX until now, which is how four of them
shipped carrying an unfilled [derive] placeholder -- nothing generated them, so nothing
checked them.

    python make_section.py grokking
    python make_section.py --all
"""
import pathlib
import re

from mechval.audit import Audit
from mechval.render.criterion_table import table as criterion_table, load, tex
from mechval.paths import AUDITS, GENERATED, audit_file, claims



def esc(s: str) -> str:
    return tex(s)


def section(claim: str) -> str:
    a = Audit.load(claim)
    reads = []
    for r in a.readings:
        stmt = ("\\textbf{Primary.} " if r.primary else "") + esc(r.statement)
        reads.append(f"{stmt}\n  & {r.verdict}\n  & {esc(r.missing)} \\\\")
    tiers = [f"{t.name} & {esc(t.requires)} & {esc(t.missing)} \\\\" for t in a.tiers]
    sep = "\n\\addlinespace[2pt]\n"
    source_title = ("\\emph{" + esc(a.source.title) + "} ") if a.source.title else ""
    return f"""\\claimheading{{{a.title}}}

\\textbf{{Source.}} {source_title}\\citep{{{a.source.citation}}}.

\\textbf{{Description.}} {esc(a.description)}

\\vspace{{4pt}}
{criterion_table(claim, load(claim)).rstrip().replace(chr(92)+"clearpage" + chr(10), "", 1).replace(chr(92)+"vspace*{-1.5em}" + chr(10), "", 1)}

\\clearpage
\\begin{{table}}[H]
\\centering
\\footnotesize
\\caption{{Readings of the claim, from the version the authors state to the version the
field cites.}}
\\label{{tab:{claim}-readings}}
\\renewcommand{{\\arraystretch}}{{1.18}}
\\begin{{tabular}}{{@{{}}>{{\\raggedright\\arraybackslash}}p{{3.9cm}}l>{{\\raggedright\\arraybackslash}}p{{6.0cm}}@{{}}}}
\\toprule
\\textbf{{Reading}} & \\textbf{{Verdict}} & \\textbf{{Missing}} \\\\
\\midrule
{sep.join(reads)}
\\bottomrule
\\end{{tabular}}
\\end{{table}}

\\begin{{table}}[H]
\\centering
\\footnotesize
\\caption{{Verdict: \\textbf{{{a.verdict}}}. A dash means the tier is reached; a criterion at
Inconclusive, Untested or Disconfirmed blocks promotion.}}
\\label{{tab:{claim}-verdict}}
\\renewcommand{{\\arraystretch}}{{1.18}}
\\begin{{tabular}}{{@{{}}l>{{\\raggedright\\arraybackslash}}p{{4.3cm}}>{{\\raggedright\\arraybackslash}}p{{6.0cm}}@{{}}}}
\\toprule
\\textbf{{Tier}} & \\textbf{{Requires}} & \\textbf{{Missing}} \\\\
\\midrule
{sep.join(tiers)}
\\bottomrule
\\end{{tabular}}
\\end{{table}}
"""


def write(claim: str) -> pathlib.Path:
    """Description, readings table, tier ladder and criterion table for one claim."""
    out = GENERATED / f"{claim}_section.tex"
    GENERATED.mkdir(parents=True, exist_ok=True)
    out.write_text(section(claim))
    return out
