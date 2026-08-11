# Does the circuit's strength track the capability in both directions?

**Status:** DRAFT — not frozen.

Sections use the [OSF Preregistration](https://osf.io/prereg/) question titles verbatim. A
question that does not apply is answered **N/A** with the reason, never deleted.

## Research questions or hypotheses

A structure that appears when a capability appears is suggestive. A structure that also *weakens*
when the capability is removed, and returns when it returns, is doing something the first
observation cannot establish. Developmental interpretability almost always shows onset only.

Two directions, one circuit:

**Onset.** Across training checkpoints, does name-mover strength rise with IOI performance?

**Offset.** Across a graded ladder that degrades and then restores the capability, does circuit
strength follow?

**H1.** Within-seed Spearman correlation between behaviour and name-mover strength across
training exceeds what matched random component sets achieve over the same checkpoints, in all
five seeds. A previous version fixed 0.90 absolutely; retained as a secondary prediction.

**H2.** Across a 40-rung destruction-and-recovery ladder, the correlation between capability and
circuit strength is at least 0.85, with size- and layer-matched random component sets falling at
most half as far.

**H3.** The recovery path differs measurably from the destruction path — hysteresis — meaning
the circuit does not simply retrace its own degradation.

## Foreknowledge of data or evidence

**A previous pre-registration exists**, frozen 2026-08-05 at commit `c643450` of the predecessor
repository. It has not been run. Its content is carried forward; one correction and several
additions:

- The paper scores this criterion as *"untestable in GPT-2 small, which ships no pretraining
  checkpoints."* That is true of OpenAI's release and misleading about the architecture. Each of
  the five Stanford CRFM GPT-2 small runs ships roughly 600 intermediate checkpoints as git
  tags. Enumerating `darkmatter-gpt2-small-x343` returns 609 tags against one branch. The
  superseded document already said this and asked for the paper's sentence to be corrected; it
  has not been.

Prior work, most of which the superseded document did not cite:

- **Chhabra, Zhu and Khalili (arXiv:2503.01896)** do the offset-and-return half on this exact
  model and task — corrupting via toxic fine-tuning, then retraining — reporting the logit
  difference going *"from 3.55 to −11.06 after just 5 epochs"* and recovery to 95–96%
  faithfulness. They do not track a fixed circuit's strength continuously, report a coupling
  coefficient, use matched random controls, or measure hysteresis.
- **Tigges et al. (arXiv:2407.10827)** show onset, and one head acquiring then losing its
  behaviour. Critically, that loss occurs *with task performance stable* — which is a
  **de**coupling, the opposite of what H1 is about, and the superseded document did not note it.
- **Nanda et al. (arXiv:2301.05217)** track structure appearing and memorization being removed
  continuously against a progress measure. Method precedent, not a result about this circuit.
- **Urdshals and Urdshals (arXiv:2501.18666)** show copy-suppression onset in list-sorting
  transformers; the capability never degrades, so it is structure replacement rather than offset.
- **Rojas Nunez et al. (arXiv:2605.28860)** report circuit retention falling under fine-tuning,
  two epoch points, no dose ladder.

**No onset or offset quantity has been computed by us.**

## Explanation of foreknowledge and managing unintended influences

Chhabra et al.'s result makes the offset direction less novel than the superseded document
implied, and their recovery figures are public.

The superseded document fixed 0.90 and 0.85 absolutely with no derivation. H1 is now anchored
to matched random sets tracked over the same checkpoints, and 0.90 is retained as a secondary
prediction. H2's "half as far as random" was already relative and is unchanged.

Tigges et al.'s decoupling is the sharpest constraint: it shows head-level structure can move
while behaviour holds. H1 predicts the opposite pattern for name movers specifically, and that
prediction is now made in full knowledge of a published counter-instance.

## Study type

Observational for onset — the checkpoints already exist. Experimental for offset — the ladder
manipulates the capability.

## Intention for causal interpretation

For the offset arm, yes: the ladder intervenes on the capability and asks what the circuit does.
The onset arm is correlational and is reported as such.

## Blinding of experimental treatments

N/A — no human judgement enters.

## Additional blinding during research or analysis

N/A.

## Study design

**Onset.** Roughly 40 checkpoints per seed, sampled from the ~600 available on a schedule fixed
before any run: every checkpoint below step 100, then thinning geometrically. Behaviour and
name-mover strength measured at each.

**Offset.** A 40-rung ladder degrading IOI performance and then restoring it, with circuit
strength and matched random-set strength measured at every rung. Rungs are defined by a
pre-specified schedule, not chosen to produce a curve.

Checkpoint counts differ between seeds — 609 for four runs and 604 for `expanse-x777` — so the
sampling schedule is defined by step number rather than by index, and the realised set per seed
is reported.

## Randomization

Matched random component sets and the ladder's data ordering use a seed fixed here: `0`.

## Data collection procedures

The five Stanford CRFM runs and their checkpoint tags, resolved by `revision=`. Checkpoints are
git **tags**, not branches; the superseded document said branches, which is wrong and would have
sent an implementation looking in the wrong place.

## Data collection procedures - File upload

N/A.

## Sample size

500 IOI prompts at each checkpoint and each rung.

## Sample size rationale

The quantity is a correlation across ~40 points, so precision on each point matters less than
the number of points. 500 prompts gives a standard error on the logit difference well below the
between-checkpoint variation the correlation is computed over.

## Starting and stopping rules

**Gate 1: the transition must be visible at the sampled resolution.** If IOI performance goes
from floor to ceiling between two adjacent checkpoints, the correlation is uninformative and
that is reported as the finding rather than resampled around.

**Gate 2: the design must be able to resolve its own criterion.** H1 compares the circuit's
correlation against what matched random sets achieve, and that null is unknown until measured.
The random-set correlations are computed **first**, over the same checkpoints. If their spread
across the five seeds exceeds the 0.25 margin H1 requires, the margin cannot be distinguished
from seed-to-seed variation in the null itself, and the study reports that rather than issuing a
verdict. More checkpoints per seed is the permitted response; loosening the margin is not.

Computing the null first is safe: random component sets reveal nothing about the name movers.

## Manipulated variables

For offset: the ladder's degradation and restoration. For onset: nothing — training already
happened.

## Measured variables

IOI logit difference and accuracy; name-mover strength, defined as the summed direct logit
attribution of the name-mover class; the same for matched random sets; and the path difference
between destruction and recovery at matched capability levels.

## Measured variables - File upload

N/A.

## Indices

Spearman correlation between capability and circuit strength, per seed for onset and per ladder
for offset. Hysteresis as the mean absolute difference in circuit strength between the two paths
at matched capability.

## Indices - File upload

N/A.

## Statistical models

None fitted. Bootstrap over prompts within checkpoint; the correlation is over checkpoints.

## Statistical models - File upload

N/A.

## Transformations

None.

## Inference criteria

**Why the anchor takes this form.** The anchor follows the metric's scale rather than a house
style. An unbounded contrast gets multiples of its null's standard deviation; a bounded
correlation gets an additive margin, because sd-scaling a quantity capped at 1.0 distorts near
the ceiling; a set overlap with a computable chance value gets a fraction of the chance-to-ceiling
range; and a quantity with a published absolute bar keeps that bar. The four registrations in
this series therefore anchor differently, and the difference is the metric's, not the design's.

**Thresholds.** H2's criterion is already relative — the circuit against matched random sets
measured in the same run — and stays that way. H1's is not, and is anchored here: matched random
component sets are tracked across the same checkpoints, giving the correlation attainable by a
set that is not the circuit.

**H1 holds** if Spearman ρ for name movers exceeds `ρ(matched random) + 0.25` in all five seeds.
The superseded document fixed 0.90 absolutely; it is retained as a secondary prediction. Four of
five seeds is reported as partial and does not count as holding.

**H2 holds** if ρ ≥ 0.85 and matched random sets fall at most half as far as the circuit.

**H3 holds** if the hysteresis interval excludes zero.

A high onset correlation with a low offset correlation is the outcome that would matter most:
it would mean the coupling is one-directional, which is what the field's evidence base currently
looks like and what this criterion was written to detect.

## Data inclusion and exclusion

All checkpoints and rungs are reported. A checkpoint that fails to load is reported as failed.

## Missing data

Reported as failed with the error, never imputed across the trajectory.

## Other planned analysis

Exploratory and labelled so.

## Context and additional information

**Scope, stated up front and not negotiable.** A result on Stanford CRFM GPT-2 small is a result
about a GPT-2 small architecture trained on OpenWebText. It is not a result about Wang et al.'s
26 heads in OpenAI's GPT-2 small, because that model has no checkpoints and never will.

**Compute.** Forty checkpoints × five seeds, plus a forty-rung ladder. This runs remotely, with
results written per checkpoint so an interrupted run resumes rather than restarts.

---

## Log

Append only. Never edit above the line.

The last column distinguishes an amendment from a deviation: `nothing run`, `no results seen`,
`results not opened`, `results seen`.

```
2026-08-11  created, superseding the 2026-08-05 document   nothing run
```
