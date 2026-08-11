# Pre-registration: closing five unmet criteria on GPT-2 small

Frozen before any experiment is run. Predictions below are committed; results are not
consulted until this file's hash is recorded.

## Why these five

The audit of sixteen published claims leaves some criteria unmet across the whole set. Two
rankings pick out the same ones, and neither is a judgment call:

| criterion | claims whose next tier it blocks | attempted in |
|---|---|---|
| I6 double dissociation | 7 of 16 | 1 of 16 |
| I4 specificity | 5 of 16 | 14 of 16 |
| E1 intervention reach | 3 of 16 | 14 of 16 |
| M7 selection correction | — | 0 of 16 |
| I10 rescue reversibility | — | 3 of 16 |

I8 (confounding sensitivity) is deliberately excluded. The framework motivates it as
residual-stream information correlated with both the ablated component and the output,
which is a real threat, but the instrument it names — VanderWeele and Ding's E-value —
assumes an observational effect estimate. An ablation is an intervention, so the E-value's
bias model does not apply. Whether I8 has a well-formed interventional analogue is a
question for the framework, not an experiment to run. Recorded here so the omission is not
read as an oversight.

## System

GPT-2 small throughout, so every result is comparable and no cross-model transfer is
assumed. Two published circuits on that model serve as the pair the dissociation needs:
the IOI circuit (Wang et al., 26 heads in seven classes) and the greater-than circuit
(Hanna et al., attention heads plus MLPs 8–11). Both are audited claims in the paper, so a
result here changes a verdict in it.

## E1 — Double dissociation (criterion I6)

**Design.** Ablate the IOI circuit and measure both the IOI logit difference and the
greater-than probability difference. Ablate the greater-than circuit and measure both.

The ablation value is the design's weak point and is fixed here rather than left to each
task's convention. IOI's ABC distribution substitutes random names inside otherwise
identical templates; greater-than's 01-distribution substitutes a fixed numeric floor into
a digit slot. Those are different interventions with different statistical properties — one
averages over discrete categorical draws, the other is a single fixed value — so using each
task's native corruption would confound the dissociation with the corruption mechanism.
Miller et al. show that unstated choices of exactly this kind move faithfulness by tens of
percentage points, which is enough to manufacture or erase a crossing.

The criterion is therefore decided on **symmetric ablations only**, each applied identically
to both circuits:

| condition | value | role |
|---|---|---|
| Z | zero-ablation | primary; involves no distribution choice at all |
| R | resample from a shared pool of natural-text activations | primary; same pool for both circuits |
| N | each task's native corruption (ABC, 01) | reported, not decisive; the asymmetry is named |

**Prediction, committed.** In both Z and R, each ablation damages its own task more than the
other, and the interaction crosses.

**Success.** The crossing holds in Z and in R. In each, both simple effects run in the
predicted direction and the crossing survives a permutation test on task labels at p < 0.01
over at least 1000 permutations. Condition N is reported alongside; agreement with Z and R
is evidence the native corruptions are interchangeable here, and disagreement is a result
about the corruptions rather than about the circuits.

**What refutes it.** Either ablation damaging both tasks comparably. That would mean the
two circuits share a resource the component lists do not name, which is the outcome I6 is
built to detect and the reason one arm cannot substitute for two.

**Reported either way.** A failed dissociation is the informative result here, not a null
to be dropped.

## E2 — Held-out estimate of a selected effect (criterion M7)

Copy suppression carries two separately selected numbers, and they need separate treatments
because only one of them is measured by a procedure that survives being moved off the
selected slice.

### E2a — the behavioural figure on an unselected sample

**Design.** The 80% figure counts completions meeting the source paper's three qualitative
copy-suppression conditions, evaluated on a sample drawn from the top 5% of completions by
L10H7's own effect. Apply the same three conditions, unchanged, to a random sample of
completions drawn without reference to the head's effect, and to a stratified sample across
effect deciles.

**Prediction, committed.** The proportion meeting the three conditions on the unselected
sample is lower than 80%. Direction committed, magnitude not.

**Success.** Three proportions with intervals: the original top-5% sample, a random sample,
and the decile-stratified sample. The gap between the first two estimates the winner's
curse for this figure.

**What refutes the concern.** The three agreeing within their intervals, showing the
selection buys nothing here.

### E2b — CSPA fidelity as a function of the threshold

**Design.** CSPA's top-k% filter is structural rather than incidental: the method preserves
attention to the highest-probability predicted source tokens and deletes the rest, so
evaluating it on the complementary 95% would invert what the measurement is defined to
keep. Instead sweep k over 1, 5, 10, 25, 50 and 100%, holding every other element of CSPA
fixed, and report recovered KL divergence as a function of k.

**Prediction, committed.** Recovered fidelity increases monotonically in k, and the
published k = 5% sits below the k = 100% value.

**Success.** The full curve reported, with the value at the published threshold marked. The
distance from k = 5% to k = 100% is the quantity M7 asks for: how much of the reported
score belongs to the threshold rather than to the head.

**What refutes the concern.** A flat curve, which would show the threshold is doing no work
and that the published figure is threshold-independent.

**Note on scope.** E2b measures the threshold's contribution, not an unbiased re-estimate.
No procedure recovers the latter without redefining CSPA, and redefining a source paper's
metric is outside what this audit does.

## E3 — Rescue reversibility (criterion I10)

**Design.** Ablate each IOI head class, then restore it from the cached clean activations,
and measure recovery. Then restore k of n heads for k = 1..n to trace the recovery curve.

**Prediction, committed.** Full restoration returns the logit difference to baseline within
numerical tolerance. The partial curve is monotone in k.

**Success.** Full-restoration recovery within 1% of baseline; monotonicity of the partial
curve reported with the exceptions named if any.

**What this rules out.** A non-monotone or incomplete recovery would show the ablation
perturbs the network in ways the component list does not capture, which bears on every
faithfulness number computed by ablation.

## E4 — Matched control tasks (criterion I4)

**Design.** Ablate the IOI circuit under conditions Z and R and measure on controls that
exist independently of this study. Shares runs with E1.

Controls divide by who constructed them, because a specificity claim checked only against a
control its own authors designed has no anchor:

- **Published.** Greater-than (Hanna et al.), a task on the same model with its own
  circuit and its own literature.
- **Unconstructed.** Next-token prediction on held-out natural text, which requires no
  design choices and has a baseline that exists whether or not this study runs.
- **Constructed, reported but not decisive.** A two-name recall task with no indirect
  object. No published task of this shape with an established baseline exists, so it would
  be a control designed by the people making the claim it tests. It is specified in advance
  — same templates as the IOI set with the indirect-object clause removed, same name pool,
  same answer-set size — and reported, but the criterion does not turn on it.

**Prediction, committed.** The IOI deficit exceeds the deficit on both independent controls.

**Success.** Both independent contrasts in the predicted direction with non-overlapping
intervals, in Z and in R. The constructed control is reported with its result either way.

**What refutes it.** Either independent control damaged as much as IOI, which would place
the circuit's specificity in question regardless of its faithfulness.

## E5 — Intervention reach (criterion E1)

**Design.** Miller et al. define faithfulness over a six-tuple of methodological choices —
granularity, component type, ablation value, token positions, direction, and whether the
circuit or its complement is ablated — and vary them jointly. This varies **ablation value
alone** and fixes the other five at the origin paper's own settings:

| dimension | held at |
|---|---|
| granularity | (head, position) pairs, as Wang et al. specify them |
| component type | attention heads only; no MLPs, no layer norms |
| token positions | the position assignment published for each head class |
| direction | ablate the complement, measuring whether the circuit alone suffices |
| circuit set | the published 26 (head, position) pairs, unmodified |
| **ablation value** | **varied: zero, mean over ABC, resample from ABC, Gaussian noise** |

**Prediction, committed.** The four values disagree by more than 10 percentage points of the
full model's logit difference.

**Success.** All four reported together with the spread as the headline, and the five fixed
dimensions restated alongside so the number is interpretable.

**Relation to prior work.** Miller et al. establish that the six-tuple jointly produces a
range from below 0% to above 100%. This decomposes one axis of that tuple rather than
reproducing the joint result, so it answers a question their design does not separate:
how much of the spread is the ablation value alone. Their paper is the source of the
six-tuple and is cited as such.

## Analysis rules, committed

- No result is inspected before this file's hash is recorded.
- Every effect is reported with an interval; no point estimate stands alone.
- Failures are reported in the same detail as successes, including E1 failing to cross.
- Any deviation from this document is recorded as a deviation, with its reason, rather than
  silently adopted.
- Sample sizes: 1000 prompts per task per condition unless a task's input space is smaller,
  in which case it is enumerated and the enumeration is stated.

## What changes in the paper if these run

E1 closing would move up to seven claims off their I6 block, and would be the second double
dissociation in the audited set. E2 would put a number on the winner's curse the framework
asserts. E3 and E5 turn two Untested criteria into measured ones for IOI. None of the five
changes the framework; each changes a cell in the audit, which is the point.

## Revision record

One revision, made before any experiment was run and before the hash below was treated as
binding. External review of the first draft found two defects, both in the direction of
under-specification rather than over-claiming.

E2 originally proposed recomputing CSPA on the completions the published figure excludes.
That inverts what the measurement preserves: CSPA is defined to keep attention to the
highest-probability predicted source tokens and delete the rest, so running it on the
complement measures the discarded mass rather than providing a held-out estimate of the
published quantity. E2 is now split — E2a moves the behavioural figure's three conditions
onto an unselected sample, which they survive, and E2b sweeps CSPA's threshold, which
leaves the metric intact.

E5 originally said "everything else fixed" without saying what "everything else" was, which
is the precise failure Miller et al. exist to demonstrate. The five fixed dimensions and
their values are now tabulated.

Second revision, same conditions: before any run, after external check.

E1 specified mean-ablation "over the task's own corruption distribution" in both arms. Those
are not one procedure applied twice. IOI's ABC substitutes random names within otherwise
identical templates and averages over discrete categorical draws; greater-than's 01
substitutes a fixed numeric floor into a digit slot and averages over nothing. Running each
arm under its own corruption would confound the dissociation with the corruption mechanism,
and by Miller et al.'s own result that confound is large enough to manufacture a crossing or
erase one. The criterion now rests on two symmetric ablations applied identically to both
circuits, with the native corruptions reported as a third, non-decisive condition.

E4 counted a self-constructed two-name control toward the criterion. No published task of
that shape with an established baseline exists, so the control would have been designed by
the same people making the claim it tests. Controls are now split by provenance: the
criterion turns on greater-than and on natural-text next-token prediction, both of which
exist independently of this study, and the constructed task is specified in advance and
reported without bearing on the verdict.

Superseded hashes, recorded so the revisions are auditable:
961f1d0f91d34ba28c1e5cade52add3549ab48e31dd908d82f682526e94b3189
61a78fad62e45549db37fb136b9678c517b331fd6753be2c9d4f73c5ca561224

---

# Amendment 1 — post-hoc, added after E1 returned

Everything above this line was frozen before any experiment ran. Everything below was
written **after seeing E1's result** and must be read as post-hoc. It is recorded here
rather than folded into the design so that no reader can mistake it for the registered
analysis.

## What E1 returned

At the registered n = 1000 with 1000 permutations, the criterion was **not met**. The
crossing held under zero-ablation (p = 0.001) and failed under resample-ablation
(p = 0.061), and the registered success condition required both.

## Why the result is not yet interpretable

The failing arm is that ablating the greater-than circuit damages IOI more than it damages
greater-than. Post-ablation scores make the reason visible in a way deficits do not:

| condition | ablated | measured | post-ablation |
|---|---|---|---|
| zero | ioi | ioi | −0.143 |
| zero | greater-than | ioi | +0.119 |
| resample | ioi | ioi | −0.160 |
| resample | greater-than | ioi | −0.151 |

Two things are confounded here and the design cannot separate them.

**Saturation.** Under zero-ablation the own-circuit intervention already drives IOI below
zero, so resample has no room to move it. A comparison of own-circuit and cross-circuit
sensitivity to ablation value therefore favours the cross-circuit arm by construction, and
that comparison cannot be used to argue for a shared resource.

**Component type.** The IOI circuit is 26 attention heads and no MLPs. The greater-than
circuit is 7 attention heads and MLPs 8 through 11. Resample-ablating four whole MLP layers
replaces a third of the model's MLP computation with activations from unrelated text, which
is a categorically larger intervention than resample-ablating 26 attention heads. The two
arms are not comparable, and component type is one of the six dimensions Miller et al.
identify. The pre-registration fixed the ablation-value asymmetry between the two arms and
did not notice the component-type asymmetry sitting beside it.

E1 as registered is consistent with a shared resource the component lists do not name, and
equally consistent with having ablated four MLPs on one side and none on the other. No
reading of it is licensed until those are separated.

## E1c — heads-only control, post-hoc

**Design.** Repeat E1 with the greater-than circuit reduced to its seven attention heads
and no MLPs, so both arms ablate attention heads only. Everything else is unchanged,
including seed, prompts, conditions and the permutation test.

**What each outcome would mean.** A crossing that returns under resample places the
registered failure on the component-type asymmetry, which is a defect in the design rather
than a property of the circuits. A crossing that stays broken leaves the shared-resource
reading standing against its first real test, though standing is not the same as supported.

**Status.** Post-hoc and prompted by a failure, so it cannot confirm anything. It can only
remove one explanation. Reported with that limit stated either way.

## A claim held back

No published double dissociation is known to flip under ablation choice; the existing
result in this area concerns single faithfulness scores. If E1's flip survives E1c it is
therefore a claim about a criterion rather than a metric, which would be new. It is held
entirely until then, and this paragraph records that it was available and not made.

Superseded hash, this amendment appended after it:
1d662b6ff7ef630e7769e7d710ec4a451f1810e251f3819aca4171669b369f31
