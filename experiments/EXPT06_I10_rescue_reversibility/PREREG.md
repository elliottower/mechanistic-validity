# Does restoring an ablated component restore the behavior?

**Status:** DRAFT — not frozen.

Sections use the [OSF Preregistration](https://osf.io/prereg/) question titles verbatim. A
question that does not apply is answered **N/A** with the reason, never deleted.

## Research questions or hypotheses

Every faithfulness number computed by ablation assumes the ablation removes a component's
contribution and nothing else. If restoring the component does not restore the behavior, the
ablation perturbed the network in ways the component list does not describe, and the assumption
fails silently — no faithfulness score reports it.

Rescue reversibility is attempted in 3 of 16 audited claims.

**H1.** Restoring an ablated head class from cached clean activations returns the logit
difference to baseline within numerical tolerance.

**H2.** The partial recovery curve is monotone in the number of heads restored.

H1 is a sanity condition and is expected to hold; its value is that failure would be severe.
H2 is the informative one, because non-monotonicity would mean heads interact in ways a
component list cannot express.

## Foreknowledge of data or evidence

**A previous version exists**, frozen 2026-08-08 as one section of a multi-criterion document.
**It has not been run.** Content is carried forward here, scoped to this criterion alone.

**H1 is expected to hold and is registered anyway.** A restoration test that passes is not a
finding, and saying so in advance is what stops a passing result from being written up as one.

**Nothing about recovery has been computed by us.**

## Explanation of foreknowledge and managing unintended influences

The 1% tolerance under Inference criteria is inherited unchanged from the superseded document and
was set before any measurement.

Because H1 is expected to pass, the reporting commitment matters more than the prediction: the
partial curve is reported in full whether or not it is monotone, and exceptions are named
individually rather than summarized.

## Study type

Experimental. Ablation and restoration are both interventions.

## Intention for causal interpretation

Yes. The design intervenes twice and asks whether the second undoes the first.

## Blinding of experimental treatments

N/A — no human judgement enters the measurement.

## Additional blinding during research or analysis

The tolerance, the head classes, and the restoration order are fixed here before any run.

## Study design

GPT-2 small, the published 26-head IOI circuit in seven role classes.

Two stages. **Full restoration:** ablate each head class, restore it from cached clean
activations, measure recovery. **Partial curve:** restore `k` of `n` heads for `k = 1..n`, tracing
recovery as a function of how much is put back.

Restoration order for the partial curve is fixed in advance rather than chosen to produce a
curve, and is reported with the result.

## Randomization

Prompt sampling uses a seed fixed here before any run: `0`.

## Data collection procedures

Wang et al.'s templates and published head classes; activations cached from the clean forward
pass. Commits recorded at freeze.

## Data collection procedures - File upload

N/A.

## Sample size

1,000 prompts per condition, unless the input space is smaller, in which case it is enumerated
and the enumeration is stated.

## Sample size rationale

H1 asks whether a recovered value sits within 1% of baseline, so the binding requirement is that
the interval on the recovered logit difference be narrower than that tolerance. 1,000 prompts
achieves it. H2 compares adjacent points on a curve and is reported with intervals rather than
tested for significance at each step.

## Starting and stopping rules

**Gate 1: caching must be exact.** Restoring *all* components must reproduce the clean forward
pass to numerical tolerance before any partial restoration is interpreted. This checks the
plumbing rather than the model, and a failure here voids every number downstream.

**Gate 2: the ablation must bite.** Each head class's ablation must move the logit difference
measurably, or there is nothing for restoration to recover and the class is reported as such.

## Manipulated variables

Which head class is ablated, and how many of its heads are restored.

## Measured variables

Clean baseline logit difference; ablated logit difference per class; recovered logit difference
at full restoration; and recovery at each `k` in the partial curve.

## Measured variables - File upload

N/A.

## Indices

None. Recovery is reported per class and per `k`; no single reversibility score is formed.

## Indices - File upload

N/A.

## Statistical models

None fitted. Bootstrap intervals on each recovery value.

## Statistical models - File upload

N/A.

## Transformations

Recovery is expressed relative to the clean baseline.

## Inference criteria

**H1 holds** if full-restoration recovery is within 1% of baseline for every head class.

**H2 holds** if the partial curve is monotone in `k`. Exceptions are named individually with the
`k` at which they occur, rather than reported as a rate.

**A non-monotone or incomplete recovery is the outcome that matters.** It would show the ablation
perturbs the network in ways the component list does not capture, which bears on every
faithfulness number computed by ablation — including the ones this project's other studies
compute. That consequence is stated here so it cannot be softened after the fact.

Every effect is reported with an interval; no point estimate stands alone.

## Data inclusion and exclusion

All seven classes and every `k` are reported. Nothing is dropped after its value is seen.

## Missing data

A cell that fails to compute is reported as failed with the error.

## Other planned analysis

Exploratory and labelled so.

## Context and additional information

**What no outcome licenses.** One circuit, one model, one restoration mechanism. Reversibility
here does not establish that ablation is clean in general, and a failure would not establish
which alternative measurement to prefer.

---

## Log

Append only. Never edit above the line.

The last column distinguishes an amendment from a deviation: `nothing run`, `no results seen`,
`results not opened`, `results seen`.

```
2026-08-11  created, superseding the 2026-08-08 document   nothing run
```
