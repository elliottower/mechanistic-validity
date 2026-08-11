# Does the IOI circuit double-dissociate from the greater-than circuit?

**Status:** DRAFT — not frozen.

Sections use the [OSF Preregistration](https://osf.io/prereg/) question titles verbatim. A
question that does not apply is answered **N/A** with the reason, never deleted.

## Research questions or hypotheses

Necessity shows a circuit matters for its task. It does not show the circuit is *for* that task —
a component set that damages everything when ablated damages its own task too. The crossed
design separates them: ablating circuit A should damage task A while sparing task B, and
ablating circuit B should damage task B while sparing task A. Both arms must hold.

Wang et al.'s 26-head IOI circuit and Hanna et al.'s greater-than circuit are the two published
circuits in GPT-2 small precise enough to test this on.

**H1.** The four-cell interaction contrast clears its null by the margin fixed under Inference
criteria — the dissociation holds. A previous version of this study predicted 0.40 in absolute
terms, and that value is retained as a secondary prediction so the two can be compared.

**H2.** Both cross-task cells nonetheless exceed their size- and layer-matched random controls —
the dissociation is *impure*, and each circuit carries task-general machinery alongside its
task-specific part.

H2 is the prediction worth staking. A clean dissociation is what the field assumes; an impure
one says circuits are not the modular objects the vocabulary implies.

## Foreknowledge of data or evidence

Substantial, and it points against H1.

**A previous pre-registration exists**, frozen 2026-08-05 at commit `c643450` of the predecessor
repository. It has not been run. Its implementation diverged from it — zero/resample/native
ablation and a permutation test where the document specified mean ablation, a normalized `D`,
200 matched random controls and a bootstrap interval. That code is discarded.

**Li and Subramani (arXiv:2605.08348) ran this comparison and got the opposite answer.** Their
criterion is the same one used here — own-circuit drop against mean other-circuit drop — and
they report *"circuits turn out not to be task-specific: ablating one task's circuit damages
another task's performance about as much as that task's own circuit does."* Their panel is
Gemma 2, Llama 3.2, Qwen3 and OLMo-2, with EAP-derived per-example circuits. **No GPT-2, no
greater-than, not the published Wang circuit.**

**Merullo et al. (arXiv:2310.08744) point the other way for this exact pair**, reporting that
*"preliminary work on other tasks that do not share this connection to the IOI task (e.g.,
predicting numbers greater than some given integer) had virtually no overlap with the IOI
circuit."*

**Hanna, Belinkov and Pezzelle (arXiv:2503.11302)** import the dissociation framing from
neuroscience and report a bidirectional result, measured by *sufficiency* rather than ablation
necessity, on models that do not include GPT-2 small. It was absent from the superseded document
and is cited here.

**Nothing about the four-cell contrast on this pair has been computed by us.**

## Explanation of foreknowledge and managing unintended influences

The literature is split and both halves are public, so neither reading can be presented as a
surprise.

The superseded document fixed H1's threshold at 0.40 with no stated derivation, and that is the
weakest part of it. This version anchors the criterion to the matched-random null the study
already measures, and keeps 0.40 as a secondary prediction so the inherited number can be
checked against a derived one rather than quietly replaced.

Li and Subramani's result makes H1 less likely than when the threshold was set. That is stated
here rather than used to move the threshold.

## Study type

Experimental. Ablation is an intervention.

## Intention for causal interpretation

Yes. The whole design is a crossed intervention.

## Blinding of experimental treatments

N/A — no human judgement enters the measurement.

## Additional blinding during research or analysis

N/A — the contrast and its threshold are fixed below.

## Study design

Two circuits × two tasks, plus matched random controls.

|  | IOI task | greater-than task |
|---|---|---|
| **ablate IOI circuit** | expected large drop | expected small drop |
| **ablate GT circuit** | expected small drop | expected large drop |
| **ablate matched random set** | control | control |

Controls are 200 random component sets per circuit, matched on size and on layer distribution,
so a cross-task effect is compared against what any set of that shape does rather than against
zero.

## Randomization

Control sets are drawn with a seed fixed here before any run: `0`.

## Data collection procedures

MIB's published IOI and greater-than datasets, loaded through MIB's own code rather than
regenerated. GPT-2 small.

## Data collection procedures - File upload

N/A.

## Sample size

2,000 examples per task.

## Sample size rationale

The contrast is a difference of differences on a bounded quantity. 2,000 examples gives a
bootstrap interval narrow enough to separate a contrast of 0.40 from one of 0.25; it cannot
separate 0.40 from 0.45, and no claim of that precision will be made.

**2,000 is a starting point, not a justified number.** Whether it resolves the registered
criterion depends on the null's spread, which is unknown until measured. Gate 2 makes that
dependency explicit and stops the study rather than letting an underpowered run produce a
verdict — the alternative would be a sample size chosen before a criterion that depends on it,
which is not a justification.

## Starting and stopping rules

**Gate 1: the model must do the tasks.** GPT-2 small must reach at least 95% on each task
unablated. Below that the
study has no signal and the gate result is reported as the outcome.

The gate is live rather than nominal. Xu (arXiv:2606.05378) reports GPT-2 small at *"top-1 13%,
IO-vs-subject 57%"* on IOI, against Wang's 99.3%. A direct check found that discrepancy comes
from a trailing space in the prompt template, which moves the answer to a different BPE token:
without it, 100% IO-over-subject; with it, 52%. The gate uses Wang's template.

**Gate 2: the design must be able to resolve its own criterion.** The matched-random null is
computed **first**, before any own-task or cross-task cell. If the bootstrap interval on the
contrast at the registered sample size is wider than `2 × sd` of that null, the design cannot
distinguish a result at the criterion from one below it, and the study does not proceed at that
sample size. Two responses are permitted and both must be recorded in the log: raise the sample
size until the interval is narrow enough, or report that the criterion is unresolvable at
available compute and stop.

Computing the null first is safe: it uses random component sets and reveals nothing about the
contrast. Choosing the sample size after seeing the contrast would not be, and is excluded by
running the null before any circuit is ablated.


## Manipulated variables

The ablated component set. Mean ablation over each task's own reference distribution, with the
mean computed per template.

## Measured variables

Task accuracy under each ablation, normalized as

    D = (clean − ablated) / (clean − corrupted)

so the two tasks' effects are on a common scale. The superseded implementation reported raw
deficits, which are not comparable across tasks with different metrics.

## Measured variables - File upload

N/A.

## Indices

The four-cell interaction contrast: the mean of the two own-task `D` values minus the mean of
the two cross-task `D` values.

## Indices - File upload

N/A.

## Statistical models

None fitted. Bootstrap over examples, 1,000 resamples, for an interval on the contrast and on
each cell.

## Statistical models - File upload

N/A.

## Transformations

The normalization above. No others.

## Inference criteria

**Why the anchor takes this form.** The anchor follows the metric's scale rather than a house
style. An unbounded contrast gets multiples of its null's standard deviation; a bounded
correlation gets an additive margin, because sd-scaling a quantity capped at 1.0 distorts near
the ceiling; a set overlap with a computable chance value gets a fraction of the chance-to-ceiling
range; and a quantity with a published absolute bar keeps that bar. The four registrations in
this series therefore anchor differently, and the difference is the metric's, not the design's.

**Thresholds are derived from this study's own null, not asserted.** The 200 size- and
layer-matched random sets are measured under the same protocol, so the contrast has a null
distribution and it does not have to be guessed at.

**H1 holds** if the lower bound of the bootstrap interval on the contrast exceeds
`5 × sd(contrast under matched random sets)`. The superseded document fixed this at 0.40 with
no stated derivation; that number is recorded here as what a previous version predicted, and it
is a prediction rather than the criterion. If the null's standard deviation makes 5 sd land far
from 0.40, the criterion is the multiple, and the discrepancy is reported.

**H2 holds** if, for both cross-task cells, the lower bound of the interval on
`D(cross) − D(matched random)` exceeds `2 × sd` of that same null.

The multiples (5 and 2) are fixed here before any run. The standard deviations are not known
and will not be inspected before the contrast is computed.

Both arms must hold for a dissociation. A result where one arm holds and the other does not is
reported as a single dissociation, which is a weaker and different claim.

## Data inclusion and exclusion

All four cells and both control distributions are reported whatever they return.

## Missing data

A cell that fails to compute is reported as failed with the error.

## Other planned analysis

Exploratory and labelled so.

## Context and additional information

**Which circuit this ablates, if I3 lands first.** I3 asks whether all 26 of Wang's heads earn
their place, and predicts at least 8 fail under naive single-head ablation. If that result
arrives before this study runs, it does not change what is ablated here: **this study uses the
published 26-head circuit as its object regardless**, because the claim under test is about the
circuit as the literature states it. Re-running against an I3-revised set would be a different
study and would need its own registration. Fixing this now avoids a resolution order being
chosen after both results are visible.

**What no outcome licenses.** This is one pair of circuits in one model. A dissociation here
says nothing about circuits in general, and Li and Subramani's contrary result on four other
model families stands unaddressed by anything measured here.

**Why it matters anyway.** This criterion is unmet for 7 of the 16 audited claims and is the
sole gate above one tier of the framework. Its status is load-bearing for the paper whichever
way it goes.

---

## Log

Append only. Never edit above the line.

The last column distinguishes an amendment from a deviation: `nothing run`, `no results seen`,
`results not opened`, `results seen`.

```
2026-08-11  created, superseding the 2026-08-05 document   nothing run
```
