# Citation-audit fixes for mechanistic_validity.tex, 2026-08-13.
#
# Each entry pairs the exact current text with its replacement and the verbatim
# source text that forced the change. Every replacement must match exactly once.

FIXES = [

# ───────────── FABRICATED / ALTERED QUOTATIONS ─────────────

dict(id="F1", kind="FABRICATED QUOTE", key="border2019no",
 issue="The quotation appears nowhere in the source. It drops 'phenotypes', "
       "rewrites 'genes chosen at random', and silently deletes the source's "
       "one hedge with no ellipsis. In a paper about validity this is the "
       "highest-severity defect present.",
 evidence='Border et al. Discussion: "the candidate genes themselves (with the '
          'possible exception of DRD2) were no more associated with depression '
          'phenotypes than genes chosen at random." Abstract: "As a set, '
          'depression candidate genes were no more associated with depression '
          'phenotypes than noncandidate genes."',
 old=r"""tested the 18 most-studied candidate genes using data from 620,000 individuals: the genes were ``no more associated with depression than randomly chosen genes.''""",
 new=r"""tested the 18 most-studied candidate genes across 621,214 individuals: the candidate genes ``(with the possible exception of DRD2) were no more associated with depression phenotypes than genes chosen at random.''"""),

dict(id="F2", kind="FABRICATED QUOTE", key="belinkov2022probing",
 issue="Two unmarked alterations inside a quotation: 'intermediate' is inserted, "
       "and the source's symbol f is silently replaced by 'the model' behind an "
       "ellipsis that reads as an omission rather than a substitution.",
 evidence='Belinkov 2022 4.3: "the probing framework may indicate correlations '
          'between representations f_l(x) and linguistic property z, but it does '
          'not tell us whether this property is involved in predictions of f."',
 old=r"""the probing framework ``may indicate correlations between intermediate representations""",
 new=r"""the probing framework ``may indicate correlations between representations"""),

dict(id="F3", kind="FABRICATED QUOTE", key="lijanson2024optimal",
 issue="Grammatical alteration inside a quotation: 'their' changed to 'its' to "
       "fit the singular subject.",
 evidence='Source: "OA indicates that the manual circuits are approximately '
          'optimal for their size."',
 old=r"""the manual circuit is ``approximately optimal for its size''""",
 new=r"""``the manual circuits are approximately optimal for their size''"""),

dict(id="F4a", kind="FABRICATED QUOTE", key="wang2023interpretability",
 issue="Presented as the authors' own words, but it is a construction from two "
       "separate passages of the source. The attributive frame makes it read as "
       "a quotation.",
 evidence='Wang abstract: "Our explanation encompasses 26 attention heads '
          'grouped into 7 main classes". The template appears separately in 1: '
          '"sentences such as \'When Mary and John went to the store, John gave '
          'a drink to\' should be completed with \'Mary\'".',
 old=r"""The claim, in the authors' own count: ``The IOI circuit uses 26 attention heads grouped into 7 main classes""",
 new=r"""The claim, in the authors' own count, encompasses ``26 attention heads grouped into 7 main classes"""),

dict(id="F4b", kind="FABRICATED QUOTE", key=None,
 issue="The paper's own paraphrase set in quotation marks under an attributive "
       "frame. Not verbatim in the source.",
 evidence="No matching string in the source; this is the paper's summary.",
 old=r"""assigns two of four heads ``an amplification role the authors flag as speculation.''""",
 new=r"""assigns two of four heads an amplification role that the authors flag as speculation."""),

dict(id="F4c", kind="FABRICATED QUOTE", key="tab:tier-promotion",
 issue="Quoted as a threshold from the paper's own table, but the table says "
       "'methods', not 'variants'.",
 evidence=r"tab:tier-promotion reads $\geq 2$ ablation methods.",
 old=r"""``at least 2 ablation variants''""",
 new=r"""``$\geq 2$ ablation methods''"""),

# ───────────────────────── WRONG ─────────────────────────

dict(id="W2", kind="WRONG", key="meloux2025everything",
 issue="Meloux et al. never studied IOI. Their worked example is Boolean "
       "functions on small MLPs; IOI appears only in their related work and "
       "reference list. The paper states this correctly 180 lines earlier. This "
       "was also the document's only bare 'et al.' with no citation key.",
 evidence='Meloux abstract: "We systematically test the identifiability of both '
          'strategies using simple tasks (learning Boolean functions) and '
          'multi-layer perceptrons small enough to allow a complete enumeration '
          'of candidate explanations."',
 old=r"""Meloux et al.\ find alternative IOI circuits with comparable faithfulness""",
 new=r"""\citet{chen2026circuits} exhibit two IOI subgraphs at 100\% accuracy sharing 4.1\% of their edges"""),

dict(id="W7", kind="WRONG", key="V4",
 issue="Criterion V4 is renamed here, contradicting the criteria table, the IOI "
       "scorecard, the appendix, and the paper's own argument that "
       "anthropomorphism is the salient case rather than the criterion.",
 evidence="Everywhere else in the document V4 is 'Unlicensed labeling'.",
 old=r"""V4 Anthropo-\newline morphism check""",
 new=r"""V4 Unlicensed\newline labeling"""),

dict(id="W8", kind="WRONG", key="roberts2021common",
 issue="Roberts et al. never tested what the models learned -- that is DeGrave "
       "et al. on a different, smaller model set. The body text gets this right; "
       "only the table is wrong.",
 evidence='Roberts abstract: "61 studies were included... none of the models '
          'identified are of potential clinical use due to methodological flaws '
          'and/or underlying biases."',
 old=r"""0/61 models learned COVID pathology""",
 new=r"""0/61 models clinically usable (methodological flaws and bias)"""),

dict(id="W3", kind="WRONG", key="freiesleben2025benchmarking",
 issue="Two of the three named theorists are absent from the source. 'Cronbach' "
       "and 'Meehl' each occur zero times; the framework is credited to Messick "
       "and Kane.",
 evidence='Source: "often referred to as construct validity (Kane, 2013, '
          'Messick, 1995)" and "first introduced by Messick (1995)".',
 old=r"""develop a psychometric framework for benchmark evaluation grounded in Cronbach, Meehl, and Messick""",
 new=r"""develop an argument-based construct-validity framework for benchmark evaluation, following Messick and Kane"""),

dict(id="W4", kind="WRONG", key="bean2025measuring",
 issue="Stated as a bound when the source gives it exactly, and the denominator "
       "is dropped.",
 evidence='Source 5.6: "At present, only 16.0% of reviewed benchmarks conducted '
          'any statistical testing." n = 445.',
 old=r"""\citet{bean2025measuring} find that fewer than 16\% of LLM benchmarks use statistical validity methods""",
 new=r"""\citet{bean2025measuring} find that only 16\% of 445 reviewed LLM benchmarks conduct any statistical testing"""),

dict(id="W5", kind="WRONG", key=None,
 issue="Arithmetic error. The appendix scorecard tallies 7 Inconclusive plus 5 "
       "Untested, and prints those figures itself.",
 evidence="Appendix summary: '7 Inconclusive, 5 Untested'. 7 + 5 = 12.",
 old=r"""Of the 36 criteria applied to the IOI circuit, eleven are Untested or Inconclusive""",
 new=r"""Of the 36 criteria applied to the IOI circuit, twelve are Untested or Inconclusive"""),

dict(id="W6a", kind="WRONG", key=None,
 issue="'Five layers' introduces a list of seven. The abstract says seven.",
 evidence="Seven follow: description mode, evidence families, metrics, criteria, "
          "validity types, synthesis, verdict.",
 old=r"""The framework evaluates such a claim through five layers:""",
 new=r"""The framework evaluates such a claim through seven layers:"""),

dict(id="W6b", kind="WRONG", key=None,
 issue="Same error, second occurrence.",
 evidence="See W6a.",
 old=r"""evaluates mechanistic claims through five layers in pipeline order""",
 new=r"""evaluates mechanistic claims through seven layers in pipeline order"""),
]

# 'Systems:' is not a framework term -- the framework has description modes,
# validity types and scope, not systems. Applied to claims/*.yaml (the source of
# record) and to paper/generated/*.tex (the current output), since the render
# pipeline cannot regenerate them while audit.py is broken.
SYSTEMS_LABEL = ("Systems:", "Evaluated on:")
