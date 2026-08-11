# How much of the faithfulness spread is the ablation value alone?

**Status:** DRAFT — not frozen.

Sections use the [OSF Preregistration](https://osf.io/prereg/) question titles verbatim. A
question that does not apply is answered **N/A** with the reason, never deleted.

## Research questions or hypotheses

Intervention reach asks whether a result survives being measured a different way. It blocks the
next tier for 3 of 16 audited claims and is attempted in 14, so the gap is not that the field
ignores it — it is that agreement across methods is rarely demonstrated.

Miller et al. show that faithfulness defined over a six-tuple of methodological choices ranges
from below 0% to above 100%. That is a joint result. This study decomposes one axis of it.

**H1.** Varying the ablation value alone, with the other five dimensions fixed at the origin
paper's own settings, moves faithfulness by more than 10 percentage points of the full model's
logit difference.

The stake is that a single axis reproducing a large fraction of the published spread would mean
the headline number is a property of one arbitrary choice, not of the circuit.

## Foreknowledge of data or evidence

**A previous version exists**, frozen 2026-08-08 as one section of a multi-criterion document.
**It has not been run.** Content is carried forward here, scoped to this criterion alone.

**Miller et al.'s result is public and is the reason this study exists.** They establish that the
six-tuple jointly produces the full range. This does not reproduce that result; it answers a
question their design does not separate, namely how much of the spread one axis carries on its
own. Their paper is the source of the six-tuple and is cited as such.

**The 10-point threshold was set before any measurement** and is inherited from the superseded
document unchanged.

**Nothing about the per-axis spread has been computed by us.**

## Explanation of foreknowledge and managing unintended influences

Knowing that the joint spread is enormous makes H1 likely, which is why the design fixes the
other five dimensions explicitly and tabulates them: a large spread here is only interpretable if
the reader can see that nothing else moved.

The five fixed dimensions are stated in this document, not chosen at run time. Under-specifying
"everything else" is the precise failure Miller et al. exist to demonstrate, and an earlier draft
of this design committed it before external review caught it.

## Study type

Experimental. The ablation value is manipulated.

## Intention for causal interpretation

Yes. Each ablation is an intervention; the question is whether the measured consequence depends
on how the intervention is defined.

## Blinding of experimental treatments

N/A — no human judgement enters the measurement.

## Additional blinding during research or analysis

All six dimensions are fixed in the table below before any run, and the varied one is named in
advance.

## Study design

GPT-2 small. The published 26 (head, position) pairs, unmodified. One dimension varies:

| dimension | held at |
|---|---|
| granularity | (head, position) pairs, as the origin paper specifies them |
| component type | attention heads only; no MLPs, no layer norms |
| token positions | the position assignment published for each head class |
| direction | ablate the complement, measuring whether the circuit alone suffices |
| circuit set | the published 26 pairs, unmodified |
| **ablation value** | **varied: zero, mean over ABC, resample from ABC, Gaussian noise** |

This shares its runs with the specificity study, so the two report the same underlying
measurements under different questions.

## Randomization

Resample draws and noise draws use a seed fixed here before any run: `0`.

## Data collection procedures

Wang et al.'s templates and published circuit, at commits recorded at freeze.

## Data collection procedures - File upload

N/A.

## Sample size

1,000 prompts per ablation value.

## Sample size rationale

The quantity is a spread across four values, so each value's interval must be narrow relative to
the 10-point threshold. 1,000 prompts places the logit-difference mean well inside that, and the
design does not support claims about differences between two ablation values of a few points.

## Starting and stopping rules

**Gate 1: the unablated baseline must match the published one.** The full model's logit
difference is measured first and compared to the origin paper's. A baseline that does not match
means the templates differ, and every downstream percentage would be a percentage of the wrong
denominator.

**Gate 2: each ablation must be what it claims.** Mean and resample ablations are drawn from the
task's own reference distribution; the draw is recorded and reported so a reader can tell which
distribution produced which number.

## Manipulated variables

The ablation value: zero, mean over ABC, resample from ABC, Gaussian noise.

## Measured variables

Faithfulness at each ablation value, as a percentage of the full model's logit difference; the
unablated baseline; and the spread across the four values.

## Measured variables - File upload

N/A.

## Indices

The spread — the range across the four ablation values — reported alongside all four values
rather than in place of them.

## Indices - File upload

N/A.

## Statistical models

None fitted. Bootstrap intervals per value.

## Statistical models - File upload

N/A.

## Transformations

Faithfulness is expressed as a percentage of the full model's logit difference, which is the
origin paper's own normalization.

## Inference criteria

**H1 holds** if the four values disagree by more than 10 percentage points of the full model's
logit difference.

All four are reported together with the spread as the headline, and the five fixed dimensions are
restated alongside so the number is interpretable. A spread reported without the fixed dimensions
is not a result this study produces.

**A small spread is the more surprising outcome** and would mean the ablation value is not what
drives the published range, which would locate the instability in one of the other five axes.

## Data inclusion and exclusion

All four ablation values are reported. Nothing is dropped after its value is seen.

## Missing data

A value that fails to compute is reported as failed with the error.

## Other planned analysis

Exploratory and labelled so. Decomposing a second axis would be a different study and needs its
own registration.

## Context and additional information

**What no outcome licenses.** One axis of a six-tuple, one circuit, one model. This apportions a
published spread; it does not establish which ablation value is correct, and no such claim
follows from it.

---

## Log

Append only. Never edit above the line.

The last column distinguishes an amendment from a deviation: `nothing run`, `no results seen`,
`results not opened`, `results seen`.

```
2026-08-11  created, superseding the 2026-08-08 document   nothing run
```
