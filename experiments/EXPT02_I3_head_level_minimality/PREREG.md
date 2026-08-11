# Do all 26 heads still earn their place under Wang et al.'s own minimality score?

**Status:** DRAFT — not frozen.

Sections use the [OSF Preregistration](https://osf.io/prereg/) question titles verbatim, so
this maps onto a registration without being rewritten. A question that does not apply is
answered **N/A** with the reason, never deleted.

## Research questions or hypotheses

Wang et al. certify their 26-head IOI circuit as minimal. The criterion is existential: for
every node `v` in circuit `C` there **exists** a subset `K ⊆ C \ {v}` whose minimality score

    m(v; K) = | F(C \ K) − F(C \ (K ∪ {v})) |

is high, where `F` is their faithfulness protocol — mean-ablate everything outside the set over
the ABC reference distribution, measure the IOI logit difference.

Re-measured under that definition, does every head still clear the bar, and how much does the
verdict depend on which `K` is chosen?

**H1.** At least 8 of 26 heads fail under `K = ∅` — single-head ablation, the naive necessity
test — because Backup Name Movers compensate for Name Movers.

**H2.** At least 23 of 26 clear under `RW`, the K sets Wang et al. print in Appendix K.

**H3.** All 26 clear under a greedily chosen `K`.

**H4.** Mean `m(v)` under class-based `K` exceeds mean `m(v)` under `K = ∅` by at least 3×,
quantifying how much redundancy masks single-head importance.

## Foreknowledge of data or evidence

Substantial, and it is why this document exists rather than the earlier one.

**A previous pre-registration of this study exists**, frozen 2026-08-05 at commit `c643450` of
the predecessor repository. It has not been run and no result from it has been seen. This
supersedes it. What changed:

- Its implementation claimed as a **finding** that Wang et al. "print no rule for choosing K."
  That is false. §4.2 states the rule and Appendix K, titled *Minimality sets*, prints
  `K ∪ {v}` for all 26 nodes in Figure 20. `RW` is therefore implementable by transcription and
  is included here.
- It misattributed Figure 6, which belongs to the **completeness** criterion, as the minimality
  protocol. Wang's greedy procedure is Algorithm 3, also for completeness.
- Its implementation used resample ablation from a natural-text pool while the document
  specified mean ablation over ABC. That code is discarded.

**The conceptual claim is not ours.** Arcuschin, uit de Bos and Garriga-Alonso (2024) already
argued that the existential quantifier makes minimality choice-dependent — *"a non-minimal
circuit can become minimal when you increase the granularity"* — with toy examples and no
measurement. Chhabra et al. (arXiv:2503.01896) compute Wang's minimality score on IOI circuits
in fine-tuned GPT-2 without stating their K. The contribution here is the measurement on the
published circuit and the comparison across K regimes, not the observation.

**Nothing about `m(v; K)` on this circuit has been computed by us at any point.**

## Explanation of foreknowledge and managing unintended influences

The prior work above concerns whether the criterion *can* be gamed, not whether it *is* on this
circuit. It constrains none of the thresholds below, which are carried unchanged from the
superseded document except where an error required correction.

The one place foreknowledge could bias a threshold is H2's "at least 23 of 26": Wang report all
26 clearing. Predicting 23 rather than 26 anticipates that some fail on re-measurement, and that
prediction is stated before any run.

## Study type

Observational re-measurement of a published result. No new system is built.

## Intention for causal interpretation

Yes, and it is the point. Minimality is a causal claim about each head: removing it changes the
circuit's output. This measures that claim under the original definition.

## Blinding of experimental treatments

N/A — no treatments are assigned. Every head is measured under every regime.

## Additional blinding during research or analysis

N/A — the analysis is fully specified below, with no outcome-dependent choices.

## Study design

Four regimes for choosing `K`, crossed with all 26 heads.

| | `K` is |
|---|---|
| `R0` | the empty set — single-head ablation |
| `RC` | the other members of `v`'s published class |
| `RG` | chosen greedily to maximise `m(v; K)`, fitted on one half and scored on the other |
| `RW` | exactly what Wang et al. print in Appendix K, Figure 20 |

`RW` is neither `R0`, `RC` nor `RG`: it is nested for the Name Movers (`(9,9)` with `K = ∅`,
`(10,0)` with `K = {(9,9)}`, `(9,6)` with `K = {(9,9),(10,0)}`), cross-class for induction heads
`(5,9)` and `(5,8)` whose `K` is the Negative Name Movers `{(11,10),(10,7)}`, class-wide for
S-Inhibition, Duplicate Token and Previous Token, and "all previous name movers and backup name
movers" for six of the eight Backup Name Movers.

`RG` uses a fit/held-out split so a greedily selected `K` cannot inflate the score it was
selected to maximise.

## Randomization

Split-half assignment for `RG` uses a seed fixed in this document before any run: `0`.

## Data collection procedures

No new data. GPT-2 small and the IOI templates of Wang et al., at commits recorded at freeze.

## Data collection procedures - File upload

N/A — no instrument beyond this document.

## Sample size

1,000 IOI prompts, stratified so every template is equally represented. A secondary arm uses
roughly 7 prompts per template, matching the size Miller et al. attribute to the original.

## Sample size rationale

Miller et al. report faithfulness increasing monotonically with reference-set size, so the
comparison between the two arms tests whether the original's small sample was generous or
conservative. 1,000 gives a bootstrap interval on `m(v)` narrow enough to separate a head at
the 1% bar from one at 3%.

## Starting and stopping rules

All 26 heads under all four regimes run to completion. No interim analysis.

## Manipulated variables

The ablated set. Everything outside `C \ K` and `C \ (K ∪ {v})` is mean-ablated over the ABC
distribution, with the mean computed **per template**, quoting §2.1: *"To ensure that
grammatical information is constant when averaging, we compute the mean of a node across
samples of the same template."*

## Measured variables

`m(v; K)` per head per regime, with a bootstrap confidence interval over prompts.

## Measured variables - File upload

N/A.

## Indices

None. `m(v; K)` is reported directly, not combined into a composite.

## Indices - File upload

N/A.

## Statistical models

None fitted. Bootstrap resampling of prompts, 1,000 resamples, for an interval on each `m(v)`.

## Statistical models - File upload

N/A.

## Transformations

None. Logit differences are analyzed on their native scale.

## Inference criteria

**Why this threshold is absolute while the others in this series are not.** The anchor follows
the metric's scale. θ = 1% of F(M) is Wang et al.'s own published bar for this exact quantity, so
it needs no null to interpret — a criterion derived from the source paper is stronger than one
derived from a null we compute. The companion registrations anchor to measured nulls because
their metrics have no published bar.

**The bar is Wang et al.'s own:** a head clears if `m(v; K)` is at least 1% of `F(M)`, quoting
their *"at least 1% of the original logit difference."* With `F(M) = 3.56`, θ = 0.0356.

A head **clears** if the lower bound of its bootstrap interval exceeds θ, **fails** if the upper
bound is below θ, and is **unresolved** otherwise. Unresolved is reported as its own category
and never collapsed into either.

No p-values. Intervals are reported and interpreted as intervals.

## Data inclusion and exclusion

All 26 heads are reported under all four regimes whatever they return.

## Missing data

A cell that fails to compute is reported as failed with the error, never dropped or imputed.

## Other planned analysis

Anything beyond the above is exploratory and labelled so in the write-up.

## Context and additional information

**What no outcome licenses.** A pass here does not make the circuit minimal in the edge-level
sense of Shi et al., does not settle the Shi / Li–Janson disagreement, and does not transfer to
any other ablation method. It answers one question: whether Wang et al.'s own test, re-run,
still returns their own verdict.

**Relation to I6.** I6 tests whether the published 26-head circuit dissociates from the
greater-than circuit, using those 26 heads as its object. If this study finds that some do not
earn their place, that does not retroactively change what I6 ablates: I6 is registered against
the circuit as the literature states it. The two are testing different properties of the same
nominal object, and neither depends on the other's result.

**Compute.** `RG` with the registered cap of |K| ≤ 25 is roughly 40M forward passes and needs a
GPU. This runs on Modal, not locally.

---

## Log

Append only. Never edit above the line.

The last column is what distinguishes an amendment from a deviation, so you do not have to
decide which word to use: `nothing run`, `no results seen`, `results not opened`, `results seen`.

```
2026-08-11  created, superseding the 2026-08-05 document   nothing run
```
