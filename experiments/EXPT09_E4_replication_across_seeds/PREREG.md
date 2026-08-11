# Is the IOI circuit a property of the architecture, or of one training run?

**Status:** DRAFT — not frozen.

Sections use the [OSF Preregistration](https://osf.io/prereg/) question titles verbatim. A
question that does not apply is answered **N/A** with the reason, never deleted.

## Research questions or hypotheses

"The IOI circuit in GPT-2 small" is spoken of as a fact about the architecture. It has only ever
been measured in one training run. Stanford CRFM released five GPT-2 small runs differing only
in random seed, on the same corpus with the same recipe, which makes the question answerable.

Run one fixed extractor over all five, take the top-26 heads from each, and compare.

**H1.** Mean pairwise Jaccard across the ten seed pairs reaches at least half the distance from
chance (0.099, computed) to the within-seed ceiling this study measures. A previous version
predicted 0.45 absolutely, retained below as a secondary prediction.

**H2.** That mean sits at least 0.10 below the within-seed bootstrap ceiling — the overlap
attainable when the seed is fixed and only sampling varies.

**H3.** At most 30% of head coordinates are shared by all five seeds.

Together these say roles replicate and coordinates do not. If H1 fails and the mean approaches
0.099, the circuit is a property of one run and every paper built on those 26 heads inherits
that.

## Foreknowledge of data or evidence

**A previous pre-registration exists**, frozen 2026-08-05 at commit `c643450` of the predecessor
repository. It has not been run. It contains two errors, corrected here:

- It attributed to Méloux et al. the sentence *"variation is over data resamples and
  hyperparameters, not over training seeds."* **That sentence does not appear in the paper** —
  the string "seed" occurs zero times in arXiv:2510.00845. The substance is right; the
  quotation was fabricated. No quotation is attributed to that work here.
- It stated that two edge-attribution variants overlap at 0.071 *"on GPT-2 small IOI."* The
  figure is real but belongs to **Llama-3.2-1B-Instruct** — it sits under Table 2, captioned
  *"Hyperparameter sensitivity in Llama-3.2-1B-Instruct."* Since that number was the stated
  justification for using a single extractor, the justification is restated below without it.

Also relevant, and absent from the superseded document:

- **Xu (arXiv:2605.24059)** ran six pretraining seeds of a 51M TinyStories model on a
  key-retrieval probe and reports *"all six implement it with different attention heads,"* plus
  a cross-seed ablation-transfer matrix. Its own limitations name the natural-text case as
  untested.
- **Bali et al. (arXiv:2602.16740)** ask *"if two different teams use the same LLM architecture
  and the same data, do they end up with the same attention heads?"* and train GPT-2 small
  refits on OpenWebText. Their measure is within-layer cosine similarity of attention patterns,
  not task-circuit overlap.
- **Gurnee et al. (arXiv:2401.12181)** use these same five Stanford models for the same question
  one level down, finding 1–5% of neurons universal.
- **Nanda's open problem 2.17** (December 2022) proposes this study verbatim and has stood open
  since.
- **Tigges et al. (arXiv:2407.10827)** does *not* bear on this: the word "seed" occurs zero
  times in it. It varies training time and parameter count.

**Nothing about cross-seed head overlap has been computed by us.**

## Explanation of foreknowledge and managing unintended influences

The superseded document fixed 0.45, 0.10 and 30% absolutely, with no derivation. This version
anchors H1 to chance and to the ceiling it measures, and keeps 0.45 as a secondary prediction so
the inherited number is checked rather than discarded. H3's 30% remains absolute and is the
weakest of the three.

Xu's toy-scale result points against H1. Stating that here rather than adjusting the threshold
is the point of the section.

## Study type

Observational. Nothing is manipulated; the seeds already differ.

## Intention for causal interpretation

N/A. This measures agreement between extractions, not an effect.

## Blinding of experimental treatments

N/A — no treatments.

## Additional blinding during research or analysis

N/A — one extractor with fixed hyperparameters is applied identically to every model.

## Study design

Five models, one extractor, top-26 heads each, ten pairwise comparisons.

**A single extractor is used deliberately.** Mixing extraction methods would inject method
variance into a seed comparison, and edge-attribution variants are known to disagree sharply
with one another. The cost is that every number below is extractor-relative, which is stated
rather than assumed.

**Standing check on the extractor.** On the reference model the top-26 must overlap Wang et
al.'s published 26 well above chance. If it does not, the attribution is broken and no
cross-seed number means anything. The heads it misses are expected to be early ones —
duplicate-token, previous-token, induction — because those act on the logits through
S-inhibition rather than directly, and node attribution measures direct effect.

**The OpenAI GPT-2 small comparison is confounded** — it varies seed, corpus and recipe
together — and is reported separately and labelled as such.

## Randomization

Bootstrap resampling for the within-seed ceiling uses a seed fixed here before any run: `0`.

## Data collection procedures

The five Stanford CRFM runs (`alias-x21`, `battlestar-x49`, `caprica-x81`, `darkmatter-x343`,
`expanse-x777`), the MIB IOI dataset, and integrated-gradients node attribution over attention
head outputs.

## Data collection procedures - File upload

N/A.

## Sample size

500 IOI prompts per model. 100 bootstrap resamples for the within-seed ceiling.

## Sample size rationale

Méloux et al. measure a within-model bootstrap Jaccard of 0.67 for GPT-2 small IOI over 100
resamples. Matching that resample count makes the ceiling here comparable to theirs. 500
prompts is set by compute rather than by power, and the consequence — a wide interval on any
single pairwise Jaccard — is why H1 is stated over the mean of ten pairs.

## Starting and stopping rules

**Gate 1: the extractor must work.** The check described above runs first and is reported
whatever it returns. If the top-26 does not overlap Wang et al.'s published 26 well above
chance on the reference model, no cross-seed number means anything and the study stops there.

**Gate 2: the ceiling must leave room for the criterion.** H1 is stated as a fraction of the
distance from chance to the within-seed ceiling, and that ceiling is unknown until measured. It
is computed **first**. If it falls below 0.30 — leaving less than 0.20 of range above chance —
the criterion cannot separate a stable circuit from an unstable one, and the study reports the
ceiling itself as the finding. A low ceiling would mean the extractor is unstable under
resampling alone, which is a result about the method rather than about seeds.

Computing the ceiling first is safe: it uses one model resampled, and reveals nothing about
agreement between models.

All five models and all ten pairs then run to completion.

## Manipulated variables

N/A — the seeds differ as released.

## Measured variables

Pairwise Jaccard between top-26 head sets; the within-seed bootstrap Jaccard; the count of
coordinates shared by all five; and per-model task accuracy and logit difference, so a model
that cannot do the task is visible rather than silently averaged in.

## Measured variables - File upload

N/A.

## Indices

Mean pairwise Jaccard across the ten seed pairs.

## Indices - File upload

N/A.

## Statistical models

None fitted. Bootstrap intervals only.

## Statistical models - File upload

N/A.

## Transformations

None.

## Inference criteria

Chance Jaccard for two independent 26-of-144 sets is 0.099, computed rather than assumed, and
recomputed in the analysis rather than taken from this document.

**Why the anchor takes this form.** The anchor follows the metric's scale rather than a house
style. An unbounded contrast gets multiples of its null's standard deviation; a bounded
correlation gets an additive margin, because sd-scaling a quantity capped at 1.0 distorts near
the ceiling; a set overlap with a computable chance value gets a fraction of the chance-to-ceiling
range; and a quantity with a published absolute bar keeps that bar. The four registrations in
this series therefore anchor differently, and the difference is the metric's, not the design's.

**Thresholds are anchored to the two quantities this study measures**, not asserted between
them. Chance is 0.099, computed. The within-seed bootstrap ceiling is measured in H2. The
cross-seed mean is then read as a fraction of the range between them.

**H1 holds** if the mean pairwise Jaccard reaches at least half the distance from chance to the
measured within-seed ceiling. The superseded document fixed 0.45 absolutely with no derivation;
that value is retained as a secondary prediction.

**Below 0.20 the circuit is a property of the run**, and that reading is committed here so it
cannot be softened later. 0.20 is roughly twice chance and is stated as an absolute floor
because a value that close to chance needs no ceiling to interpret.

Méloux et al. propose a mean pairwise Jaccard above 0.8 under bootstrap resampling as a
stability bar. That is a *bootstrap* bar; H2 repurposes it as a cross-seed comparison, which is
a different use and is flagged as such.

## Data inclusion and exclusion

All five models are reported. A model failing the task is reported, not dropped.

## Missing data

A model that fails to load or extract is reported as failed with the error.

## Other planned analysis

Functional-class persistence across seeds — whether the *roles* recur even when coordinates do
not — needs behavioural head classification that is not implemented, and is not part of this
registration.

## Context and additional information

**Downloads.** Five models at roughly 500MB each. This runs remotely.

**What no outcome licenses.** Five seeds of one architecture on one corpus. A high Jaccard does
not establish universality; a low one does not establish that circuits are always run-specific.

---

## Log

Append only. Never edit above the line.

The last column distinguishes an amendment from a deviation: `nothing run`, `no results seen`,
`results not opened`, `results seen`.

```
2026-08-11  created, superseding the 2026-08-05 document   nothing run
```
