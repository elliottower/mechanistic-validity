# Does the IOI effect survive name-frequency and sequence-length controls?

**Status:** DRAFT — not frozen.

Sections use the [OSF Preregistration](https://osf.io/prereg/) question titles verbatim. A
question that does not apply is answered **N/A** with the reason, never deleted.

## Research questions or hypotheses

The IOI task draws names from a fixed list of 100 common English first names, selected on one
stated criterion: that each is a single token. Nothing controls how *frequent* those tokens are
in training data. If the measured circuit tracks token frequency rather than the indirect-object
computation, the mechanism attributed to it is partly an artifact of the stimulus set.

**H1.** Behaviour is confounded and the mechanism is not: stratifying names by corpus frequency
moves the logit difference well beyond what random band assignment produces, while circuits
extracted within each band transfer across bands about as well as they transfer within one. A
previous version fixed 0.5 nats and 90%; both are retained as secondary predictions.

**H2.** Accuracy in the adversarial cell — rare names in the indirect-object position, common
names as subject — stays above 70%.

H1 is the prediction worth staking. It says the *task* is confounded while the *circuit* is not,
which is a specific and falsifiable division rather than a claim that everything is fine.

## Foreknowledge of data or evidence

**A previous pre-registration exists**, frozen 2026-08-05 at commit `c643450` of the predecessor
repository. It has not been run. One of its claims was wrong and is corrected here:

- It stated that no published test of the **length** confound was located. Wang et al. §4.4 run
  one: *"To ensure that the observed effect is not an artifact of the additional sentences, we
  included a control dataset using the same templates, but where the middle sentence contains S
  instead of IO."* It is behavioural only, one added sentence, with no circuit measurement — but
  it exists, and the claim as written was false.

Also relevant:

- **Anani et al. (arXiv:2602.22968)** evaluate GPT-2 small IOI circuits on longer prompts with
  distractors, though length is confounded with distractor content and there is no graded curve.
- **Rai et al. (arXiv:2605.09129)** build an IOI filler variant, but the filler contains the IO
  name, making it a double-IO manipulation rather than a length control.
- **Bayat Makou et al. (arXiv:2606.06267)** run the frequency-band design — four token-frequency
  bands, cross-band circuit transfer — on Literal Sequence Copying across five Pythia scales,
  and extend it to sequence length in their Appendix I. It is the closest prior work and the
  design here is the same shape applied to a semantic task.
- **ronakrm** brute-forced Wang's stimulus space and found *"1.348%, or about 125,000 out of the
  ~9 million sentences"* where GPT-2 prefers the subject, with failures concentrating on
  particular names. He speculates about rarity without measuring frequency.

**The frequency arm has no prior.** Two metadata sweeps returned nothing crossing IOI with token
frequency, and `frequen` occurs zero times in Wang et al.

**No frequency or length quantity has been computed by us.**

## Explanation of foreknowledge and managing unintended influences

Wang's §4.4 control and ronakrm's 98.7% ceiling both bear on H2's 70% threshold, and both were
found after that threshold was set in the superseded document. It is carried unchanged, and the
98.7% ceiling is now cited as what it is stated against.

H1's two numbers, 0.5 nats and 90%, had no derivation at all. They are replaced by criteria
anchored to nulls this study measures, with the originals retained as secondary predictions.

Bayat Makou et al.'s result on a different task is the reason H1 predicts transfer rather than
failure; that influence is declared rather than hidden.

## Study type

Experimental. Stimulus properties are manipulated.

## Intention for causal interpretation

Yes, for the confound: whether frequency causes the measured effect.

## Blinding of experimental treatments

N/A — no human judgement enters.

## Additional blinding during research or analysis

N/A.

## Study design

**Frequency arm.** Name tokens are binned into four frequency bands by their count in an
OpenWebText sample. Prompts are generated per band, plus an adversarial cell pairing rare names
in the IO position with common names as subject. Circuits are extracted within each band and
evaluated across bands.

**Length arm.** A graded ladder of name-free, pronoun-free filler sentences inserted between the
setup and the final clause, so length varies while the entities do not. Wang's §4.4 control
varies content as well as length; this one does not.

A syntax-stripped control appears in neither the literature nor here, and is named as a gap
rather than claimed.

## Randomization

Prompt generation and band assignment use a seed fixed here before any run: `0`.

## Data collection procedures

Wang et al.'s templates and name list. Token frequencies counted from an OpenWebText sample
whose size and commit are recorded at freeze.

## Data collection procedures - File upload

N/A.

## Sample size

1,000 prompts per frequency band, 1,000 per length rung.

## Sample size rationale

The frequency contrast is a difference in mean logit difference; 1,000 per band gives a
bootstrap interval narrow enough to separate 0.5 nats from 0.2. Cross-band transfer is a ratio
of faithfulness scores and is noisier, which is why it is judged against a within-band transfer
null rather than against a fixed fraction. 200 random band assignments give the frequency null a
spread estimate stable enough to multiply.

## Starting and stopping rules

**Gate 1: the frequency proxy must be self-consistent.** It must correlate with itself across
two disjoint corpus samples at Spearman ρ > 0.9. A proxy that is not self-consistent cannot
support the arm, and that outcome is reported rather than worked around.

**Gate 2: the design must be able to resolve its own criterion.** The frequency null — 200
random band assignments — is computed **first**, before the real band contrast. If the bootstrap
interval on the contrast at 1,000 prompts per band is wider than `2 × sd` of that null, the
design cannot distinguish a result at the criterion from one below it. Either the sample size
rises until it can, or the study reports that the criterion is unresolvable at available compute.
Both outcomes are recorded in the log.

Computing the null first is safe: random band assignment reveals nothing about the real
contrast. Choosing the sample size after seeing the real contrast would not be.

## Manipulated variables

Name-token frequency band; filler length; the adversarial frequency-by-role pairing.

## Measured variables

Logit difference and accuracy per cell; circuit faithfulness within band; cross-band transfer
as the ratio of cross-band to within-band faithfulness; per-head direct logit attribution
across the length ladder.

## Measured variables - File upload

N/A.

## Indices

Cross-band transfer ratio. No other composite.

## Indices - File upload

N/A.

## Statistical models

None fitted. Bootstrap over prompts, 1,000 resamples.

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

**Thresholds are anchored to nulls this study measures**, not asserted. Two nulls are computed
before any contrast is inspected:

- **Frequency null.** Names are assigned to bands at random, ignoring frequency, and the same
  contrast computed. Repeated 200 times, this gives the spread of a frequency effect that is
  not one.
- **Transfer null.** Circuits are extracted from two disjoint halves of the *same* band and
  transferred between them, giving the transfer ratio attainable when nothing differs.

**H1 holds** if the frequency contrast exceeds `5 × sd` of the frequency null, *and* the lower
bound on cross-band transfer exceeds the within-band transfer null's lower bound minus 0.05.
The superseded document fixed 0.5 nats and 0.90 absolutely with no derivation; both are retained
as secondary predictions.

**H2 holds** if adversarial-cell accuracy exceeds 70%. This one stays absolute: ronakrm's
brute-force sweep of Wang's stimulus space found GPT-2 preferring the subject on 1.348% of ~9
million sentences, so the unadversarial ceiling is near 98.7%, and 70% is a floor stated against
that published number rather than against a null.

A frequency effect on behaviour with transfer *below* 0.90 is the interesting failure: it would
mean the circuit itself is frequency-specific, and it is reported as such rather than as a null.

## Data inclusion and exclusion

All bands and all rungs are reported. Names that fail the single-token requirement in GPT-2's
tokenizer are excluded before generation, and the count is reported.

## Missing data

A cell that fails to compute is reported as failed with the error.

## Other planned analysis

Exploratory and labelled so.

## Context and additional information

**What no outcome licenses.** One task, one model, one name list. A frequency effect here says
nothing about whether other circuit claims are frequency-confounded, though it would raise the
question for any task built from a hand-made word list — which is most of them.

---

## Log

Append only. Never edit above the line.

The last column distinguishes an amendment from a deviation: `nothing run`, `no results seen`,
`results not opened`, `results seen`.

```
2026-08-11  created, superseding the 2026-08-05 document   nothing run
```
