# Does the IOI circuit damage its own task more than it damages others?

**Status:** DRAFT — not frozen.

Sections use the [OSF Preregistration](https://osf.io/prereg/) question titles verbatim. A
question that does not apply is answered **N/A** with the reason, never deleted.

## Research questions or hypotheses

Necessity shows a component set matters. Specificity asks whether it matters *for this task*
rather than for everything, and the criterion blocks the next tier for 5 of 16 audited claims
while being attempted in 14 — the common failure is a control the claim's own authors designed.

**H1.** Ablating the IOI circuit costs more on IOI than on either control that exists
independently of this study, under both ablation conditions.

The prediction worth staking is the one that can fail informatively: an independent control
damaged as much as IOI would place the circuit's specificity in question regardless of its
faithfulness, which is a stronger statement than a weak specificity result.

## Foreknowledge of data or evidence

**A previous version exists**, frozen 2026-08-08 as one section of a multi-criterion document.
**It has not been run.** Content is carried forward here, scoped to this criterion alone.

**It was revised once before anything ran, after external review, and the revision changed what
counts.** The first draft counted a self-constructed two-name control toward the criterion. No
published task of that shape with an established baseline exists, so the control would have been
designed by the same people making the claim it tests. Controls are now split by provenance, and
the constructed one is reported without bearing on the verdict.

**Nothing about specificity has been computed by us.**

## Explanation of foreknowledge and managing unintended influences

The provenance split is the whole design, and it is stated before any run precisely because a
control chosen after seeing a deficit is not a control. The constructed task is specified in
advance — same templates as the IOI set with the indirect-object clause removed, same name pool,
same answer-set size — so it can be reported honestly while being excluded from the verdict.

## Study type

Experimental. Ablation is an intervention.

## Intention for causal interpretation

Yes. The circuit is ablated and the consequence measured on several tasks.

## Blinding of experimental treatments

N/A — no human judgement enters the measurement.

## Additional blinding during research or analysis

The control set, its provenance split, and the ablation conditions are fixed here before any
deficit is measured.

## Study design

GPT-2 small throughout, so every result is comparable and no cross-model transfer is assumed.

The published 26-head IOI circuit is ablated under two conditions — zero and resample — and the
deficit measured on IOI and on three controls:

| control | provenance | bears on the verdict |
|---|---|---|
| greater-than | published, own circuit and own literature | yes |
| next-token prediction on held-out natural text | unconstructed; needs no design choices | yes |
| two-name recall with no indirect object | constructed by us | no, reported either way |

The third exists because its absence would be conspicuous, not because it can settle anything.

This shares its ablation runs with the intervention-reach study, so the two report the same
underlying measurements under different questions.

## Randomization

Prompt sampling and resample-ablation draws use a seed fixed here before any run: `0`.

## Data collection procedures

Wang et al.'s templates and published head set; Hanna et al.'s greater-than task; held-out
natural text. Commits recorded at freeze.

## Data collection procedures - File upload

N/A.

## Sample size

1,000 prompts per task per condition, unless a task's input space is smaller, in which case it is
enumerated and the enumeration is stated.

## Sample size rationale

The comparison is between deficits on different tasks, so what matters is that each deficit's
interval is narrow relative to the gap H1 predicts. 1,000 per cell achieves that for a deficit
difference of the size the audit treats as meaningful, and does not support claims about small
differences between the two independent controls.

## Starting and stopping rules

**Gate 1: the model must do every task unablated.** Each task's clean performance is measured
first and reported. A control the model cannot perform has no deficit to lose and cannot serve as
a control.

**Gate 2: the ablation must bite on IOI.** If ablating the circuit does not damage IOI, there is
no specificity question to ask, and that outcome is reported as the finding.

## Manipulated variables

The ablation condition — zero or resample — and the task being measured.

## Measured variables

Clean and ablated performance per task per condition, and the deficit with its interval.

## Measured variables - File upload

N/A.

## Indices

None. Deficits are reported per task; no specificity ratio is formed, because a ratio would hide
which side of it moved.

## Indices - File upload

N/A.

## Statistical models

None fitted. Bootstrap intervals on each deficit.

## Statistical models - File upload

N/A.

## Transformations

None.

## Inference criteria

**H1 holds** if the IOI deficit exceeds the deficit on **both** independent controls, with
non-overlapping intervals, in **both** ablation conditions. Holding in one condition and not the
other is reported as partial and does not count as holding.

**Either independent control damaged as much as IOI refutes specificity** for this circuit, and
is reported as such rather than as an inconclusive result.

The constructed control is reported with its result whichever way it falls, and is never used to
rescue or strengthen the verdict.

Every effect is reported with an interval; no point estimate stands alone.

## Data inclusion and exclusion

All four tasks and both conditions are reported. Nothing is dropped after its result is seen.

## Missing data

A cell that fails to compute is reported as failed with the error.

## Other planned analysis

Exploratory and labelled so.

## Context and additional information

**What no outcome licenses.** One circuit, one model, three controls. Specificity against these
controls is not specificity in general, and the space of tasks a circuit might damage is not
enumerable.

---

## Log

Append only. Never edit above the line.

The last column distinguishes an amendment from a deviation: `nothing run`, `no results seen`,
`results not opened`, `results seen`.

```
2026-08-11  created, superseding the 2026-08-08 document   nothing run
```
