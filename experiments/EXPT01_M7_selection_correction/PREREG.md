# How much of a reported figure belongs to the threshold that selected it?

**Status:** DRAFT — not frozen.

Sections use the [OSF Preregistration](https://osf.io/prereg/) question titles verbatim. A
question that does not apply is answered **N/A** with the reason, never deleted.

## Research questions or hypotheses

Selection correction is the criterion no audited claim attempts: 0 of 16. A figure computed on
the slice a method itself selects is not an estimate of the effect in general, and the gap
between the two is the winner's curse.

Copy suppression carries two separately selected numbers, and they need different treatments
because only one is measured by a procedure that survives being moved off the selected slice.

**H1.** The behavioral figure falls on an unselected sample. The published 80% counts
completions meeting three qualitative conditions, evaluated on the top 5% of completions by the
head's own effect. Applying the same three conditions to a sample drawn without reference to
that effect returns a lower proportion. **Direction is committed; magnitude is not.**

**H2.** Recovered fidelity increases monotonically in the threshold `k`, and the published
`k = 5%` sits below the `k = 100%` value.

H1 is the prediction worth staking, because it is the one that can be wrong in the interesting
direction: three proportions agreeing within their intervals would show the selection buys
nothing, which is a result about this claim rather than a failure of the audit.

## Foreknowledge of data or evidence

**A previous version exists**, frozen 2026-08-08 as one section of a multi-criterion document.
**It has not been run.** Content is carried forward here, scoped to this criterion alone.

**That document was revised twice before anything ran, both times after external review, and
both revisions are recorded because they changed what this experiment measures:**

- The first draft proposed recomputing the fidelity metric on the completions the published
  figure excludes. That inverts what the measurement preserves — the method is defined to keep
  attention to the highest-probability predicted source tokens and delete the rest, so running
  it on the complement measures the discarded mass rather than providing a held-out estimate.
  The design was split in two as a result: H1 moves the behavioral conditions onto an unselected
  sample, which they survive, and H2 sweeps the threshold, which leaves the metric intact.
- Superseded hashes are recorded so the revision is auditable:
  `961f1d0f91d34ba28c1e5cade52add3549ab48e31dd908d82f682526e94b3189` and
  `61a78fad62e45549db37fb136b9678c517b331fd6753be2c9d4f73c5ca561224`.

**Nothing about either quantity has been recomputed by us.**

## Explanation of foreknowledge and managing unintended influences

The published 80% is known, so H1 commits to a direction rather than a magnitude. Committing to a
magnitude would be committing to a number chosen after seeing the one it is compared against.

The scope limit under Context is stated now rather than after the result: H2 measures the
threshold's contribution, not an unbiased re-estimate.

## Study type

Experimental. The selection threshold and the sampling frame are manipulated.

## Intention for causal interpretation

N/A. This estimates how much of a reported number is attributable to selection, not an effect in
the model.

## Blinding of experimental treatments

N/A — the three qualitative conditions are the source paper's, applied unchanged.

## Additional blinding during research or analysis

The three conditions, the sampling frames and the threshold grid are all fixed here before any
completion is scored.

## Study design

GPT-2 small throughout, so every result is comparable and no cross-model transfer is assumed.

**H1 — the behavioral figure on unselected samples.** Three samples, one metric: the original
top-5%-by-effect sample, a random sample drawn without reference to the head's effect, and a
sample stratified across effect deciles. The source paper's three qualitative conditions are
applied unchanged to all three.

**H2 — fidelity as a function of the threshold.** Sweep `k` over 1, 5, 10, 25, 50 and 100%,
holding every other element of the method fixed, and report recovered KL divergence at each. The
distance from `k = 5%` to `k = 100%` is the quantity this criterion asks for.

## Randomization

Sample draws use a seed fixed here before any run: `0`.

## Data collection procedures

The source paper's own prompt distribution and the published head, at commits recorded at freeze.

## Data collection procedures - File upload

N/A.

## Sample size

1,000 prompts per condition, unless the input space is smaller, in which case it is enumerated
and the enumeration is stated.

## Sample size rationale

H1 compares three proportions, so the binding requirement is an interval narrow enough to
separate them. 1,000 per condition places a proportion near 0.8 to within a few points, which is
finer than the gap H1 predicts. H2 is a curve rather than a contrast and needs precision per
point rather than power.

## Starting and stopping rules

**Gate 1: the three conditions must reproduce the published figure on the published slice.**
Applying them to the original top-5% sample must return approximately 80%. If it does not, the
conditions have been operationalized differently from the source and no comparison across
samples means anything. Reported whatever it returns.

## Manipulated variables

The sampling frame in H1; the threshold `k` in H2.

## Measured variables

The proportion meeting all three conditions, per sample, with intervals; recovered KL divergence
per `k`; and the gap between the selected and unselected estimates.

## Measured variables - File upload

N/A.

## Indices

None. The three proportions are reported individually and the curve is reported in full; neither
is reduced to a single correction factor.

## Indices - File upload

N/A.

## Statistical models

None fitted. Intervals on proportions and on recovered KL.

## Statistical models - File upload

N/A.

## Transformations

None.

## Inference criteria

**H1 holds** if the unselected sample's proportion falls below the top-5% sample's, with
non-overlapping intervals. **The three agreeing within their intervals refutes the concern for
this figure**, and is reported as such rather than as a null.

**H2 holds** if recovered fidelity is monotonic in `k` and the published threshold sits below the
`k = 100%` value. **A flat curve refutes the concern**, showing the threshold does no work and
the published figure is threshold-independent.

Every effect is reported with an interval; no point estimate stands alone.

## Data inclusion and exclusion

All three samples and all six thresholds are reported. Nothing is dropped after its value is seen.

## Missing data

A condition that fails to compute is reported as failed with the error.

## Other planned analysis

Exploratory and labelled so.

## Context and additional information

**Scope, stated before the result.** H2 measures the threshold's contribution, not an unbiased
re-estimate of the published quantity. No procedure recovers the latter without redefining the
source paper's metric, and redefining a source paper's metric is outside what this audit does.

**Why a neighboring criterion is excluded.** Confounding sensitivity (I8) is not run here. The
framework motivates it as residual-stream information correlated with both the ablated component
and the output, which is a real threat, but the instrument it names — the E-value — assumes an
observational effect estimate. An ablation is an intervention, so the E-value's bias model does
not apply. Whether I8 has a well-formed interventional analogue is a question for the framework
rather than an experiment to run, and the omission is recorded so it is not read as an oversight.

**What no outcome licenses.** One claim, two figures, one model. A winner's curse here says
nothing about the size of the effect elsewhere, though it would raise the question for any figure
reported on a method-selected slice — which is most of them.

---

## Log

Append only. Never edit above the line.

The last column distinguishes an amendment from a deviation: `nothing run`, `no results seen`,
`results not opened`, `results seen`.

```
2026-08-11  created, superseding the 2026-08-08 document   nothing run
```
