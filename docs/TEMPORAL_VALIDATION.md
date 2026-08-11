# Temporal Validation of Mechanistic Interpretability Claims

**Method.** Modeled on the ClinGen retrospective re-curation exercise, which re-simulated 30
gene–disease validity curations at one-year increments from first publication using only the
evidence available at each date. ClinGen's result: of 8 associations that sat at a low
classification tier for five or more years, 3 were later reclassified Disputed or Refuted.

The analogous question here: **do mechanistic interpretability claims reach their strongest
asserted form faster than the evidence justifies, and does later work contradict them?**

For each of fifteen claims drawn from the case-studies table of
`docs/paper/mechanistic_validity_v11.tex` (`tab:case-studies`), this document records:

1. **Origin** — paper, date, the claim as stated, the evidence it rested on.
2. **Timeline** — later work classified strictly as *supports*, *qualifies*, or *contradicts*.
3. **Turning points** — dates at which the available evidence would have changed an assessment.
4. **Current state** versus origin.

**Conventions.**

- Dates are the **earliest public version**. arXiv v1 dates are used in preference to conference
  publication dates, and the choice is stated per entry.
- *Supports* = independent evidence for the claim as originally scoped.
  *Qualifies* = the claim survives but with narrower scope, added conditions, or a weaker
  effect than originally reported.
  *Contradicts* = a direct empirical conflict with the claim as originally scoped.
  *Silent* = no follow-up found. Reported explicitly, never inferred from absence of effort.
- No verdicts and no tier assignments are issued here. This document records dated evidence only.

**Status markers.** `[COMPLETE]` = timeline researched and written. `[PARTIAL]` = some evidence
gathered, gaps noted inline. `[NOT YET RESEARCHED]` = not reached.

---

## 1. Grokking / Fourier mechanism for modular addition — [COMPLETE]

*Source: `docs/GROKKING_EVIDENCE.md`, quotes verified against source texts archived in
`docs/grokking_sources/`.*

### Origin

**Nanda, Chan, Lieberum, Smith & Steinhardt, "Progress Measures for Grokking via Mechanistic
Interpretability," arXiv:2301.05217, 2023-01** (arXiv v1; ICLR 2023 followed).

Claim: a one-layer ReLU transformer trained on modular addition (`p = 113`) implements a
**Fourier multiplication algorithm** — token embeddings sparse in the Fourier basis, the MLP
composing `cos(w_k(a+b))` and `sin(w_k(a+b))` via trigonometric identities, logits dominated by a
few key frequencies. Every weight-matrix entry is predicted in closed form. Progress measures
derived from the mechanism track a three-phase training trajectory (memorization → circuit
formation → cleanup).

Evidence at origin: closed-form weight analysis, key-frequency ablation, excluded-loss and
restricted-loss progress measures, and a robustness appendix over data fractions, depths, moduli,
regularizers, and seeds.

**A distinction the origin paper itself makes, which most citations lose.** The paper's generality
statement is "every model trained with weight decay **and that generalizes correctly** implements
some variation of the Fourier multiplication algorithm" (Appendix C.2.3). The antecedent is
*generalization*, never *grokking*. Later usage bundled the delayed-generalization phenomenon with
the mechanism into a single object, "the grokking circuit."

### Timeline

**Prior art (before origin), which the origin paper builds on:** Power et al., arXiv:2201.02177
(2022-01), discovers grokking; Liu, Michaud & Tegmark "Omnigrok," arXiv:2210.01117 (2022-10),
attributes it to weight-norm travel time; Gromov, arXiv:2301.02679 (2023-01, one week before
Nanda et al.), gives an analytic Fourier solution for a two-layer quadratic MLP.

| Date (arXiv v1) | Work | Direction | What it showed |
|---|---|---|---|
| 2023-01 | **The origin paper's own appendix** | **qualifies (self)** | At ≥60% training data and at `p = 401`, models **generalize immediately without grokking** and still implement the Fourier circuit (Table 5: 70%-data run has logit FVE 99.0%). §5.2 states "the circuit is formed well before grokking occurs." Grokking is not necessary for the mechanism, and the paper says so. |
| 2023-01 | Same appendix, dropout runs | **qualifies (self)** | Dropout `p=0.2` models grok and generalize, yet Gini(W_E) is 0.19–0.20 against 0.55–0.80 elsewhere, logit FVE 71–74%. Classified as "some variation of the Fourier algorithm" — a classification the reported statistics do not force. |
| 2023-02 | Chughtai, Chan & Nanda, arXiv:2302.03025 | **qualifies** | Group composition via representations, with the strong claim disclaimed up front: "compelling evidence for weak universality, but against strong universality." |
| 2023-06 | **Zhong, Liu, Tegmark & Andreas, "The Clock and the Pizza," arXiv:2306.17844** | **contradicts (uniqueness)** | Modular addition admits at least three solution families in the same architecture class. Pizza uses `\|cos(w_k(a-b)/2)\| cos(w_k(a+b-c))` where Clock uses `cos(w_k(a+b-c))`. On their Model A, Clock explains ~75% of logit variance, Pizza ~99%. Non-circular solutions (1D lines, 3D Lissajous curves) also occur, more often at depth. A width-1024 model at **attention rate 1** — real attention, Nanda et al.'s own family — implements Pizza. |
| 2023-09 | Varma, Shah, Kenton, Kramár & Kumar, arXiv:2309.02390 | **supports (timing only)** | Circuit efficiency: weight decay eventually prefers the generalizing circuit. Indifferent to what the circuit computes. |
| 2023-10 | Kumar, Bordelon, Gershman & Pehlevan, arXiv:2310.06110 | **supports (timing only)** | Lazy-to-rich transition; small laziness `α` eliminates grokking entirely. "our results subsume past work on grokking." Also contradicts the circuit-efficiency account on parameter norm. Says nothing about which algorithm. |
| 2023-10 | Levi, Beck & Bar-Sinai, arXiv:2310.16441 | **qualifies (the phenomenon)** | In a linear teacher-student setting, losses are pure exponentials with no phase structure; the apparent transition is produced by thresholding a smooth curve. A memorization-to-understanding transition is not required to produce a grokking-shaped curve. |
| 2023-11 | **Morwani, Edelman, Oncescu, Zhao & Kakade, arXiv:2311.07568** | **supports (strongest)** | Theorem 7: for one-hidden-layer quadratic networks with `m ≥ 4(p-1)`, any max-`L_{2,3}`-margin network has every neuron 1-sparse in frequency space with `θ_u + θ_v = θ_w`. Non-Fourier interpolating solutions exist and are excluded **by margin**, not by expressivity. Derives the mechanism without invoking the delay. |
| 2023-12 | Stander, Yu, Fan & Biderman, arXiv:2312.06581 | **contradicts (adjacent claim)** | Coset circuits for S5/S6 permutation composition where representation-theoretic composition was reported. Does **not** extend to modular addition — the coset algorithm is degenerate for cyclic groups of prime order. |
| 2024-05 | Lee, Kang, Choi & Cho, "Grokfast," arXiv:2405.20233 | **qualifies (timing)** | Gradient low-pass filtering accelerates grokking up to 50x. On MNIST the delay is nearly abolished *and final accuracy improves* (89.5% → 91.5%) — awkward for any account in which the delay is intrinsic to finding structure. Endpoint mechanism not measured; the authors explicitly decline to claim the endpoints match. |
| 2025-01 | Prieto et al., arXiv:2501.04697 | **qualifies (timing)** | Softmax Collapse under naive loss minimization; grokking removable by perpendicular gradient updates. Mechanism not measured. |
| 2025-06 | Notsawo, Dumas & Rabusseau, arXiv:2506.05718 | **qualifies (timing)** | Grokking is induced by small regularization of *any* property the generalizing solution possesses (sparsity, low rank, nuclear norm); depth alone can produce or remove it; "grokking can be amplified solely through data selection." |
| 2026-03 | "The Geometric Inductive Bias of Grokking," arXiv:2603.05228 (preprint) | **qualifies + supports** | The cleanest published necessity test. Nanda et al.'s exact regime (`d=128`, 4 heads, `p=113`, 30% train, 10 seeds). Baselines grok at ~51–54k epochs; spherical residual stream or forced-uniform attention removes the delay entirely, and key-frequency ablation confirms "the same Fourier-based solution identified in prior work." Runs at `λ = 0`, detaching the mechanism from the regularizer too. |
| 2026-03 | "Latent Algorithmic Structure Precedes Grokking," arXiv:2603.23784 (preprint) | **qualifies** | Phase-sum relation `φ_out = φ_a + φ_b` holds even in models that fail to grok; an idealized model rebuilt from a 0.23%-accuracy non-grokking model's Fourier components reaches 95.5%. "grokking does not discover the correct algorithm, but rather sharpens an algorithm substantially encoded during memorization." Also reports ReLU MLPs learning **near-binary square-wave** weights rather than sinusoids. |

**Unpublished local work** (author's repositories, not public evidence, recorded for completeness):
a six-architecture ablation on modular *multiplication* reports a linearized transformer that groks
to 100% test accuracy with Fourier alignment 0.000 — a sufficiency counterexample of the form the
published literature lacks, weakened by `n = 1` per architecture, a different operation, and a
non-standard alignment metric. A 1,002-checkpoint trajectory reports generalization *preceding*
Fourier crystallization, opposite to the origin paper's ordering on a different operation.

### Turning points

- **2023-01, at origin.** The strongest qualification to the bundled "grokking circuit" claim is
  inside the origin paper. Anyone reading Appendix C.2.2 and Table 5 on publication day had the
  necessity counterexample in hand.
- **2023-06 (5 months):** Clock and Pizza refutes mechanism *uniqueness*. Fastest
  contradicting result in this document. Its force is limited by a gap that persists: Zhong et al.
  **never measure grokking** — the string "grok" appears in their text only in the bibliography.
  They train on 80% of data, where Nanda et al. report immediate generalization, so the likeliest
  reading is that their models mostly did not grok.
- **2023-11:** Morwani et al. is the turning point in the *upward* direction, and it strengthens a
  narrower object than the origin claim — the Fourier *feature basis* is provably forced under
  stated assumptions (quadratic activation, `L_{2,3}` norm, no biases, one hidden layer). Those
  assumptions do not cover Nanda et al.'s ReLU transformer.
- **2026-03:** the necessity test the field left undone for three years finally gets run with the
  mechanism actually measured.

### Current state versus origin

**The Fourier feature basis is more secure than at origin**; it appears across MLPs, transformers,
RNNs, and non-neural methods, and is provably forced under Morwani et al.'s assumptions.

**The algorithm composed from those features is not unique**, which the origin claim as popularly
stated asserts. Pizza, hybrids, and non-circular solutions occupy the same architecture family
under small hyperparameter changes.

**The bundling of grokking with the mechanism does not survive**, and the origin paper never
asserted it. Grokking is a property of the optimization trajectory; the Fourier mechanism is a
property of the endpoint. Every account of grokking made mathematically precise — weight norm,
lazy-to-rich, margin, circuit efficiency, regularizer geometry — is an account of *when* a
solution is reached, saying nothing about *which*.

**The standing gap, and the field's most legible avoidance pattern:** for three years, every paper
that deleted the grokking delay declined to check what the resulting model computes. Omnigrok,
Kumar et al., Prieto et al., Grokfast — none reported a Fourier analysis of the accelerated model.
The 2026 preprint is the first to do it.

## 2. Induction heads — [COMPLETE]

*Source: `docs/INDUCTION_HEADS_EVIDENCE.md`, which verified every quote below against paper PDFs.
Dates are arXiv v1 month from the identifier (`YYMM.NNNNN`), which is the submission month of v1.*

### Origin

**Olsson et al., "In-context Learning and Induction Heads."** Earliest public version:
Transformer Circuits Thread, **2022-03**; arXiv:2209.11895 followed in **2022-09**. The
Transformer Circuits date is the one that counts.

The paper advances **two claims of different reach**, and the whole temporal story is that later
evidence separated them.

- **Narrow claim.** Induction heads implement in-context token copying via a two-head composition
  (previous-token head → induction head).
- **Broad claim.** Induction heads are the mechanistic source of *general* in-context learning.

Evidence at origin: six arguments spanning phase-change co-occurrence, per-head prefix-matching
scores, and direct ablation. The ablations covered only 1–6 layer models at `d_model` 768
(≤ ~42M parameters). The largest model in the paper (13B, 40 layers) was **never ablated** —
stated by the authors: "Unfortunately, we do not have ablations for our full-scale models."
Their own scope restriction was narrower than what the field attributed to them: "induction heads
are the primary mechanism for in-context learning in **small attention-only models**, but see this
evidence as only suggestive for the MLP case."

Critically, the paper **predicts its own scope refutation** in Argument 6: "it's possible that
above some size, non-induction composition heads could together account for more of the phase
change and in-context learning improvement than induction heads do."

### Timeline

| Date (arXiv v1) | Work | Direction | What it showed |
|---|---|---|---|
| 2023-07 | Halawi, Denain & Steinhardt, arXiv:2307.09476 | **supports** (narrow) | Zero-ablating the 5 highest prefix-matching heads in GPT-J-6B cuts the correct/incorrect demonstration gap by 38.9%, with a random-head control. Ablation *improves* accuracy under misleading demonstrations. |
| 2024-02 | Rushing & Nanda, arXiv:2402.15390 | **qualifies** | Induction heads "don't seem to be self-repaired" — flagged anecdotally, no experiment reported. Implies redundancy by degeneracy rather than dormant backup. |
| 2024-06 | Kissane et al., arXiv:2406.17759 | **qualifies** | SAE analysis splits apparently duplicate induction heads into long-prefix and short-prefix variants; apparent redundancy is partly specialization. |
| 2024-07 | Crosbie & Shutova, arXiv:2407.07011 | **supports** | Strongest direct replication. Mean-ablating the top 1% of prefix-matching heads in Llama-3-8B drops Repetition 91.3% → 59.7% against 85.9% for a **layer-matched** random control. |
| 2024-10 | Cho, Kato, Sakai & Inoue, arXiv:2410.04468 | **qualifies** | Attention knockout of the retrieval-and-copy step costs 5–11 points on Llama-3-8B (vs ≈0 random control) but does **not** reduce ICL to zero-shot: "bypass mechanisms that solve ICL tasks in parallel." |
| 2025-02 | **Yin & Steinhardt, arXiv:2502.14010** | **qualifies + contradicts (broad)** | The controlled test. Ablating induction heads *while excluding the top 2% function-vector heads* has "minimal impact on few-shot ICL performance — comparable to random ablations in models exceeding 1B parameters." The converse does not hold. |
| 2025-02 | Yang, Campbell, Huang, Wang, Cohen & Webb, arXiv:2502.20332 | **contradicts (broad)** | At 70–72B (Qwen2.5-72B, Llama-3.1-70B), heads causally carrying abstract in-context reasoning correlate **r = 0.11** with prefix-matching score and **r = 0.86** with function-vector score — "disjoint sets of attention heads." |
| 2025-04 | Feucht, Todd, Wallace & Bau, arXiv:2504.03022 | **qualifies** | Two causally dissociable populations. Token induction heads carry verbatim copying; concept induction heads carry word-level translation. The two scores are uncorrelated. Olsson's head is only the token route. |
| 2025-05 | **Yang, Cho, Zhong & Inoue, arXiv:2505.18752** | **supports (narrow)** | The 70B ablation. Zero-ablating the top 10% of induction heads in Llama2-70B collapses 8-shot accuracy 80.57% → 2.50%, against 79.13% for matched random. Closes the gap Olsson named. Conditional on a directly copyable label (§I.5 reverses the ordering without one). |
| 2025-07 | Doan, Hiraoka & Inui, arXiv:2507.07810 | **supports** | Zero-ablation at 7B–13B; three or more induction heads removed drops pattern recall 75.4–76.7%. Head selection uncontrolled for FV overlap. |
| 2025-09 | Saanum et al., arXiv:2509.21534 | **qualifies** | 0.5B and 1.5B models drop to chance under induction ablation; the 3B model stays above chance. The largest model is the one that survives. |
| 2025-09 | Sabry & Belz, arXiv:2509.22947 | **qualifies** | Induction-head *scores* can be inflated by curriculum without the mechanism becoming load-bearing: "eliciting a mechanism is not the same as making it load-bearing." Direct warning against the selection proxy the supporting studies use. |
| 2025-09 | Yang, Cho & Inoue, arXiv:2509.24164 | **qualifies** | Up to 34B, ablating induction heads produces a pattern "closely resembling TR head ablation" — they help the model *recognize the task*, rather than perform the in-context computation. Function reassigned, causal potency confirmed. |
| 2025-11 | Şahin, Feucht, Belfki, Brinkmann, Mueller & Bau, arXiv:2511.05743 | **contradicts (developmental)** | Training-time suppression of induction-head formation at 1B leaves abstract ICL intact on **13 of 21 tasks**: "the developmental link between induction heads and abstractive ICL capabilities is weaker than previously hypothesized." |
| 2026-04 | Bajaj et al., arXiv:2604.01094 | **supports** (narrow, unverified) | Serial recall at 7–9B; 50 induction heads ablated drops lag-+1 probability 0.90 → 0.28. |
| 2026-04 | Pouw et al., arXiv:2604.06356 | **supports** (cross-modal, unverified) | Speech model on a Llama-2-7B backbone; 50 prefix-matching heads ablated with random and non-prefix controls. |

**A misattribution to correct.** Bansal et al., arXiv:2212.09095 (2022-12, ACL 2023) is routinely
cited as the 66B causal test. It **prunes heads ranked by task importance** and separately
*computes* induction scores, then observes overlap. It is correlational.

### Turning points

- **2022-03 → 2024-07 (28 months): silence on the stated gap.** The authors named the missing
  large-model ablation in the original paper. Nobody ran it for over two years. During this window
  the broad claim propagated on evidence the authors had explicitly labeled suggestive.
- **2024-07:** Crosbie & Shutova gives the first real large-model replication. An assessment made
  on this date would have *raised* the narrow claim.
- **2025-02 (two papers, eight days apart):** the decisive turning point, and it runs downward on
  the broad claim. Yin & Steinhardt's exclusion control shows the effect was carried by heads that
  are simultaneously function-vector heads. Webb et al. independently reach *r = 0.11* disjointness
  at ten times the scale. Two labs, two methods, one direction.
- **2025-05:** Yang et al.'s 70B result *raises* the narrow claim to its strongest state on the same
  day the broad claim is at its weakest. The two claims move in opposite directions simultaneously.
- **2025-11:** Şahin et al. closes the developmental route — the last surviving argument for the
  broad claim, and the direct analogue of Olsson's own Argument 2, run with the opposite outcome.

### Current state versus origin

**The narrow claim is stronger than at origin and better scoped.** Causal ablation now reaches 70B
with matched random controls, on arbitrary sequences including random tokens. It has been narrowed
in two ways: it is conditional on a directly copyable label being present, and it covers only the
*token* route of a two-route mechanism.

**The broad claim does not survive.** Three independent methods — decorrelating ablation, causal
mediation at 72B, and training-time suppression — reject it. The failure is a **scope refutation
the original authors anticipated**, never a failed replication. Nobody has attempted and failed to
reproduce the small-model ablations.

**The metric dissociation is what reconciles the literature.** On Olsson et al.'s own
token-loss-difference metric, induction heads remain the dominant causal contributor above 345M
parameters. What collapses at scale is their contribution to *few-shot task accuracy* — the metric
the field substituted. Even the narrow claim's advantage on the original metric "decreases with
model scale."

**Standing methodological hole.** Exactly one study in this literature controls for induction/FV
head overlap. Every other causal result selects heads by prefix-matching score alone.

## 3. Greater-Than circuit — [COMPLETE]

### Origin

**Hanna, Liu & Variengien, "How does GPT-2 compute greater-than? Interpreting mathematical
abilities in a pre-trained language model," arXiv:2305.00586, v1 2023-04-30** (NeurIPS 2023).

Claim: GPT-2 small computes greater-than on prompts of the form "The war lasted from the year 1732
to the year 17__" via a circuit whose **final MLPs boost the probability of end years greater than
the start year**. Attention heads move the start-year information to the final position; MLPs 8–11
implement the comparison. The paper claims the mechanism is "generalizable" across contexts.

Evidence at origin: path patching, per-component functional characterization, and generalization
tests to prompt variants beyond the war template.

**The structural feature that shapes its entire follow-up history:** the circuit is
**MLP-dominated**, where IOI is attention-dominated. Almost every method developed for IOI assumes
attention heads are the unit of analysis.

### Timeline

This claim is cited far more than it is examined. Nearly all of the entries below use Greater-Than
as *benchmark task #2 behind IOI* rather than testing the mechanism on its own terms. That pattern
is itself the finding.

| Date (arXiv v1) | Work | Direction | What it showed |
|---|---|---|---|
| 2023-10-11 | Merullo, Eickhoff & Pavlick, arXiv:2310.08744 | **supports (specificity)** | Used as a *low-overlap control* against IOI: Greater Than shares only 3/18 = 16.7% of components with IOI, against 78% for Colored Objects. The circuit is distinguishable from the field's other canonical circuit. |
| 2024-03-26 | Hanna, Pezzelle & Belinkov, arXiv:2403.17806 | **qualifies (by the origin author)** | The smallest EAP circuit containing ≥90% of the manually found Greater-Than nodes achieves **51% faithfulness** — better than IOI's 0%, still only half. Component overlap does not deliver mechanism. |
| 2024-07-19 | uit de Bos & Garriga-Alonso, arXiv:2407.15166 | **supports (relatively)** | Over 1,000,000 benign input pairs, model-vs-circuit KL has mean 2.09, max 5.31 — against IOI's 5.15/14.64 and docstring's 3.91/12.07. **The best worst-case behavior of the three circuits tested.** |
| 2024-09-16 | Li & Janson, arXiv:2409.09951 | **qualifies (minimality)** | Under optimal ablation the Pareto frontier sits 42% below the manual Greater-Than circuit (IOI: 29%). Under mean/resample/counterfactual, optimized circuits achieve 70–84% lower Δ. Also: "resample ablation loss is relatively low for Greater-Than but relatively high for IOI." |
| 2024-10-16 | Shi et al., arXiv:2410.13032 | **contradicts (minimality)** | "the G-T and IOI canonical circuits are not minimal." And a sharper result: "for G-T and IOI, knocking down the complete model has less impact than knocking down the candidate circuit" — under STR ablation, though absent under zero-ablation. |
| 2024-10-28 | **Nikankin, Reusch, Mueller & Belinkov, arXiv:2410.21272** | **contradicts (the framing)** | "Arithmetic Without Algorithms." Across several LLMs, arithmetic is carried by a sparse set of neurons implementing simple range-detecting heuristics whose *unordered combination* explains most accuracy. "LLMs perform arithmetic using neither robust algorithms nor memorization; rather, they rely on a bag of heuristics." Different task family and different models, so it does not falsify the GPT-2 greater-than circuit — it undercuts the inference from "a circuit was found" to "the model implements a comparison algorithm." |
| 2024-11-25 | Nainani et al., arXiv:2411.16105 | **qualifies (generalization)** | Adaptive circuit behavior on task variants, with Greater-Than in Appendix N. Establishes that measured faithfulness on variants can exceed 1 as a knockout artifact. |
| 2026-02-26 | Anani, Lorenz, Schiele, Fritz & Fischer, arXiv:2602.22968 | **qualifies (stability)** | Certified circuit discovery with provable invariance to bounded dataset perturbations; Greater-Than is one of three benchmarks. Up to 56% higher accuracy with 80% fewer components — the manual circuit carries components that certification discards. |
| 2026-06-03 | **Xu, arXiv:2606.05378** | **contradicts (cross-architecture)** | Runs the standard recipe — select heads by task-pattern selectivity, verify by causal ablation against a matched-random null over ten seeds — on Greater-Than plus three other tasks across Pythia-1B, OLMo-1B, and OLMoE-1B-7B. Across the 12 task-model cells, **no two share the same primary causal screen at comparable effect size**. The same task and the same behavioral capability recruit different attention patterns in different models. |
| 2026-07-02 | Gong, Zeng, Yuen & Lim, arXiv:2607.01940 | **qualifies (method boundary)** | Conditional co-ablation, which recovers IOI's backup heads at ROC-AUC 0.91, "does not transfer to the MLP-dominated greater-than circuit" — 1.5× over random, within one standard deviation. Self-repair methods built on attention heads do not carry over. |

### Turning points

- **2024-03-26 (11 months):** the origin author's own follow-up puts overlap-matched faithfulness at
  51%. First qualification, and it comes from inside.
- **2024-10 (18 months):** two results land within two weeks pulling in opposite directions.
  Shi et al. shows the circuit is not minimal and can *underperform* the full model under STR
  ablation; Nikankin et al. reframes arithmetic mechanisms generally as heuristic aggregates.
- **2026-06-03 (37 months):** Xu's cross-architecture null is the first study to run the
  discovery-plus-verification recipe on Greater-Than with a proper matched-random null across
  models and seeds, and it finds no shared primary cause. This is the single result that would most
  change an assessment.

### Current state versus origin

**More robust than IOI on the metric where both were measured head to head.** Greater-Than has the
tightest worst-case KL of the three canonical GPT-2 circuits and 51% rather than 0% overlap-matched
faithfulness. Where the two circuits were compared, Greater-Than came out ahead.

**Minimality fails, as it does for IOI**, and by the same ablation-dependent route.

**The generalization claim has not survived the cross-architecture test.** The origin paper called
the mechanism "generalizable"; the one study that tested it across three 1B-class models found no
two cells sharing a primary causal screen.

**A quiet claim inside a loud literature.** Greater-Than is one of the two most-cited circuits in
mechanistic interpretability and is almost never the object of study. It appears as the second task
in method papers, as a control for IOI, and as a benchmark row. No paper located re-derives the
mechanism, and no paper tests the MLP comparison claim directly. Its MLP-dominated structure means
tools developed on IOI silently do not apply to it, which Gong et al. is the first to state
explicitly.

## 4. Copy suppression — [COMPLETE]

### Origin

**McDougall, Conmy, Rushing, McGrath & Nanda, "Copy Suppression: Comprehensively Understanding an
Attention Head," arXiv:2310.04625, v1 2023-10-06.**

Claim: attention head L10H7 in GPT-2 Small has **one main role across the entire training
distribution** — if earlier components predict a token and that token appears earlier in the
context, the head suppresses it. The claim's distinguishing feature is its scope: it is stated over
OpenWebText rather than over a curated task.

Evidence at origin: 76.9% of L10H7's effect on OpenWebText is explained by a
copy-suppression-preserving ablation (OV ablation alone 81.1%, QK alone 95.2%); 84.70% of
vocabulary tokens have their OV diagonal in the top-10 most negative of its column; L10H7 and
L11H10 account for 39% of IOI self-repair after Name Mover ablation. Replicated in GPT-2 Medium,
Pythia, and Stanford GPT-2 Small E in appendices.

This is the cleanest specificity result of the fifteen claims at origin — the only one whose
headline number is a *fraction of the head's total behavior on the training distribution* rather
than a task-conditional effect size.

### Timeline

| Date (arXiv v1) | Work | Direction | What it showed |
|---|---|---|---|
| 2023-10-11 | Merullo, Eickhoff & Pavlick, arXiv:2310.08744 | **qualifies** | In GPT-2 **Medium** the negative mover "attends only to the S2 token and demotes its likelihood," where in GPT-2 small it attends to all names. Same functional role, different attention pattern one model size up. |
| 2024-02-23 | Rushing & Nanda, arXiv:2402.15390 | **supports + qualifies** | Self-repair "exists on a variety of model families and sizes when ablating individual attention heads on the full training distribution," but is imperfect and noisy across prompts. Identifies two further mechanisms — LayerNorm scaling and sparse Anti-Erasure neurons — so copy suppression is one route among several. |
| 2024-07-15 | Tigges, Hanna, Yu & Biderman, arXiv:2407.10827 | **contradicts (sign, in Pythia)** | In Pythia the copy-suppression heads contribute **positively** to IOI, by downweighting the *incorrect* name. The mechanism is present; its sign relative to the task is model-dependent. |
| 2025-01-30 | Urdshals & Urdshals, arXiv:2501.18666 | **supports (generalization)** | A one-layer attention-only transformer trained from scratch on list sorting spontaneously organizes into two modes, one of which is copy suppression, traced explicitly to the GPT-2 mechanism. Independent architecture, independent task, no pretraining. |
| 2025-05-23 | Edin et al., arXiv:2505.17630 | **qualifies (methodological)** | "Attention self-repair, in which softmax redistribution causes gradients for influential attention scores to vanish" — self-repair silently corrupts gradient-based circuit localization, so measurements of suppression heads by attribution are biased. |
| 2025-05-27 | Jobanputra et al., arXiv:2505.21785 | **supports (generalization)** | An induction-versus-anti-induction asymmetry in pretrained models, traced to circuit-strength differences. Suppression circuitry is a stable pretraining product, not a GPT-2 quirk. |
| 2025-07-16 | **Campregher, Chen, Hoffman & Heuss, arXiv:2507.11809** | **supports (mechanism) + contradicts (a rival account)** | A reproducibility study reconciling three papers. Finds attention heads promote factual outputs through "**general copy suppression rather than selective counterfactual suppression**" — the general mechanism wins over the task-selective one. Also finds strengthening these heads can paradoxically inhibit correct facts, and that behavior varies by domain with larger models more category-sensitive. |
| 2025-08-22 | Saraipour & Zhang, arXiv:2508.16109 | **supports (generalization) + qualifies (scale)** | Heads 10.7 and 11.10 act as negative heads on syllogism tasks, producing negated tokens absent from the input. But "the heads most responsible for enabling opposite syllogism performance in the larger models are not the negative heads." |
| 2026-05-25 | Wang, arXiv:2606.07560 | **supports (analogous structure)** | Function-vector heads split into "writers" and "cancellers" — the same promote/suppress sign structure, in a different head population, invisible to magnitude-only rankings. |
| 2026-07 | Gong, Zeng, Yuen & Lim, arXiv:2607.01940 | **qualifies** | Self-repair is a completeness failure and is 1.9× super-additive; 55% of repair is carried by backups dormant in the intact model. Copy suppression's 39% share is one component of a larger, non-additive repair system. |

### Turning points

- **2025-07-16 (21 months):** Campregher et al. is the only paper that pits the copy-suppression
  account directly against a rival explanation of the same heads and finds copy suppression is the
  correct one. This is the strongest supporting evidence and it arrives as a *reproducibility
  study*, which is unusual in this field.
- **2024-07 and 2025-08:** two independent findings that the mechanism's *relationship to the task*
  flips — positive contribution in Pythia, and displaced by other heads in larger models on
  syllogisms. Neither touches the mechanism itself.

### Current state versus origin

**Stronger than at origin on the mechanism, and unusually so.** Copy suppression is the only claim
of the fifteen that has been (a) reproduced in an explicit reproducibility study, (b) shown to
arise de novo in a from-scratch transformer on an unrelated task, and (c) preferred over a rival
account of the same heads.

**Qualified on the mapping from mechanism to task effect.** The sign of the contribution flips in
Pythia; the responsible heads change in larger models on syllogisms; the attention pattern differs
in GPT-2 Medium. The suppression computation is stable across models; what it does *for any given
task* is not.

**The 39% self-repair share is now known to be a fraction of a non-additive whole**, with 55% of
repair carried by dormant backups and further contributions from LayerNorm scaling and Anti-Erasure
neurons. The origin paper stated 39% as a share of a narrow task and made no claim to exclusivity,
so this is elaboration rather than correction.

**No contradiction of the origin claim as scoped.** Nothing found disputes that L10H7 does copy
suppression across the training distribution.

## 5. IOI circuit — [COMPLETE]

*Source: `docs/IOI_LITERATURE.md`, 37 papers, every number read in the paper's own full text.
This is the densest follow-up literature of the fifteen claims by a wide margin.*

### Origin

**Wang, Variengien, Conmy, Shlegeris & Steinhardt, "Interpretability in the Wild,"
arXiv:2211.00593, 2022-11** (arXiv v1; ICLR 2023 followed).

Claim: a 26-attention-head circuit in 7 functional classes (Duplicate Token, Previous Token,
Induction, S-Inhibition, Name Mover, Negative Name Mover, Backup Name Mover) implements indirect
object identification in GPT-2 small — 1.1% of all (head, position) pairs.

Evidence at origin: path patching traced backward from the logits, head-class characterization by
attention pattern and OV/QK projection, and three self-proposed validation criteria (faithfulness,
completeness, minimality). Headline number: mean-ablating everything outside the circuit leaves
`|F(M)−F(C)| = 0.46`, "87% of the performance of M."

**The origin paper is unusually candid about its own limits**, and three of its disclosures predict
the follow-up literature:

- "Our circuit shows significant improvements compared to a naïve (but faithful) circuit, but
  **fails to pass the most challenging tests**" (§1). Greedy completeness search found subsets with
  incompleteness score up to 3.09 — **87% of the original logit difference**, the same number as the
  headline faithfulness figure.
- Knocking out **all** Name Mover Heads gives "only a 5% drop in logit difference" (§3.4) — their
  own evidence against simple component necessity, later named self-repair.
- The adversarial construction in §4.4 (duplicated IO in a natural sentence) exhibits a mechanism
  "beyond the analysis presented in Section 3."

**The load-bearing methodological choice**, which the follow-up literature turns on: mean ablation
over a `p_ABC` distribution, computed per template, with "around seven examples per template."

### Timeline

| Date (arXiv v1) | Work | Direction | What it showed |
|---|---|---|---|
| 2023-04 | Conmy et al. (ACDC), arXiv:2304.14997 | **supports + qualifies** | ACDC recovers 9 heads "sufficient to complete the IOI task." But edge-level AUC is 0.869 with corrupted activations and **0.539 with zero ablation**; 0.869 (KL) falls to 0.589 (logit difference), and logit-difference optimization "does not find Negative Name Movers at any threshold." |
| 2023-07 | McGrath et al. (Hydra Effect), arXiv:2307.15771 | **qualifies (mechanism of an origin anomaly)** | Self-repair replicates in Chinchilla-7B, "trained without any form of dropout" — killing Wang et al.'s own dropout hypothesis for backup behavior. Never runs IOI. |
| 2023-09 | Zhang & Nanda, arXiv:2309.16042 | **qualifies** | Symmetric token replacement and Gaussian noising "detect different sets of heads as important" for any fixed metric. Corrupting S2 misses ≥2 of 3 Name Mover Heads under every metric; corrupting S1+IO recovers all three and then finds no S-Inhibition Heads. |
| 2023-10 | McDougall et al., arXiv:2310.04625 | **qualifies (specificity)** | 76.9% of L10H7's effect on OpenWebText is copy suppression — the negative name mover is a general mechanism, not an IOI component. Two negative heads account for 39% of post-ablation self-repair. |
| 2023-10 | Merullo, Eickhoff & Pavlick, arXiv:2310.08744 | **qualifies (specificity + replication)** | 78% head overlap (25/32) between IOI and Colored Objects circuits in **GPT-2 Medium**; forcing IOI-style inhibition raises Colored Objects accuracy 49.6% → 93.7%. Overlap collapses to 5/10 (Large) and 0/10 (XL). The negative mover behaves differently in Medium: attends only to S2. |
| 2023-11 | Makelov, Lange & Nanda, arXiv:2311.17030 | **contradicts (a sub-result)** | The MLP8 subspace patching result on IOI is an interpretability illusion; proposes a nullspace diagnostic. |
| 2024-01 | Wu et al. reply, arXiv:2401.12631 | **disputes the critique** | Accepts the empirical finding, rejects the diagnostic and the framing. Both papers report ~4% interchange accuracy for MLP8 and ~70% for the residual stream. **Contradiction left standing.** |
| 2024-02 | Rushing & Nanda, arXiv:2402.15390 | **qualifies** | Self-repair mostly does not invalidate circuit discovery because importance is heavy-tailed — with an explicit caveat for narrow distributions. |
| 2024-03 | Hanna, Pezzelle & Belinkov, arXiv:2403.17806 | **qualifies** | Cross-task faithfulness near zero for most task pairs; overlap does not predict it. The smallest EAP circuit containing ≥90% of the manual IOI circuit's nodes achieves **0% faithfulness** — component overlap is not mechanism identity. |
| 2024-06 | Bhaskar et al. (Edge Pruning), arXiv:2406.16778 | **qualifies (minimality)** | A 98.8%-sparse IOI circuit is as faithful as ACDC's at 96.8% — 2.65× fewer edges. |
| 2024-07 | **Miller, Chughtai & Saunders, arXiv:2407.08734** | **contradicts (the headline number)** | The 87% figure ranges **below 0% to well over 100%** across six methodological choices. The edge-level, specific-token-position variant — which "best represents the hypothesis of Wang et al." — has "a median score well over 100%." Per-example IQR reaches 50%, outliers in the tens of thousands of percent. "The task cannot be separated from the ablation methodology." |
| 2024-07 | Tigges, Hanna, Yu & Biderman, arXiv:2407.10827 | **supports (replication)** | The same three-step algorithm in Pythia 70M–2.8B across 154 checkpoints, path-patching step metrics "generally above 50%," core step above 70%. Two deviations: copy-suppression heads flip sign relative to GPT-2, and Pythia-160m has no duplicate-token heads. Head identity is unstable while the algorithm persists. |
| 2024-07 | uit de Bos & Garriga-Alonso, arXiv:2407.15166 | **contradicts (per-example)** | Over 1,000,000 benign clean/corrupted pairs, model-vs-circuit KL has mean 5.15, max 14.64. "the circuits for the IOI and docstring tasks fail to behave similarly to the full model **even on completely benign inputs from the original task**." |
| 2024-09 | Li & Janson, arXiv:2409.09951 | **supports (against Shi)** | Under optimal ablation the manual circuit is "approximately optimal for its size" — Pareto frontier only 29% below. The 84–85% slack seen under mean/resample/counterfactual ablation is attributed to spoofing artifacts of those methods. |
| 2024-10 | Shi et al., arXiv:2410.13032 | **supports + contradicts** | IOI is significantly more faithful than random circuits up to 90% of model size — passes a flexible sufficiency test. But "the IOI canonical circuit is not minimal": ~20% of edges removable, and faithfulness does not vary monotonically as edges are knocked out. |
| 2024-11 | Nainani et al., arXiv:2411.16105 | **qualifies (artifact)** | "S2 Hacking": on DoubleIO and TripleIO the base circuit *outperforms* the full model (faithfulness 1.285, 2.586), traced to the mean-ablation knockout rather than to model behavior. |
| 2025-03 | Chhabra, Zhu & Khalili, arXiv:2503.01896 | **supports** | Fine-tuning on clean IOI amplifies existing mechanisms without introducing new ones; corrupted models recover the original circuit on retraining at 95–96% faithfulness. |
| 2025-04 | Mueller et al. (MIB), arXiv:2504.13151 | **supports (cross-model)** | IOI localizable in GPT-2, Qwen, Gemma, Llama with EAP-IG. Private test set holds out names and direct objects. Also: "circuits found with CF ablations outperform those found with mean or optimal ablations." |
| 2025-08 | Saraipour & Zhang, arXiv:2508.16109 | **qualifies (specificity)** | Heads 10.7 and 11.10 act as negative heads in *syllogism* tasks; Truth Modulation Heads "align with the S-Inhibition category from IOI." In larger models the responsible heads "are not the negative heads." |
| 2025-10 | Méloux et al., arXiv:2510.00845 | **qualifies (stability)** | Bootstrap-resampled IOI circuits share mean pairwise Jaccard 0.67 on gpt2-small, 0.34–0.39 on Llama. Different EAP variants on the same task overlap at **0.071**. |
| 2026-02 | Franco et al., arXiv:2602.13483 | **qualifies (confound)** | Per-prompt IOI circuits cluster into families — by role order (ABBA vs BABA) in GPT-2 Small, by surface wording in Pythia-160M. |
| 2026-05 | **Li & Subramani, arXiv:2605.08348** | **contradicts (necessity + specificity)** | Ablating the shared IOI circuit produces **near-zero or negative accuracy drops** in Gemma, Llama, and Qwen at K ≤ 10%; "random ablation hurts more than shared-circuit ablation." The full cross-task ablation matrix — the correct dissociation design — finds no dissociation at all. IOI circuit reuse in OLMo-2 peaks in the first ~76B tokens then declines; necessity is negative at 17 of 20 checkpoints. |
| 2026-05 | Venkatesh, arXiv:2605.08853 | **qualifies (architecture)** | Circuit concentration tracks attention architecture, not scale: GQA models need 1 ablation to reach 80% task damage, MHA models 2–5. |
| 2026-05 | **Chen et al., arXiv:2605.12671** | **contradicts (uniqueness)** | Two sheaves, both **100% IOI accuracy**, both ~3.5–4% edge density, edge IoU **4.1%**. Across 20 sheaves the shared core is 11 edges of a 7382-edge union (mutual IoU 0.15%). A three-edge sheaf reaches 86.7% accuracy alone. Node-level IoU is 64.2% — the near-disjointness is in *routing*, not in which heads participate. |
| 2026-05 | Naser Moghadasi & Ghaderi, arXiv:2605.22719 | **qualifies (confound)** | 45 of 300 prompts using the object "the keys" account for 42 of 61 failures (93.3% vs 7.5%, Fisher exact p = 8.79 × 10⁻³³). Conditioning on the keys-free subset drops significant SAE features from 146 to 5. |
| 2026-06 | Bayat Makou et al., arXiv:2606.06267 | **qualifies (methodological control)** | On a different task, structurally distinct circuits proved **functionally interchangeable** under cross-condition transfer. Structural difference alone does not establish mechanistic difference — the control Chen et al.'s result needs, not yet run on IOI. |
| 2026-06 | Wu, Tonin & Cevher, arXiv:2606.16920 | **qualifies (variance)** | EAP-IG circuits vary under resampling and prompt rephrasing; "prompts with different templates tend to activate different circuits." |
| 2026-07 | Gong et al. (CoAx), arXiv:2607.01940 | **qualifies (recovers necessity)** | Ablating documented name-mover primaries moves IOI accuracy 1.00 → 0.97. Ablating primaries **plus their eight backups** drops logit difference by 1.15 against 0.60 predicted by summing single ablations — 1.9× super-additive. 55% of repair is attributed to backups dormant in the intact model. Completeness gap closes from 0.72 to 0.15 once backups are added. |

### Turning points

- **2022-11, at origin.** The completeness failure (incompleteness up to 3.09, 87% of the logit
  difference) and the 5%-drop Name Mover knockout were both in the original paper. Neither
  travelled with the claim.
- **2023-04 (5 months):** ACDC's zero-vs-corrupted AUC gap (0.869 → 0.539) is the first published
  signal that the result is method-conditional. It appears as a methods detail, not a critique.
- **2024-07 (20 months):** Miller et al. is the decisive turning point. The 87% number does not
  survive its own protocol's variations, and the variant that best matches the stated hypothesis
  scores **over 100%**. An assessment made the day before and the day after differ sharply.
- **2024-07, simultaneously:** uit de Bos & Garriga-Alonso shifts the question from average to
  per-example behavior, and the circuit fails there on benign in-distribution inputs.
- **2026-05 (42 months):** Li & Subramani and Chen et al. land in the same month and attack
  different pillars — necessity and specificity outside GPT-2, and uniqueness inside it.
- **2026-07:** Gong et al. partially *reverses* the necessity failure by showing the problem was
  first-order ablation missing dormant backups. This is the clearest instance in this document of
  a claim recovering after being weakened.

### Current state versus origin

**The algorithm replicates; the numbers do not.** The three-step algorithm reproduces across
Pythia 70M–2.8B, GPT-2 Medium, and four architectures on MIB. The specific 87% figure is a
property of one ablation protocol.

**Necessity split by ablation order.** First-order single-component ablation fails on GPT-2 small
because of self-repair — which the origin paper reported and did not resolve. Set-level necessity
is recovered only when backups are removed jointly (2026-07). No paper reports a clean necessity
result for the 26-head circuit as originally specified.

**Uniqueness is refuted at the edge level** and holds at the node level (64.2% node IoU vs 4.1%
edge IoU). Which of these matters depends on whether the claim is about *which heads participate*
or *how information routes*, and the origin claim is stated at edge level.

**Specificity has moved from untested to negative.** Every paper that tested it — Merullo,
McDougall, Hanna, Li & Subramani, Saraipour — found components shared with other tasks. The
formal double dissociation has still never been run on IOI; the nearest attempt found no
dissociation.

**Four contradictions are still standing and unresolved**: minimality (Shi vs Li & Janson),
task-specificity (Merullo vs Hanna), whether self-repair invalidates discovery (Rushing & Nanda vs
Gong), and the MLP8 illusion (Makelov vs Wu). Each is traceable to a methodological choice rather
than to an experimental error.

**Structurally unanswerable for the original model.** Cross-seed circuit stability and circuit
co-emergence with behavior cannot be tested in GPT-2 small — it was released as a single run
without intermediate checkpoints.

## 6. Superposition — [COMPLETE]

### Origin

**Elhage et al., "Toy Models of Superposition."** Earliest public version: Transformer Circuits
Thread, **2022-09**; arXiv:2209.10652 the same month.

Claim: neural networks represent **more features than they have dimensions** by storing features in
near-orthogonal directions, accepting interference in exchange for capacity. Sparsity governs when
superposition occurs; features organize into regular geometric structures (digons, triangles,
pentagons, tetrahedra) as sparsity increases; a phase transition separates monosemantic from
polysemantic regimes.

Evidence at origin: small ReLU autoencoders on synthetic sparse features, analyzed exhaustively.
The paper is explicit that this is a **toy model** — a hypothesis about real networks, not a
demonstration in them. That self-declared scope is the reason the follow-up literature reads as it
does: the claim's history is the history of attempts to move it out of the toy setting.

### Timeline

| Date | Work | Direction | What it showed |
|---|---|---|---|
| 2022-10-04 | Scherlis, Sachan, Jermyn, Benton & Shlegeris, arXiv:2210.01892 | **supports (theory)** | "Feature capacity" — the fractional dimension each feature consumes. Optimal allocation keeps important features monosemantic and shares unimportant ones; polysemanticity rises with input kurtosis and sparsity. Identifies a block-semi-orthogonal embedding geometry. Independent derivation of the origin paper's core tradeoff, three weeks later. |
| 2023-05-02 | **Gurnee, Nanda, Pauly, Harvey, Troitskii & Bertsimas, arXiv:2305.01610** | **supports (real models)** | Sparse probing over 100+ features in 7 models from 70M to 6.9B. "Early layers make use of sparse combinations of neurons to represent many features in superposition." The first evidence for superposition in real language models rather than toys. |
| 2023-09-15 | Cunningham, Ewart, Riggs, Huben & Sharkey, arXiv:2309.08600 | **supports (method)** | Sparse autoencoders recover interpretable features from polysemantic activations — a decomposition method presupposing and apparently confirming superposition. |
| 2023-10 | Bricken et al., "Towards Monosemanticity," Transformer Circuits Thread | **supports** | Dictionary learning on a one-layer model recovers monosemantic features from superposed activations at scale. |
| 2023-12-05 | **Lecomte, Thaman, Schaeffer, Bashkansky, Chow & Koyejo, arXiv:2312.03096** | **contradicts (an inference, not the claim)** | "Incidental polysemanticity": polysemanticity arises **even when there are ample neurons to represent all features**, from regularization and neural noise. Random initialization assigns multiple features to a neuron by chance, and training dynamics strengthen the overlap. The observation that motivated superposition has a second sufficient cause. |
| 2024-05-23 | **Engels, Michaud, Liao, Gurnee & Tegmark, arXiv:2405.14860** | **qualifies (structurally)** | Irreducible **multi-dimensional** features exist — circular representations of days of the week and months of the year in GPT-2 and Mistral-7B — and intervention experiments on Mistral-7B and Llama-3-8B show these circular features "are indeed the fundamental unit of computation in these tasks." The one-feature-one-direction premise underlying the geometric account is false for at least some features. |
| 2024-05 | Templeton et al., "Scaling Monosemanticity," Transformer Circuits Thread | **supports (scale)** | Dictionary learning extended to a production model, recovering millions of features. |
| 2025-02-07 | Leask, Bussmann, Pearce, Bloom, Tigges, Al Moubayed, Sharkey & Nanda, arXiv:2502.04878 | **qualifies (the recovery method)** | SAE latents are neither complete nor atomic — larger dictionaries recover latents smaller ones miss, and single latents decompose into finer ones. The instrument used to demonstrate superposition in real models does not recover canonical units. |
| 2025-05-15 | **Liu, Liu & Gore, arXiv:2505.10465** | **supports (strongest)** | "Superposition Yields Robust Neural Scaling." Under strong superposition, loss scales inversely with model dimension across a broad class of frequency distributions, from geometric overlap between representation vectors. **Open-source LLMs are confirmed to operate in the strong-superposition regime**, and the Chinchilla scaling laws are consistent with it. Superposition makes a quantitative prediction about a phenomenon it was not designed to explain, and the prediction holds in real models. |
| 2026-06-12 | Bhagat, Molas-Medina, Giglemiani & Heimersheim, arXiv:2606.14673 | **contradicts (a downstream toy model)** | The Compressed Computation model's advantage comes from "mixing inputs via its noisy residual stream" rather than superposed computation; gains track a mixing matrix and vanish when it is removed. "CC is not a suitable toy model of computation in superposition." |
| 2026-06-16 | arXiv:2606.18538 | **qualifies** | Effects of sparsity and superposition on loss in simple autoencoders. |
| 2026-06-18 | arXiv:2606.19946 | **supports** | Geometric constraints enabling multi-semantic superposition in LLMs. |
| 2026-07-06 | arXiv:2607.04800 | **disputes the critique** | "Compressed Computation under L⁴ Loss is likely Computation in Superposition" — a direct rebuttal three weeks later. **Contradiction left standing.** |

### Turning points

- **2023-05-02 (8 months):** Gurnee et al. moves the claim from toys to real models. Before this
  date, superposition in language models was an extrapolation.
- **2023-12-05 (15 months):** Lecomte et al. is the first result that would have lowered an
  assessment. It does not show superposition is absent; it shows the *evidence* for it —
  polysemantic neurons — is not diagnostic, because incidental polysemanticity produces the same
  observation with ample capacity. This is a construct-validity problem, not an empirical
  refutation, and the authors flag the two stories as non-mutually-exclusive.
- **2024-05-23 (20 months):** Engels et al. breaks the one-dimensional-feature premise. The
  geometric structures in the origin paper are structures of *directions*; irreducible circular
  features are not directions.
- **2025-05-15 (32 months):** the strongest supporting evidence, and it arrives by an unusual
  route — a novel quantitative prediction (the scaling exponent) rather than another decomposition.

### Current state versus origin

**The core claim is better supported than at origin and now has a quantitative confirmation in
real models.** Superposition has moved from toy-model hypothesis to a mechanism confirmed present
in open-weight LLMs, with a derived scaling law consistent with Chinchilla.

**Two of the origin paper's specific commitments have been qualified.** Features are not all
one-dimensional (2024-05), and the geometric phase structure was demonstrated in synthetic
autoencoders whose relationship to language models remains inferential.

**The diagnostic inference has been contradicted.** Polysemanticity does not imply superposition;
incidental polysemanticity produces it with ample capacity. Since polysemantic neurons are the
observation most often cited as evidence for superposition in real models, this matters more than
its citation count suggests.

**The instrument problem is unresolved.** Sparse autoencoders both presuppose superposition and
supply most of the evidence for it, and the same instrument has been shown not to recover atomic
units. This circularity is the claim's largest standing weakness, and it is inherited from the
method rather than from the origin paper.

**One live dispute:** whether compressed computation is computation in superposition, with a
critique (2026-06) and rebuttal (2026-07) three weeks apart and no resolution.

## 7. Steering vector (refusal direction) — [COMPLETE]

### Origin

**Arditi, Obeso, Syed, Paleka, Panickssery, Gurnee & Nanda, "Refusal in Language Models Is Mediated
by a Single Direction," arXiv:2406.11717, v1 2024-06-17** (NeurIPS 2024).

Claim: refusal is mediated by **a single direction** in the residual stream. Ablating the direction
removes refusal; adding it induces refusal. Replicated across 13 open-weight chat models up to 72B.

Evidence at origin: difference-in-means direction extraction, directional ablation and activation
addition as bidirectional intervention, and a weight-orthogonalization jailbreak demonstrating the
finding is load-bearing rather than descriptive.

**The word "single" is the load-bearing part of the title**, and it is the part the follow-up
literature attacked. Everything below concerns dimensionality, not whether the intervention works.

### Timeline

| Date (arXiv v1) | Work | Direction | What it showed |
|---|---|---|---|
| 2024-07-17 | Tan, Chanin, Lynch, Kanoulas, Paige, Garriga-Alonso & Kirk, arXiv:2407.12404 | **qualifies** | Steering vectors show "substantial limitations both in- and out-of-distribution." Steerability varies by input, spurious biases contribute substantially to measured effectiveness, and generalization is brittle under prompt variation. **One month after origin.** |
| 2024-11-13 | Marshall, Scherlis & Belrose, arXiv:2411.09003 | **qualifies (generalizes it)** | "Refusal in LLMs is an Affine Function." Prior steering methods, including the single direction, are **subsets** of an affine decomposition. Affine concept editing controls refusal reliably across ten models including Llama-3-70B and "generalizes to models where previous techniques fail." The direction is a special case of a larger object. |
| 2025-02-24 | **Wollschläger, Elstner, Geisler, Cohen-Addad, Günnemann & Gasteiger, arXiv:2502.17420** | **contradicts** | "Contrary to prior work, we uncover multiple independent directions and even multi-dimensional **concept cones** that mediate refusal." Introduces representational independence — orthogonality alone does not imply independence under intervention — and identifies mechanistically independent refusal directions. "Multiple distinct mechanisms drive refusal behavior." |
| 2025-04-03 | Du et al., arXiv:2504.02904 | **qualifies** | The refusal direction differs between base and post-trained models with limited forward transferability. |
| 2025-04-26 | Abbas et al., arXiv:2504.18872 | **qualifies** | Latent adversarial training concentrates refusal representation in early SVD components, creating a new vulnerability to self-generated vectors. |
| 2025-05-22 | **Wang et al., arXiv:2505.17306** | **supports (strongest)** | "Refusal Direction is Universal Across Safety-Aligned Languages." English-derived refusal vectors transfer across **14 languages** without fine-tuning. The direction is not an artifact of one language's alignment data. |
| 2025-07-03 | Yamaguchi et al., arXiv:2507.03167 | **qualifies (reasoning models)** | "Where Do Reasoning Models Refuse?" Linear refusal directions are extractable from reasoning-model activations, but ablating them **reduces robustness less than in non-reasoning models** — the single-direction lever weakens where chain-of-thought is present. |
| 2025-07-16 | **Zhao et al., arXiv:2507.11878** | **contradicts (construct)** | "LLMs Encode Harmfulness and Refusal Separately." A harmfulness direction exists distinct from the refusal direction, and steering each produces different behavioral outcomes. The refusal direction is a behavioral lever downstream of a separate harm representation, which is precisely the affinity-versus-efficacy distinction. |
| 2025-09-07 | Prakash et al., arXiv:2509.09708 | **contradicts** | Sparse autoencoders identify multiple feature subgroups whose ablation independently flips refusal — "redundant safety mechanisms," not one. |
| 2025-09-08 | Du et al., arXiv:2509.06795 | **qualifies (stability)** | The refusal direction **drifts** during fine-tuning; projection magnitude must be constrained to stabilize it. |
| 2025-11-11 | Piras et al., arXiv:2511.08379 | **contradicts** | "SOM Directions are Better than One." Multiple refusal directions extracted via self-organizing maps outperform the single-direction approach at suppression. |
| 2026-03-29 | Maskey et al., arXiv:2603.27518 | **qualifies (scope)** | Harmful-refusal directions are task-agnostic; **over-refusal directions are task-dependent and span higher dimensions**. The single direction covers one of two refusal regimes. |
| 2026-04-09 | Cheng, Wiegreffe & Manocha, arXiv:2604.08524 | **supports (mechanism)** | The first mechanistic account of *why* steering works. Steering vectors act through the **OV circuit** and largely ignore QK — freezing all attention scores during steering costs only 8.75% across two model families. Vectors sparsify by 90–99% with most performance retained, and different steering methods agree on a subset of important dimensions. |
| 2026-05-17 | David et al., arXiv:2605.17413 | **contradicts** | Comparing refusal-direction projection against subspace methods, **rank-4 projection achieves a better utility-safety balance** than the rank-1 direction. |
| 2026-06-21 | Ratnakar & Vats, arXiv:2606.22686 | **qualifies** | Across seven model families, the safety axis is a steerable linear feature that is "fundamentally unstable" and collapses under prefix injection — simultaneously a defense primitive and a vulnerability. |
| 2026-07-02 | arXiv:2607.02396 | **contradicts** | "Fast Multi-dimensional Refusal Subspaces via RFM-AGOP" — the single direction is extended to a subspace as a matter of course. |

### Turning points

- **2024-07-17 (1 month):** Tan et al. is the **fastest qualification of any claim in this
  document**. Reliability limits on steering vectors were published one month after the origin
  paper.
- **2025-02-24 (8 months):** Wollschläger et al. is the decisive contradiction and states it in
  those terms. Any assessment before this date reads "single direction" as established; after it,
  the word cannot stand.
- **2025-05-22 (11 months):** the strongest supporting result arrives three months *after* the
  strongest contradiction, and they are compatible: the direction is universal across languages and
  is one of several.
- **2025-07-16 (13 months):** the construct-validity turn. Separating harmfulness from refusal
  shows the direction is a lever on the output behavior rather than the representation of the
  concept — the description-mode mismatch, demonstrated rather than argued.
- **2026-04-09 (22 months):** the mechanism is finally explained (OV circuit, 90–99% sparsifiable).
  This is support for the *intervention*, and it also explains why a single direction was ever
  sufficient without being unique.

### Current state versus origin

**The intervention is more robust than at origin.** Bidirectional control replicates across 13+
models, 14 languages, multiple modalities, and reasoning models, with a mechanistic account of the
pathway. Nothing found disputes that ablating a refusal direction removes refusal.

**"Single" does not survive.** At least six independent groups — using gradient-based extraction,
self-organizing maps, sparse autoencoders, affine decomposition, subspace projection, and RFM-AGOP —
find multiple independent directions or a higher-rank subspace, and several report that the
multi-dimensional version *outperforms* the single direction on the origin paper's own task.
Publishing multi-directional refusal is now routine rather than contrarian.

**The construct has been split.** Harmfulness and refusal are encoded separately, and over-refusal
is task-dependent while harmful-refusal is not. The origin claim addressed one direction in one of
several regimes.

**Fragility is documented in four independent ways**: input-dependent steerability (2024-07), drift
under fine-tuning (2025-09), collapse under prefix injection (2026-06), and weakening in reasoning
models (2025-07).

This is the **fastest-qualified and most-contradicted claim of the fifteen**, and it remains among
the most useful. The gap between "the lever works" and "the lever is the representation" is where
every contradiction sits.

## 8. Global workspace / J-space — [COMPLETE — and the timeline is empty by construction]

### Origin

**Gurnee, Sofroniew, Pearce, Piotrowski, Kauvar, Chen, Soligo, Bogdan, Ong, Wang, Thompson,
Abrahams, Kantamneni, Ameisen, Batson & Lindsey (Anthropic), "Verbalizable Representations Form a
Global Workspace in Language Models."** Earliest public version: Transformer Circuits Thread,
**2026-07-06**; arXiv:2607.15495 on **2026-07-16**.

Claim: language models maintain a privileged set of internal representations — the **J-space** —
that functions like a global workspace, enabling flexible reasoning and report while routine
processing continues unaffected.

Method: the **Jacobian lens** computes "the average linearized effect of an activation on the
model's likelihood of producing a particular token," averaged across diverse contexts to isolate
generally verbalizable concepts. At any moment the J-space is a sparse non-negative combination of
roughly **10–25 J-lens vectors**, occupying **under 10% of activation variance**.

Evidence at origin: three converging interventions.
- **Swap** — exchange one concept's lens vector for another while preserving orthogonal components.
- **Ablate** — zero the top-k J-lens directions across specified layers.
- **Inject** — add a concept's lens vector and test whether it becomes reportable or changes behavior.

Models: Claude Sonnet 4.5 primary, corroborated on Haiku 4.5 and Opus 4.5, with some analyses on
Opus 4.6.

**Stated limitations at origin**, which are unusually forthcoming: the J-lens resolves only
single-token concepts and misses multi-token words and phrases; it captures the underlying structure
only approximately; transformers lack clear analogs to brain specialization and recurrent broadcast;
and early-layer workspace contents may be unresolved by the method.

**The deception sub-claim.** Models trained with misaligned behaviors carry internal workspace
signatures absent from their outputs — a model trained to write malicious code shows "secretly" and
"trick" in J-lens readouts; one taught to appease biased reward models shows "reward" and "bias."

### Timeline

**Empty. Reported as quiet because the claim is under one month old.**

Searches run: arXiv abstract search for "Jacobian lens," "J-lens," and "verbalizable
representations" (one hit — the origin paper itself); arXiv abstract search for "global workspace"
combined with language model terms, sorted newest-first (same single hit). No replication, critique,
or extension exists.

**One item could not be verified.** The audit's case-study text refers to "an independent
replication on open-weight Qwen." No such paper was located in the searches above. Either it is not
on arXiv, it postdates indexing, or the characterization needs a source. Recorded as unverified
rather than absent.

### Turning points

None available. The interval from origin to the present is **26 days**.

### Current state versus origin

Identical to origin. Nothing has been added and nothing has been contested.

**This claim's value in the temporal exercise is as a control.** Every other claim in this document
has had between 5 and 76 months of exposure. The workspace claim shows what a claim looks like
before the literature has touched it: three converging interventions from one lab, one evidence
family, on closed-weight models, with specificity untested and the interpretive question — whether
the subspace is a workspace or a general high-influence bottleneck — unaddressed because no one
outside the authoring lab has yet had the chance to address it.

**A structural feature that will shape its future timeline.** The J-space is *defined* as the
directions most influential on output tokens. Any correlation with deliberate reasoning is
therefore partly guaranteed by construction, and the specificity test that would separate a
workspace from a bottleneck — does ablating it degrade every task that coordinates many
representations, or only deliberate reasoning? — is the first experiment an outside group would
run. Whether that experiment happens, and when, is the measurement this document would take on a
future pass.

## 9. Successor heads — [COMPLETE]

### Origin

**Gould, Ong, Ogden & Conmy, "Successor Heads: Recurring, Interpretable Attention Heads In The
Wild," arXiv:2312.09230, v1 2023-12-14** (ICLR 2024).

Claim: **successor heads** — attention heads that increment tokens with a natural ordering
(numbers, months, days of the week) — recur across model scales and architectures. The mechanism
rests on **mod-10 features** in the numeric representation. The heads are polysemantic on natural
language.

Evidence at origin: identification across multiple model families, feature-level analysis of the
mod-10 structure, and ablation. The claim's distinguishing strength at origin is
**cross-architecture recurrence** — it was framed as a *universality* result from the start, which
is rare among the fifteen.

### Timeline

This is one of the quieter claims. The abstract phrase "successor head" appears in only two arXiv
papers in the whole corpus: the origin paper and one 2025 follow-up. The evidence below is mostly
indirect — work on the mod-10 substrate and on cross-architecture recurrence.

| Date (arXiv v1) | Work | Direction | What it showed |
|---|---|---|---|
| 2023-11-07 | Lan, Torr & Barez, arXiv:2311.04131 | **concurrent, supports** | "Towards Interpretable Sequence Continuation." Shared circuits across similar sequence-continuation tasks in GPT-2 and Llama-2. Published **five weeks before** the origin paper, reaching a compatible conclusion independently. |
| 2024-01-22 | Gurnee et al., arXiv:2401.12181 | **supports (universality)** | "Universal Neurons in GPT2." A minority of neurons recur across independently trained models with the same function — the general phenomenon the successor-head claim instantiates. |
| 2024-10-15 | **Levy & Geva, arXiv:2410.11781** | **supports (the substrate)** | LLM errors on numerical tasks distribute across *digits* rather than around numeric value, and probing plus causal intervention shows "individual circular representations per-digit in base 10" rather than value encoding. Independent confirmation of the mod-10 feature account, arrived at from error analysis rather than from head analysis. |
| 2024-10-28 | Nikankin, Reusch, Mueller & Belinkov, arXiv:2410.21272 | **qualifies (framing)** | Arithmetic is carried by a bag of heuristic neurons, each detecting a numerical input pattern, whose unordered combination explains most accuracy. Increment behavior sits inside a heuristic aggregate rather than an algorithm. |
| 2025-04-29 | **He et al., arXiv:2504.20938** | **qualifies (decomposition)** | Low-Rank Sparse Attention finds "cleaner and finer-grained versions of previously discovered MHSA behaviors like induction heads, successor heads," resolving atomic arithmetic operations in Llama-3.1-8B. The successor head is a coarse unit that decomposes under a better basis — the head is not the atom. |
| 2025-08-04 | arXiv:2508.02513 | **supports (substrate)** | "Modular Arithmetic: Language Models Solve Math Digit by Digit." Converges with Levy & Geva on digit-wise structure. |
| 2026-06-03 | **Xu, arXiv:2606.05378** | **contradicts (universality)** | Successor sequences are one of four tasks run through the standard select-then-ablate recipe with a matched-random null over ten seeds, across Pythia-1B, OLMo-1B, and OLMoE-1B-7B. Across the 12 task-model cells **no two share the same primary causal screen at comparable effect size**. This attacks the origin claim's central selling point — cross-architecture recurrence. |
| 2026-07-18 | Naganna, Sijan & Kalita, arXiv:2607.16693 | **supports (invariance)** | Arithmetic heuristic neurons are largely form-invariant across symbolic arithmetic, word problems, and Python code in Llama-3. Transferring shared-neuron activations from a successful format to a failed one recovers over 97% of incorrect predictions for addition and subtraction. Cross-format failures come from activation states, not from distinct circuits. |

### Turning points

- **2024-10-15 (10 months):** the mod-10 substrate is independently confirmed by a group studying
  numeric errors rather than heads. This is convergent evidence in the strict sense — different
  question, different method, same structure — and it is the strongest support the claim has.
- **2025-04-29 (16 months):** the unit of analysis is undercut. Successor heads resolve into finer
  components under sparse decomposition, so "a head that increments" describes an aggregate.
- **2026-06-03 (30 months):** the universality claim is directly tested with a proper null for the
  first time, and fails.

### Current state versus origin

**The representational substrate is stronger than at origin.** Mod-10 / per-digit circular
structure has independent confirmation from error analysis and from causal intervention, in models
the origin paper did not study.

**The unit of analysis has been undercut.** Sparse attention decomposition resolves successor heads
into finer atomic operations, so the head is a convenient aggregate rather than a mechanism
boundary.

**The universality claim — the origin paper's headline — has one direct test and it is negative.**
Across 1B-class models of three architectures, successor-sequence circuits do not share a primary
causal screen.

**Reported as quiet.** Two arXiv abstracts in the entire corpus name successor heads. The claim is
cited widely as an example of a recurring interpretable head and is examined on its own terms
almost never. This is a genuine gap rather than a failure to search: the searches run were on the
phrase, on the mod-10 mechanism, and on the full citation list.

## 10. Othello world model — [COMPLETE]

### Origin

**Li, Hopkins, Bau, Viégas, Pfister & Wattenberg, "Emergent World Representations: Exploring a
Sequence Model Trained on a Synthetic Task," arXiv:2210.13382, v1 2022-10-24** (ICLR 2023 oral).

Claim: a GPT trained only on legal Othello move sequences, with no knowledge of the board or the
rules, develops an **emergent world representation** of the board state.

Evidence at origin: *nonlinear* probes decode board state (black / white / empty) with high
accuracy where linear probes largely fail, and interventions along probe directions change the
model's move predictions in the direction the edited board implies. The intervention is what
separates this from ordinary probing.

**The technical claim the origin paper made and later had to give up:** that the representation is
**nonlinear**, inferred from linear probes underperforming.

### Timeline

| Date | Work | Direction | What it showed |
|---|---|---|---|
| 2023-03 | Nanda, "Actually, Othello-GPT Has A Linear Emergent World Representation" (LessWrong; earliest public version) | **contradicts (technical) + supports (headline)** | Probing for **"my colour vs opponent's colour"** rather than black vs white recovers the board state with *linear* probes, and vector arithmetic on those directions steers the model. The origin paper's nonlinearity conclusion was an artifact of the chosen basis. The world representation is real and simpler than claimed. |
| 2023-09-02 | Nanda, Lee & Wattenberg, arXiv:2309.00941 | **same, peer-reviewable form** | The arXiv version of the above, with a co-author from the origin paper. |
| 2023-10-11 | Hazineh et al., arXiv:2310.07582 | **supports** | Independent confirmation that the linear representations causally steer decisions, with the effect depending on layer depth. |
| 2024-02-19 | He et al., arXiv:2402.12201 | **supports** | Sparse dictionary learning extracts monosemantic features and identifies fine-grained circuits — the representation supports mechanism-level decomposition, not only decoding. |
| 2024-03-21 | **Karvonen, arXiv:2403.15498** | **supports (generalization)** | Chess-playing language models learn internal board-state representations, and additionally estimate a latent **player-skill** variable that improves predictions. The phenomenon is not specific to Othello. |
| 2024-06-06 | **Vafa, Chen, Rambachan, Kleinberg & Mullainathan, arXiv:2406.03689** | **contradicts (the inference)** | Formalizes world-model evaluation via deterministic finite automata and Myhill–Nerode. "The generative models we consider do well on existing diagnostics for assessing world models, but our evaluation metrics reveal their world models to be **far less coherent than they appear**" — failing under small task modifications despite superior next-token performance. The diagnostic the origin claim rests on does not distinguish a coherent world model from an incoherent one. |
| 2024-12-10 | Rohekar et al., arXiv:2412.07446 | **supports (stronger form)** | Causal structure encoded in attention, supporting zero-shot causal learning on Othello and chess sequences. |
| 2025-01-13 | Du et al., arXiv:2501.07108 | **supports (refines)** | Layer-wise progression: early layers capture static board attributes, deeper layers track dynamic tile changes. |
| 2025-03-06 | **Yuan & Søgaard, arXiv:2503.04421** | **supports (strongest)** | "Revisiting the Othello World Model Hypothesis." Seven models — GPT-2, T5, Bart, Flan-T5, Mistral, LLaMA-2, Qwen2.5 — reach **up to 99% accuracy** in unsupervised board-layout induction, with high similarity of learned board features across architectures. Architecture-independent replication. |
| 2025-10-28 | Singh et al., arXiv:2511.00059 | **supports** | Decision-tree analysis finds roughly half of layer-5 neurons encode rule-based game logic. |
| 2026-02-26 | Chawla et al., arXiv:2602.23164 | **supports (causal, cross-rule)** | "MetaOthello": transformers trained on mixed Othello variants converge on **shared board representations that transfer causally across rule sets**. |
| 2026-05-11 | Lee et al., arXiv:2605.09967 | **qualifies (structurally)** | Board-state representations have **tensor-product structure**, factorizing into square and colour embeddings. The representation is richer than a set of linear directions, and the linear-direction account is a projection of it. |

### Turning points

- **2023-03 (5 months):** the fastest correction in this document, and it is a correction that
  *strengthens* the headline while overturning a specific technical claim. This is the clearest case
  in the fifteen of a result improving under contradiction.
- **2024-06-06 (20 months):** Vafa et al. is the only genuine challenge, and it attacks the
  *inference* rather than the finding. It does not deny that board state is decodable; it denies
  that decodability plus intervention establishes a coherent world model, and supplies a metric
  showing the difference.
- **2025-03-06 (29 months):** architecture-independent replication at 99%. After this date the
  empirical core is about as well replicated as any claim in mechanistic interpretability.

### Current state versus origin

**The empirical core is substantially stronger than at origin.** Board state is linearly decodable
and causally interveneable, in seven architectures, in chess as well as Othello, transferring
causally across rule variants, with tensor-product structure and identified rule-encoding neurons.
This is the most-replicated claim of the fifteen.

**The nonlinearity claim is refuted**, five months after publication, by re-basing the probe.

**The "world model" label remains ahead of the evidence, and the gap is now measured.** What has
been established is that board state is *linearly decodable and causally load-bearing for move
prediction*. Vafa et al. shows that a model passing exactly these diagnostics can still have a world
model that is "far less coherent than it appears," failing on small task modifications. The
interpretive question — what licenses "world model" over "linearly decodable causally-relevant state
representation" — has one paper on it and remains open.

**Vafa et al. did run their coherence metric on Othello-GPT.** § 4 applies it to both of Li et al.'s
checkpoints. The synthetic model scores 0.98 / 0.99 / 1.00 against an untrained floor of
0.00 / 0.02 / 0.14, and Vafa et al. write that it "recovers the true world model." The championship
model fails (0.00 / 0.65 / 0.27). The result therefore splits by checkpoint rather than refuting the
claim, and it narrows the label's scope to the synthetically trained model.

## 11. Docstring circuit — [COMPLETE]

### Origin

**Heimersheim & Janiak, "A Circuit for Python Docstrings in a 4-Layer Attention-Only
Transformer," Alignment Forum, 2023-02-20.** Never submitted to arXiv, never peer-reviewed. The
Alignment Forum post is the only version.

Claim: an eight-head circuit across four layers predicts argument names in Python docstrings, via
three information flows — a definition subcircuit (head 1.4 reads `B_def`, head 2.0 copies to
`C_def`), a docstring subcircuit (head 0.4 derives position from the causal mask, head 1.4 uses
induction to find matching `B_doc`), and two argument-mover heads (3.0, 3.6) integrating both.

Evidence at origin: residual-stream patching tracing the information path, per-head attention
patching, and ablation. **The model is a 4-layer attention-only toy transformer**, not a pretrained
language model.

**The origin post is the most self-limiting of the fifteen.** Full model 56% success; the isolated
eight-head circuit 42%; circuit plus three further heads 58%. The authors state the circuit
"recovers up to half of the model performance" and name unexamined heads and unresolved composition
relationships.

**The origin addressed the rival hypothesis rather than leaving it open.** The authors' label is
"Docstring Induction," not "variable binding" — that phrase appears nowhere in the post. They name
the competing account explicitly as "line number based," design prompts to suppress it at a cost of
roughly 75% to 56% performance, and conclude that "at least the first two algorithms are implemented
to some degree." Head 0.4 "derives positional information from the causal attention mask rather than
positional embeddings," and that positional signal feeds *into* the induction step rather than
replacing it.

### Timeline

The docstring circuit's entire follow-up literature treats it as **benchmark task #3** for circuit
discovery methods. No paper located re-derives the mechanism, tests the variable-binding
interpretation, or extends it to a real language model.

| Date (arXiv v1) | Work | Direction | What it showed |
|---|---|---|---|
| 2023-04-28 | Conmy, Mavor-Parker, Lynch, Heimersheim & Garriga-Alonso, arXiv:2304.14997 | **used as benchmark** | ACDC evaluated on Docstring among six tasks. Notes a limitation that applies to it: single-metric methods "systematically miss internal model components such as the 'negative' components found in previous work (IOI, Docstring)." An origin author is a co-author. |
| 2023-10-16 | Syed, Rager & Conmy, arXiv:2310.10348 | **qualifies (method-dependence)** | On Docstring, "ACDC used with the KL Divergence metric outperforms EAP," reversing the ordering that holds on IOI and Greater-Than. The approximation-quality check — R² = 0.27, best-fit gradient 0.531 — is run on Docstring, and it is poor. |
| 2024-05-21 | O'Neill & Bui, arXiv:2405.12522 | **used as benchmark** | SAE-based discovery reports higher precision and recall recovering ground-truth circuits on docstring completion. "Ground truth" here means the Heimersheim & Janiak circuit. |
| 2024-07-01 | Hsu et al., arXiv:2407.00886 | **used as benchmark** | Contextual decomposition "outperforms ACDC and EAP by better recovering the manual circuits" on docstring completion. |
| 2024-07-11 | Miller, Chughtai & Saunders, arXiv:2407.08734 | **qualifies** | Docstring is one of four case studies establishing that faithfulness scores "reflect both the methodological choices of researchers as well as the actual components of the circuit." |
| 2024-07-21 | **uit de Bos & Garriga-Alonso, arXiv:2407.15166** | **contradicts** | Over 1,000,000 clean/corrupted pairs, model-vs-circuit KL has mean 3.91, median 3.66, max **12.07**, with the worst points "more than 5 standard deviations away from the mean." "The circuits for the IOI and docstring tasks fail to behave similarly to the full model **even on completely benign inputs from the original task**." |

### Turning points

- **2024-07-21 (17 months):** the only result that directly tests the circuit as a *claim about the
  model* rather than as a target for method benchmarking, and it fails. This is the single turning
  point in the timeline.
- **There is no upward turning point.** No paper strengthens the claim. Every entry either uses it
  as a fixed target or weakens it.

### Current state versus origin

**Weaker than at origin, and the origin was already hedged.** The circuit recovered 42% of a 56%
baseline when published; it now additionally fails to match the model on benign in-distribution
inputs by a wide and heavy-tailed KL margin.

**A circular-validation problem specific to this claim.** Four method papers score themselves on
how well they recover the Heimersheim & Janiak circuit, treating an unreviewed blog post's
eight-head set as ground truth. A method that recovers it perfectly recovers a circuit known to
explain under half the model's behavior. The claim's function in the literature is as a fixed
point, and being a fixed point insulates it from testing.

**The interpretive question was answered at origin and not revisited since.** The authors tested the
positional rival and reported a partial result, so the open question is how much each account
contributes, not which one holds. No subsequent work has taken it up.

**Reported as quiet, with a structural reason.** The claim lives on a 4-layer attention-only toy
model with no publication of record. Searches run: the term "docstring" with circuit and
interpretability across arXiv abstracts, and the full IOI-adjacent literature index of 37 papers.

## 12. Knowledge neurons — [COMPLETE]

### Origin

**Dai, Dong, Hao, Sui, Chang & Wei, "Knowledge Neurons in Pretrained Transformers,"
arXiv:2104.08696, v1 2021-04-18** (ACL 2022). **The oldest claim of the fifteen** — 63 months of
follow-up literature.

Claim: factual knowledge is stored in identifiable **knowledge neurons** in transformer
feed-forward layers. "Activation of such knowledge neurons is positively correlated to the
expression of their corresponding facts," and facts can be updated or erased by manipulating those
neurons without fine-tuning.

Evidence at origin: integrated-gradients attribution over FFN neurons, suppression and amplification
of identified neurons with measured effects on fact expression, and knowledge editing and erasure
demonstrations.

**The claim bundles three separable propositions**, and the follow-up literature separated them:
(1) attribution identifies neurons whose manipulation changes fact expression; (2) those neurons
*store* the fact; (3) storage location tells you where to edit.

### Timeline

| Date (arXiv v1) | Work | Direction | What it showed |
|---|---|---|---|
| 2022-02-10 | Meng, Bau, Andonian & Belinkov (ROME), arXiv:2202.05262 | **supports** | Causal tracing localizes factual prediction to "a distinct set of steps in middle-layer feed-forward modules" processing subject tokens, and rank-one editing there changes facts. Independent method, converging localization. |
| 2022-05-03 | Juneja et al., arXiv:2205.01366 | **qualifies (refines)** | Middle layers carry relational information; later layers refine to specific facts. The neuron set is not homogeneous. |
| **2023-01-10** | **Hase, Bansal, Kim & Ghandeharioun, arXiv:2301.04213** | **contradicts (proposition 3)** | "Does Localization Inform Editing?" Facts can be changed by editing weights **in different places than localization identifies**. Representation-denoising results "do not provide any insight into which model MLP layer would be best to edit," and "which layer we edit is a far better predictor of performance." Better mechanistic localization does not yield better editing. |
| 2023-07-24 | Cohen, Biran, Yoran, Globerson & Geva, arXiv:2307.12976 | **contradicts (specificity)** | RippleEdits, 5,000 edits testing downstream consequences. "Current methods fail to introduce consistent changes in the model's knowledge" — a successful single-fact edit does not propagate to logically entailed facts. A simple in-context strategy beats the established weight-editing methods. |
| 2023-08-25 | Chen et al., arXiv:2308.13198 | **qualifies (specificity)** | **Degenerate** knowledge neurons: "different knowledge neurons can store the same fact." Also finds language-independent neurons. Localization is one-to-many, so an identified neuron is not *the* storage site. |
| 2023-12-17 | Nori et al., arXiv:2312.10770 | **supports (generalization)** | Knowledge neurons identified in protein language models, with high density in self-attention key-vector networks. The method transfers to a non-linguistic domain. |
| 2024-02-21 | Chen et al., arXiv:2402.13731 | **qualifies (formalizes)** | Degenerate knowledge neurons defined rigorously and linked to robustness and complexity. |
| **2024-05-03** | **Niu, Liu, Zhu & Penn, arXiv:2405.02421** | **contradicts (proposition 2, the construct)** | "What does the Knowledge Neuron Thesis Have to do with Knowledge?" The same editing methods that support the thesis also modify **linguistic phenomena unrelated to factual recall**, so the mechanism is not fact-specific. "While the MLP weights store complex patterns that are interpretable both syntactically and semantically, these patterns do not constitute 'knowledge'." The thesis "does not adequately explain the process of factual expression." |
| 2024-05-23 | Chen et al., arXiv:2405.14117 | **qualifies** | "Knowledge Localization: Mission Not Accomplished?" Knowledge storage is less rigid than assumed, and attention mechanisms play a larger role than the neuron account allows. |
| 2024-08-06 | Wang et al., arXiv:2408.03247 | **qualifies** | Knowledge-neuron activation does not guarantee correct reasoning; models "fail to harness critical factual associations" they demonstrably contain. |
| 2024-11-26 | Cao et al., arXiv:2411.17401 | **supports** | Language-agnostic knowledge neurons refined with uncertainty quantification — cross-lingual storage confirmed. |
| 2025-03-29 | Sato et al., arXiv:2503.22941 | **supports (generalization)** | Knowledge neurons localized in multimodal vision-language transformers. |
| 2026-01-09 | Voria et al., arXiv:2601.05663 | **supports (transfer)** | Knowledge-neuron attribution adapted to stereotypes: "biased knowledge is localized within small neuron subsets" analogous to factual knowledge. |
| **2026-04-06** | **Balogh et al., arXiv:2604.04756** | **contradicts (proposition 2, mechanistically)** | "Knowledge neurons function as **routing infrastructure rather than fact storage**," with the MLP amplifying signals arriving from attention rather than holding the fact. A mechanistic account of what the neurons do instead. |

### Turning points

- **2023-01-10 (21 months):** Hase et al. severs localization from editing. This is the first
  contradiction and it targets the claim's main practical justification.
- **2023-07-24 (27 months):** the specificity failure is quantified at scale. Edits do not
  propagate to entailed facts — the "editing corrupts related facts" problem, measured.
- **2024-05-03 (37 months):** Niu et al. attacks the construct. Showing the same editing machinery
  moves syntax as well as facts is a discriminant-validity argument: the intervention is not
  selective for the construct it names.
- **2026-04-06 (60 months):** the routing account supplies the positive alternative that the
  earlier critiques lacked. Before this date the literature said what knowledge neurons are not;
  after it, there is a competing account of what they are.

### Current state versus origin

**Proposition 1 survives and has generalized far beyond the origin.** Attribution locates neurons
whose manipulation changes fact expression, and this replicates in protein language models,
vision-language models, multiple languages, and for stereotype associations. The *method* is the
most portable of the fifteen claims.

**Proposition 2 — that these neurons store the fact — has been contradicted twice, on independent
grounds.** The same machinery moves non-factual linguistic phenomena (2024-05), and a mechanistic
account puts the MLP in a routing rather than a storage role with the signal originating in
attention (2026-04). Storage is also one-to-many: degenerate neurons store the same fact
redundantly.

**Proposition 3 — that localization tells you where to edit — was contradicted at 21 months and
has not recovered.** Editing layer predicts editing success better than localization does.

**Specificity is the persistent failure.** Strong intervention effects with weak selectivity was
visible in the origin and has been confirmed by every study that looked: degenerate neurons,
non-factual editing effects, and ripple-effect failures on entailed facts.

**Shape of the literature.** This is the claim with the longest record and the clearest structure:
a method that works and generalizes, wrapped in a storage interpretation that three independent
lines of work reject. The name outlived the mechanism it named.

## 13. SAE features — [COMPLETE]

### Origin

**Cunningham, Ewart, Riggs, Huben & Sharkey, "Sparse Autoencoders Find Highly Interpretable
Features in Language Models," arXiv:2309.08600, v1 2023-09-15** (ICLR 2024). Anthropic's
"Towards Monosemanticity" (Bricken et al., Transformer Circuits Thread, **2023-10**) is the
concurrent second origin and carries most of the field's citation weight.

Claim: sparse dictionary learning on model activations recovers **highly interpretable, more
monosemantic features** than neurons, resolving superposition into its constituent directions.
These features are the appropriate unit of analysis.

Evidence at origin: automated interpretability scores exceeding those of neurons and other
decomposition baselines, plus case studies of individual features.

**The claim has a strong and a weak form**, and the field adopted the strong one: that SAE features
are the model's features — atomic, canonical, and model-properties rather than
dictionary-properties.

### Timeline

| Date (arXiv v1) | Work | Direction | What it showed |
|---|---|---|---|
| 2024-05 | Templeton et al., Transformer Circuits Thread | **supports (scale)** | Dictionary learning at production scale, recovering millions of features with steering demonstrations. |
| 2024-06 | Gao et al., arXiv:2406.04093 | **supports (scale)** | Scaling laws for SAE training and improved evaluation metrics. |
| **2024-09-22** | **Chanin, Wilken-Smith, Dulka, Bhatnagar, Golechha & Bloom, arXiv:2409.14507** | **contradicts (atomicity)** | **Feature absorption**: parent features fail to activate and are absorbed into child features, so hierarchical splitting is unstable. Validated across many LLM SAEs, and "adjusting SAE configurations alone cannot resolve this issue." Features have dependency relations rather than independence. |
| **2025-01-28** | **Wu, Arora, Geiger, Wang, Huang, Jurafsky, Manning & Potts (AxBench), arXiv:2501.17148** | **contradicts (utility)** | "Even Simple Baselines Outperform Sparse Autoencoders." On steering, "prompting outperforms all existing methods, followed by finetuning," and "SAEs are not competitive." |
| **2025-01-28** | **Paulo & Belrose, arXiv:2501.16615** | **contradicts (canonicity)** | SAEs differing **only in random seed** learn different features: in a 131K-latent SAE on Llama-3-8B, **only 30% of features were shared across seeds**. Holds across three LLMs, two datasets, several architectures; TopK SAEs are *more* seed-dependent than ReLU. Conclusion: features are "a pragmatically useful decomposition of activation space, rather than an exhaustive and universal list of features truly used by the model." |
| **2025-01-29** | **Heap, Lawson, Farnik & Aitchison, arXiv:2501.17727** | **contradicts (construct)** | "SAEs trained on **randomly initialized transformers** produce auto-interpretability scores and reconstruction metrics that are similar to those from trained models." The origin paper's headline metric does not distinguish a trained model from noise. |
| **2025-02-07** | **Leask, Bussmann, Pearce, Bloom, Tigges, Al Moubayed, Sharkey & Nanda, arXiv:2502.04878** | **contradicts (canonicity)** | "Sparse Autoencoders Do Not Find Canonical Units of Analysis." Larger dictionaries recover latents smaller ones miss, and a single latent decomposes into finer ones. |
| **2025-02-23** | **Kantamneni, Engels, Rajamanoharan, Tegmark & Nanda, arXiv:2502.16681** | **contradicts (utility)** | "Are Sparse Autoencoders Useful?" Across data scarcity, class imbalance, label noise, and covariate shift, no SAE-plus-baseline ensemble consistently beats baseline-only ensembles. Promising applications — spurious correlations, dataset quality, multi-token probes — are matched by simple non-SAE baselines. Notably, two authors are among the field's leading SAE proponents. |
| 2025-04 | Mueller et al. (MIB), arXiv:2504.13151 | **contradicts (causal localization)** | On the Mechanistic Interpretability Benchmark, SAE features localize causal variables no better than raw neurons. |
| 2026-05-29 | Nelson et al., arXiv:2605.31245 | **qualifies (partial fix)** | Standard SAEs show high instability across training runs; an identifiable variant improves stability under approximate identifiability conditions. |
| 2026-05-29 | Jørgensen et al., arXiv:2605.31183 | **disputes the critique** | "Steering LLMs? **Actually**, Sparse Autoencoders can outperform simple baselines" — comparable to LoRA with proper feature selection; high sparsity may be unnecessary. A direct rebuttal to AxBench 16 months later. |
| 2026-06-10 | Gerasimov et al., arXiv:2606.12138 | **qualifies (rescues part of it)** | Unstable individual features concentrate in **reproducible low-rank subspaces**, so seed dependence reflects basis ambiguity rather than noise. The *subspace* is canonical even though the *features* are not. |
| 2026-06-22 | Grandien et al., arXiv:2606.22994 | **qualifies** | Feature absorption systematically degrades concept hierarchies, though SAEs still provide a reasonable basis for them. |
| 2026-06-23 | Klotz et al., arXiv:2606.24716 | **qualifies** | Moderate dictionary sizes are most interpretable; increased overcompleteness *reduces* perturbation alignment. Bigger is not better. |
| **2026-07-13** | Bal et al., arXiv:2607.12166 | **contradicts** | A reproducible causal audit finds **up to 77% of high-cosine-similarity features are causally inert** — geometric alignment and causal effect come apart. |
| 2026-07-22 | Cho et al., arXiv:2607.20596 | **qualifies** | Cross-family causal stability of single-token features varies substantially; training methodology matters more than activation function. |
| 2026-07-27 | Hoang et al., arXiv:2607.24645 | **qualifies** | SAE features often lack stable steering directions; value-like features have structured effects while pointer-like features are diffuse and context-dependent. |

### Turning points

- **2024-09-22 (12 months):** feature absorption is the first structural contradiction, and it is
  shown to be unfixable by hyperparameter choice.
- **2025-01-28 to 2025-02-23 (four weeks, 16–17 months):** the decisive window. Four independent
  groups publish, within 26 days, that SAE features are seed-dependent (30% overlap), that
  interpretability metrics do not distinguish trained from random transformers, that features are
  not canonical, and that SAEs do not beat simple baselines on steering or probing. **This is the
  densest cluster of contradicting evidence anywhere in this document.**
- **2026-06-10 (33 months):** the first result that partially rescues the claim by relocating it —
  subspaces are reproducible even where features are not.
- **2026-05-29:** AxBench is directly rebutted, with the rebuttal's title constructed as a reply.
  **Contradiction left standing.**

### Current state versus origin

**The weak form survives.** Sparse dictionary learning yields a useful, more-interpretable-than-
neurons decomposition of activation space, and this is what Paulo & Belrose explicitly endorse.

**The strong form does not.** Features are not atomic (absorption, decomposition under larger
dictionaries), not canonical (30% cross-seed overlap), not better than baselines at steering or
probing, no better than neurons at causal localization, and up to 77% causally inert where
geometrically aligned.

**The construct-validity problem is the most severe of the fifteen.** The origin metric —
automated interpretability score — produces similar values on randomly initialized transformers.
A measure that cannot distinguish a trained model from noise cannot establish that recovered
features are model properties.

**Notable feature of this timeline: the contradictions come from inside.** Nanda, Bloom, and
Sharkey are co-authors on both foundational SAE work and on the papers showing features are
non-canonical, absorbed, and no better than baselines. This is a field correcting itself quickly
rather than a claim defended against outsiders — the opposite of the ClinGen pattern, where low-tier
associations persisted uncontested for years.

## 14. Probing classifiers — [COMPLETE]

### Origin

The audit anchors this claim to **Belinkov, "Probing Classifiers: Promises, Shortcomings, and
Advances," Computational Linguistics 48(1), 2022**. That is a *survey*, and this claim's temporal
structure is unlike the other fourteen: **the method's origin and the survey that names it are six
years apart, and every major qualification falls between them.**

The method originates with **Alain & Bengio, arXiv:1610.01644 (2016-10)** and contemporaneous work
by Shi et al. and Adi et al. (both 2016).

Claim, as used in practice: training a classifier on a model's internal activations to predict a
property, and reading high accuracy as evidence the model **represents and uses** that property.

Evidence at origin: classification accuracy above chance, benchmarked against a majority baseline.

**Belinkov's 2022 survey is itself a statement of the limitation**, and its subtitle says so. The
temporal question here is therefore not "did later work contradict it" but "how long did the method
travel on the strong reading after the limitation was published."

### Timeline

| Date | Work | Direction | What it showed |
|---|---|---|---|
| 2016-10 | Alain & Bengio, arXiv:1610.01644 | **origin (method)** | Linear classifier probes for reading properties off intermediate layers. |
| **2019-09-08** | **Hewitt & Liang, arXiv:1909.03368** | **contradicts (measurement)** | Control tasks — words paired with random outputs. "A good probe should be selective, achieving high linguistic task accuracy and low control task accuracy." Popular probes on ELMo are **not selective**: they reach high accuracy partly by memorizing word-type associations rather than reading structure off the representation. Accuracy alone is uninformative without a matched control. |
| **2020-05-02** | **Ravichander, Belinkov & Hovy, arXiv:2005.00719** | **contradicts (task relevance)** | "Does Probing Accuracy Entail Task Relevance?" No. Models "encode linguistic properties even if they are not needed for the task," and encode properties "considerably above chance-level even when distributed in the data as random noise." Belinkov is an author, two years before the survey. |
| **2020-06-01** | **Elazar, Ravfogel, Jacovi & Goldberg, arXiv:2006.00995** | **contradicts (causal)** | Amnesic probing removes a property by causal intervention and measures the behavioral effect. Finding: "**conventional probing performance is not correlated to task importance**." The authors "call for increased scrutiny of claims that draw behavioral or causal conclusions from probing results." |
| 2020 | Voita & Titov, arXiv:2003.12298; Pimentel et al., arXiv:2004.03061 | **qualifies (formal)** | Information-theoretic reframings: probe accuracy conflates the property's presence with the probe's own capacity; under a mutual-information framing the quantity probing purports to measure is degenerate. |
| **2022-07-08** | **Kumar, Tan & Sharma, arXiv:2207.04153** | **contradicts (downstream use)** | Probing classifiers are unreliable for concept removal and detection. Proved: "even under the most favorable conditions... when a concept's relevant features in representation space alone can provide 100% accuracy," a probe is likely to use non-concept features, so removal methods built on probes fail and "in the worst case may end up destroying all task-relevant features." Confirmed on synthetic, Multi-NLI, and Twitter data. |
| **2022** | **Belinkov, Computational Linguistics 48(1)** | **the survey — states the limitation** | "Promises, Shortcomings, and Advances." Consolidates the above. Published **three years after** Hewitt & Liang and **two years after** amnesic probing. |
| **2023-03-05** | **Geiger, Wu, Potts, Icard & Goodman (DAS), arXiv:2303.02536** | **the repair** | Distributed alignment search: find alignments between interpretable causal variables and distributed representations by gradient descent, allowing neurons multiple roles. Supplies the causal follow-up whose absence is the probing claim's ceiling. |
| 2023-11 | Makelov, Lange & Nanda, arXiv:2311.17030 | **qualifies (the repair)** | Subspace activation patching — the causal method meant to fix probing — admits interpretability illusions of its own. |
| 2025–2026 | SAE-feature critiques (§13) | **inherited** | Every construct-validity failure of SAE features is a probing failure at one remove: automated interpretability scores do not distinguish trained from random transformers (arXiv:2501.17727), and up to 77% of geometrically aligned features are causally inert (arXiv:2607.12166). |
| 2026-07-12 | arXiv:2607.13075 | **qualifies (contemporary)** | "Activation-Space Probes as Risk Detectors, Not Context Adjudicators" — probes detect the presence of a risk signal without adjudicating context. The 2019 limitation restated for a safety application seven years later. |

### Turning points

- **2019-09-08:** control tasks. Any assessment after this date must ask for selectivity, and most
  published probing results do not report it.
- **2020-06-01 (the decisive one):** amnesic probing establishes empirically that probe accuracy and
  causal importance are **uncorrelated**. This is the strongest available statement of the ceiling
  and it is 25 years' worth of citations old in field-time — six years before the present.
- **2023-03-05:** DAS makes the causal upgrade routine, converting the ceiling from a permanent
  limit into a missing step.

### Current state versus origin

**The limitation is settled, has been settled since 2020, and was settled by the same author the
audit cites for it.** Nothing in the last six years disputes that decodability without intervention
fails to establish use. There is no live controversy here.

**The method's evidential reach is bounded, and the bound is well characterized in four independent
ways**: no selectivity without control tasks (2019), no task relevance from accuracy (2020),
no correlation with causal importance (2020), and provable failure of probe-based concept removal
even under ideal conditions (2022).

**The repair exists and predates most of the claims that still need it.** Causal follow-up via
DAS or amnesic-style intervention has been available since 2020–2023.

**The finding worth stating plainly: this is the only claim of the fifteen where the qualifying
evidence entirely predates the citation the field anchors to.** The limitation was published in
2019–2020; the survey naming it appeared in 2022; probing results reported without control tasks or
causal follow-up continued to appear throughout. The problem is not that the evidence was absent —
it is that a settled methodological result did not change practice.

## 15. Gender bias circuits — [COMPLETE]

### Origin

**Vig, Gehrmann, Belinkov, Qian, Nevo, Singer & Shieber, "Causal Mediation Analysis for
Interpreting Neural NLP: The Case of Gender Bias," arXiv:2004.12265, v1 2020-04-26** (NeurIPS 2020,
where it appeared as "Investigating Gender Bias in Language Models Using Causal Mediation
Analysis"). **The second-oldest claim of the fifteen.**

Claim: gender bias in language models is mediated by identifiable components. Bias effects are
"sparse, concentrated in a small part of the network" and decomposable into direct and indirect
effects flowing through specific neurons and attention heads.

Evidence at origin: causal mediation analysis — a genuinely causal method, and one imported from
epidemiology rather than invented for the setting. Per-neuron and per-head total, direct, and
indirect effects.

**The presupposition that later became the problem:** that "gender bias" and "legitimate gender
knowledge" name separable things in the representation. The origin paper does not test this, and
does not claim to.

### Timeline

| Date (arXiv v1) | Work | Direction | What it showed |
|---|---|---|---|
| 2021-12-13 | De Cao et al., arXiv:2112.06837 | **supports (sparsity)** | Differentiable masking finds small neuron subsets mediating gender-bias behavior in LSTMs. Does not distinguish bias from legitimate gender knowledge. |
| 2022-07-06 | Joniak & Aizawa, arXiv:2207.02463 | **qualifies (first signal)** | Movement pruning to locate bias-containing regions identifies a **bias-performance trade-off** — the first published indication that the surgery costs capability. |
| **2023-10-19** | **Chintam, Beloch, Zuidema, Hanna & van der Wal, arXiv:2310.12611** | **supports (convergence) + qualifies (construct)** | Three causal-discovery methods — mediation analysis, automated circuit discovery, and DiffMask+ — show "significant overlap in the identified components despite huge differences in computational requirements." Mitigation works with less damage than full fine-tuning. But the paper "underscores **the difficulty of defining and measuring bias**, and the sensitivity of causal discovery procedures to dataset choice." Method convergence, construct doubt. |
| 2023-12-24 | Zayed et al., arXiv:2312.15398 | **supports (intervention)** | Fairness-aware structured pruning reduces bias 8–39.5% while preserving performance. |
| **2024-01-12** | **Leteno et al., arXiv:2401.06495** | **contradicts (localization)** | In BERT and DistilBERT, bias is **not localized**: "every attention head uniformly encodes bias," except in underrepresented classes. Directly opposes the origin claim's sparsity finding, in a different architecture family. |
| 2024-03-21 | Cai et al., arXiv:2403.14409 | **supports (localization)** | Causal mediation identifies bottom MLPs and top attention modules as primary bias contributors in decoder-only LLMs. |
| 2024-06-18 | Prakash et al., arXiv:2406.12347 | **supports (refines)** | Feature-based methods differentiate MLP and attention-head roles in bias propagation. |
| **2025-01-24** | **Yu & Ananiadou, arXiv:2501.14457** | **qualifies (the therapeutic window)** | Distinguishes *gender neurons* from *general neurons* within bias circuits, and cautions that "editing even a small number of **general** neurons can disrupt the model's overall capabilities." The first result to locate the damage mechanism, and it implies the two populations are at least partly distinguishable. |
| 2025-03-20 | Dasu et al., arXiv:2503.15815 | **supports (intervention)** | Attention pruning by simulated annealing reduces gender bias up to 40%. |
| 2025-05-13 | Manna et al., arXiv:2505.08546 | **qualifies (construct)** | In machine translation, models "ignore available gender cues in most cases" in favour of stereotypes; masculine cues get a more diffuse response than feminine. Bias and gender *processing* interact rather than sit in separate channels. |
| **2026-05-12** | **Veloso & Schütze, "GKnow: Measuring the Entanglement of Gender Bias and Factual Gender," arXiv:2605.12299** | **the direct test — supports the entanglement claim** | Curates a benchmark separating factually gendered predictions from stereotypically biased ones, identifies circuits and neurons for each, and runs ablation against GKnow, DiFair, and StereoSet. Finding: "**gender bias and factual gender are severely entangled on the level of both circuits and neurons, entailing that ablation is an unreliable debiasing method.**" Standard bias benchmarks "hide the decrease in factual gender knowledge" caused by ablation. |
| 2026-05-19 | Pearman et al., arXiv:2605.20410 | **qualifies** | Chain-of-thought prompting gives "only superficial mitigation"; bias "remains embedded in hidden representations." |

### Turning points

- **2022-07-06 (27 months):** the bias-performance trade-off appears, unnamed, as a practical
  finding in a pruning paper.
- **2023-10-19 (42 months):** three independent causal methods converge on the same components
  while the same paper raises the construct problem. Convergent *measurement* validity alongside
  weak *construct* validity — an unusual combination.
- **2024-01-12 (45 months):** the sparsity finding fails to replicate in encoder models. This would
  have lowered an assessment of the localization claim on that date.
- **2026-05-12 (73 months):** the decisive test. This is the longest origin-to-decisive-test
  interval in this document by a wide margin — **just over six years.**

### Current state versus origin

**The localization claim is architecture-dependent.** Sparse, localized mediation replicates in
decoder-only models and fails in BERT and DistilBERT, where bias is uniformly distributed across
heads.

**The separability presupposition has now been tested directly, and it fails.** Bias and factual
gender are "severely entangled at the level of both circuits and neurons," and ablation is
therefore unreliable as a debiasing method. The construct problem is no longer an argument from the
absence of evidence — there is evidence, and it points at entanglement.

**A measurement-validity finding worth stating separately:** standard gender-bias benchmarks
*conceal* the loss of factual gender knowledge that ablation causes. Every mitigation paper in this
timeline that reported bias reduction with "preserved performance" measured performance on
instruments now shown to be blind to the relevant damage. That includes the 8–39.5% and up to 40%
reduction results above.

**One qualification to the entanglement finding.** Yu & Ananiadou's gender-neuron / general-neuron
distinction suggests partial separability, and it predates GKnow by 16 months. The two are not
squarely in conflict — one reports a distinction among neurons, the other reports entanglement of
the circuits and neurons carrying the two constructs — but they have not been reconciled.

**Note on prior characterization.** An earlier draft of the audit recorded that "no subsequent study
has directly tested whether bias and grammatical-gender knowledge are separable." As of 2026-05-12,
one has. The result agrees with the audit's reasoning and replaces its argument-from-gap with
evidence.

---

## Final Measurements

### Master table

Origin dates are earliest public version. "First Q/C" is the first qualifying or contradicting
result. Intervals in months.

| # | Claim | Origin | Strongest support | Δ | First Q/C | Δ | Outcome |
|---|---|---|---|---|---|---|---|
| 1 | Grokking / Fourier | 2023-01 | 2023-11 Morwani | 10 | 2023-01 own appendix | **0** | contradicted |
| 2 | Induction heads | 2022-03 | 2025-05 Yang 70B | 38 | 2024-02 Rushing | 23 | contradicted (broad) |
| 3 | Greater-Than | 2023-04 | 2024-07 uit de Bos | 15 | 2024-03 Hanna | 11 | contradicted |
| 4 | Copy suppression | 2023-10 | 2025-07 Campregher | 21 | 2023-10 Merullo (+5 days) | **0.2** | qualified only |
| 5 | IOI | 2022-11 | 2024-07 Tigges | 20 | 2023-04 Conmy | 5 | contradicted |
| 6 | Superposition | 2022-09 | 2025-05 Liu | 32 | 2023-12 Lecomte | 15 | qualified only |
| 7 | Refusal direction | 2024-06 | 2025-05 Wang | 11 | 2024-07 Tan | **1** | contradicted |
| 8 | Global workspace | 2026-07 | — (origin) | 0 | **none** | — | silent |
| 9 | Successor heads | 2023-12 | 2024-10 Levy & Geva | 10 | 2024-10 Nikankin | 10.5 | contradicted |
| 10 | Othello world model | 2022-10 | 2025-03 Yuan & Søgaard | 29 | 2023-03 Nanda | 5 | contradicted |
| 11 | Docstring | 2023-02 | **none** | — | 2023-10 Syed | 8 | contradicted |
| 12 | Knowledge neurons | 2021-04 | 2022-02 ROME | 10 | 2023-01 Hase | 21 | contradicted |
| 13 | SAE features | 2023-09 | 2024-05 Templeton | 8 | 2024-09 Chanin | 12 | contradicted |
| 14 | Probing classifiers | 2016-10 | **none** | — | 2019-09 Hewitt & Liang | 35 | contradicted |
| 15 | Gender bias circuits | 2020-04 | 2023-10 Chintam | 42 | 2022-07 Joniak | 27 | contradicted |

### 1. Time from origin to strongest supporting evidence

**Median 17.5 months** (n = 12 with an identifiable strongest-support date, excluding the 26-day-old
workspace claim). Range 8 to 42 months.

**Two claims have no supporting follow-up at all.** The docstring circuit has been used as a
benchmark target four times and confirmed zero times. Probing classifiers never had a result raise
the method's evidential ceiling — every development lowered it or supplied a replacement.

### 2. Time from origin to first qualifying or contradicting result

**Median 11 months** (n = 14). Range 0 days to 35 months.

**14 of 15 have one.** The single exception, the global workspace claim, is 26 days old.

Four claims were qualified within a year, three of them within a month:
- Grokking / Fourier: **same document.** The necessity counterexample is in the origin paper's own
  Table 5.
- Copy suppression: **5 days.**
- Refusal direction: **1 month.**
- IOI: 5 months. Othello: 5 months.

### 3. How many have been qualified or contradicted

**14 of 15 qualified or contradicted. 12 of 15 contradicted** — a direct empirical conflict with the
claim as originally scoped or with an explicitly stated sub-claim.

Two are qualified without contradiction: **copy suppression** (the mechanism holds; its relation to
any given task varies by model) and **superposition** (the core representational claim holds; the
diagnostic inference from polysemanticity and the one-dimensional-feature premise do not).

One is silent: **global workspace / J-space**, too recent to have a timeline.

### 4. Do claims strengthen or weaken with time?

**Both, and the split is the finding: the mechanism strengthens while the scope narrows.** In
almost every case the claim decomposes into a narrow empirical result that survives and gets better
supported, and a broader reading that does not survive.

| Claim | What strengthened | What did not survive |
|---|---|---|
| Induction heads | token copying, now ablated at 70B | general in-context learning |
| Othello | board state linearly decodable, 7 architectures, 99% | the nonlinearity claim; "world model" as a licensed label |
| Knowledge neurons | attribution + intervention, portable to proteins and vision | that the neurons *store* the fact; that localization guides editing |
| Refusal direction | bidirectional control, 14 languages, OV-circuit mechanism | "single" |
| SAE features | a useful decomposition of activation space | atomic, canonical, better than baselines |
| Superposition | more features than dimensions, with a scaling law | features as one-dimensional directions |
| Grokking / Fourier | the Fourier feature basis, provably forced | that the composed algorithm is unique; the grokking/mechanism bundle |
| Successor heads | mod-10 / per-digit substrate | cross-architecture universality |
| IOI | the three-step algorithm across models and scales | the 87% number; minimality; edge-level uniqueness |
| Gender bias | three causal methods converge on the same components | that bias and factual gender are separable |

Four claims weakened without a compensating narrow core: **docstring**, **probing classifiers**,
**greater-than** (whose generalization claim failed with no supporting result to offset it), and
**SAE features** in the strong form the field adopted.

### 5. Contradictions still live

Four disputes have a published rebuttal and no resolution:

| Dispute | Contradiction | Rebuttal | Gap |
|---|---|---|---|
| IOI MLP8 subspace illusion | Makelov 2023-11 | Wu et al. 2024-01 | 2 months |
| SAE steering vs baselines | AxBench 2025-01 | Jørgensen 2026-05 | 16 months |
| Compressed computation | Bhagat 2026-06 | arXiv:2607.04800 2026-07 | 3 weeks |
| IOI minimality | Shi 2024-10 | Li & Janson 2024-09 | concurrent |

And one claim **recovered** after being weakened: IOI necessity failed under first-order ablation
from 2022 to 2026, and Gong et al. (2026-07) restored it by showing the failure was an additivity
artifact — first-order methods miss backups that are dormant until the primaries are removed.

### 6. The qualification is often already in the origin paper

This is the most consistent structural pattern in the fifteen, and it has no ClinGen analogue.

| Claim | The origin paper's own disclosure |
|---|---|
| Induction heads | Argument 6 names the exact scale refutation later work confirmed; "only suggestive for the MLP case" |
| Grokking / Fourier | Table 5 contains non-grokking models with the same mechanism; §5.2 says the circuit forms before grokking |
| IOI | greedy completeness search fails at 87% of the logit difference; Name Mover knockout costs only 5% |
| Docstring | circuit recovers 42% against a 56% baseline; "up to half of the model performance" |
| Superposition | framed explicitly as a toy model, not a demonstration in real networks |
| Probing (Belinkov survey) | the limitation is the subtitle |
| Global workspace | four method limitations stated, including that the J-lens captures the structure only approximately |

In at least seven of fifteen, the strongest early qualification was published *by the original
authors, in the original document*, and did not travel with the claim.

---

## Comparison to ClinGen

**ClinGen's result.** Re-simulating 30 gene–disease curations at one-year increments from first
publication, using only evidence available at each date: associations that sat at a **low tier for
five or more years** were the ones that failed. Of 8 such associations, **3 became Disputed or
Refuted**. The mechanism is *evidence starvation* — a claim that stopped accumulating support was
eventually reclassified downward, and reclassification was terminal.

**The mechanistic interpretability result has the opposite shape on three axes.**

**Rate.** ClinGen: 3 of 8 long-stalled associations refuted, roughly 10% of the full set of 30.
Here: **12 of 15 contradicted, 14 of 15 qualified**. Contradiction is the normal outcome, not the
exception.

**Speed.** ClinGen's downgrades required five or more years of stasis. Here the median time to
first qualification is **11 months**, and three claims were qualified within a month of
publication. Two were qualified before or on the day of publication, by their own authors.

**Direction of the correlation with attention.** This is the sharp inversion. In ClinGen, the
claims that failed were the **quiet** ones — nobody looked, evidence never arrived, the tier fell.
Here, the claims with the most contradiction are the **loudest**: IOI has 37 follow-up papers and
the most contested headline number in the field; SAE features drew four independent
contradictions in a 26-day window in early 2025. The quiet claims — docstring, successor heads,
global workspace — are not refuted. They are **untested**, which is a different state and one this
document keeps distinct throughout.

**Terminality.** ClinGen's Refuted verdicts settle a question. Here, four contradictions have
published rebuttals and remain open, and one claim recovered after four years by showing the
disconfirming measurement was methodologically incomplete. Contradiction in this field is a stage
in a dispute rather than an endpoint.

**What is genuinely analogous.** ClinGen's core insight — that a verdict is a function of the date
it was assigned — holds here and holds harder. Assessments of IOI made before and after 2024-07,
of the refusal direction before and after 2025-02, of SAE features before and after 2025-01, and of
gender bias before and after 2026-05 differ so much that a verdict without a date attached carries
little information.

**Where the analogy breaks, and what replaces it.** ClinGen was diagnosing a *pipeline* problem:
evidence that should have arrived did not. The pattern here is a *scoping* problem: the evidence
arrives quickly, it is usually good, and it almost always shows that the claim as stated reached
further than the experiment supported. The narrow result survives; the reach does not. And in
roughly half the cases, the original authors said so at the time and the field cited the headline
anyway.

The ClinGen question — do claims stall at a low tier and then get refuted? — has the answer **no**
for this field. The productive question is the one the data actually poses: **claims do not fail
from lack of evidence; they fail at the boundary between what was measured and what was asserted,
and that boundary is usually visible on the day of publication.**
