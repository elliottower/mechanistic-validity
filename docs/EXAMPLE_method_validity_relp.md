# Worked example: scoring a method paper

**Not part of the audited corpus, and not cited in the paper.** This exists to answer a
question the sixteen audits cannot: what happens when the framework is pointed at a paper
about a *measurement instrument* rather than a paper about a *mechanism*.

The subject is Rezaei Jafari, Eberle, Khakzar and Nanda, "RelP: Faithful and Efficient
Circuit Discovery in Language Models via Relevance Patching", arXiv:2508.21258v2 (30 Oct
2025), PDF at `reference/relp_2025_relevance_patching.pdf`.

## What it claims

Attribution patching estimates the effect of patching a node by a first-order Taylor step:
the finite activation difference dotted with the ordinary local gradient. RelP keeps the
finite difference and replaces the gradient with a layer-wise-relevance-propagation
coefficient, computed by a modified backward pass that detaches the LayerNorm denominator,
linearizes the GELU/SiLU nonlinear factor, and splits relevance evenly across a gate's two
branches. The forward pass is untouched.

The headline, verbatim from the abstract:

> "for MLP outputs in GPT-2 Large, attribution patching achieves a Pearson correlation of
> 0.006, whereas RelP reaches 0.956"

## Why it scores differently from everything in the corpus

**It has a criterion target.** The quantity RelP wants to estimate — the effect of actually
replacing a node and completing the forward pass — is computable, just expensively. So the
paper can report agreement between its estimate and the thing being estimated, and it does,
across eight models in four families: GPT-2 Small/Medium/Large, Pythia-70M/410M,
Qwen2-0.5B/7B, and Gemma2-2B.

Almost nothing in the audited corpus has this. A claim that a set of heads "is the IOI
circuit" names no independently computable quantity that the circuit-discovery procedure is
estimating, so there is nothing to correlate against. That absence is why so many criteria
in the corpus sit at U rather than at I: the measurement cannot fail because there is no
standard it could fail against.

## The ladder walk

| Criterion | Status | Basis |
|---|---|---|
| C1 falsifiability | C | The correlation could have come out at zero, and for the baseline it did — 0.006 |
| C2 structural plausibility | C | Each rule targets a named source of curvature: the normalization statistic, the nonlinear factor of the activation, double-counting through a gate |
| M2 baseline separation | C | Attribution patching is the baseline and the gap is not marginal |
| C3 convergent validity | C | Sparse-feature circuits from RelP and from integrated gradients reach comparable faithfulness by an independent route |
| E4 cross-model generalization | C | Eight models, four families, two orders of magnitude in scale |
| E2 prompt generalization | PC | Self-limited: "relying on predefined original–patch input pairs and single-token prediction metrics", so "circuit discovery was limited to moderately complex behaviors" |
| I4 specificity | PC | The method does not work uniformly, and the paper says so: "gains for attention outputs were smaller" |
| M3 stability | I | Rule selection "introduces some model-specific overhead"; the estimate depends on an analyst choice the paper does not fix |
| V5 scope declaration | C | The limitations section names the rule dependence, the attention weakness, the model scale, and the task simplicity without being asked |

Walking the ladder: C1 and C2 clear Proposed. M2 clears Causally Suggestive. The next rung
asks for sufficiency, intervention reach and specificity, and here the walk stops being
meaningful rather than failing — those criteria ask what an intervention on a *mechanism*
does, and RelP is not claiming a mechanism.

**So the honest answer is that RelP reaches Causally Suggestive and then leaves the ladder,
not because the evidence is thin but because the rungs above it ask questions its claim does
not pose.** That is a limitation of the framework, not a verdict on the paper. The ladder
was built for claims of the form "component X implements behavior Y", and a claim of the
form "estimator A approximates quantity B better than estimator C" runs orthogonal to it.

## What the framework does catch

Two things, and both are real.

**M3 is the live weakness, and it is the same shape as the gauge finding.** The LRP rules
are conventions, not derivations. The half rule in particular — split relevance evenly
across a gate's two branches — is a conservation stipulation with no argument from the
network's computation. The paper concedes rule selection is model-specific. So a number
produced by RelP is a number relative to a rule set, in the same way a J-lens readout is
relative to a backward-pass convention, and in the same way an attention score is relative to
a choice of gauge. Change the convention and the measure moves.

**The attention gap is the part to press.** RelP lists an attention rule that freezes
attention probabilities while propagating through values, and did not use it in the
experiments. Attention outputs are also where the gains are smallest. So attention
attribution is unresolved for both methods, and it is exactly the region a head-level circuit
claim depends on.

## The transfer that must not be made

R-lens applies the same LRP machinery inside the Jacobian lens and argues its early-layer
readouts are more faithful. RelP earns the word "faithful" by measuring against activation
patching. R-lens inherits the machinery without inheriting the criterion: there is no
independently computable answer to what the correct readout at an early layer is, so nothing
anchors the claim that one lens is closer to it. Shared method is not shared validation, and
credibility does not transfer along the axis of borrowed machinery.

This is the general form of an error worth naming: a technique validated against a criterion
in one setting gets reused in a setting where the criterion does not exist, and carries its
reputation across the gap.

## What it would take to score above Causally Suggestive

Nothing the paper omits by oversight. The rungs above ask about mechanism, and a method paper
would have to make a mechanism claim to reach them. The useful adjacent test is the one the
method makes cheap: rank a circuit with attribution patching, integrated gradients and RelP,
then evaluate each ranking by actual patching rather than by the score that produced it. If
the three select different circuits at comparable faithfulness, that is evidence for
underdetermination of the mechanism, which is a claim the ladder *can* score.
