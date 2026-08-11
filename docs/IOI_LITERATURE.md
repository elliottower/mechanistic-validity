# The IOI Circuit: A Standing Literature Reference

Scope: work bearing on the indirect object identification (IOI) circuit in GPT-2, from Wang et al. (arXiv:2211.00593) onward. Includes follow-ups, replications, critiques, method comparisons, automated circuit discovery evaluated on IOI, faithfulness analyses, circuit-reuse and pruning work, and papers that use IOI only as a test case.

**Verification convention.** Every number and quote below was read in the paper's own full text (arXiv HTML, ar5iv, or the published PDF). Numbers reported without a section, table, or figure location are not recorded. Where a paper is internally inconsistent, both figures are given. Where a number could not be located in the source, the entry says so.

**The model caveat, stated once.** IOI results do not transfer between GPT-2 sizes by default. Wang et al., Miller et al., Hanna et al., Shi et al., Makelov et al., and McDougall et al. work on **GPT-2 small**. Merullo et al. work on **GPT-2 Medium** and report a mechanism difference from GPT-2 small in the negative mover head. Tigges et al. work on **Pythia only** and never run GPT-2. Li & Subramani work on **Gemma / Llama / Qwen / OLMo** and never run GPT-2. Every per-paper entry states the model explicitly.

### Roster — 37 papers, sorted by what they actually ran

**IOI experiments on GPT-2 (25).** Wang 2211.00593 (small) · Miller 2407.08734 ("GPT-2") · Hanna 2403.17806 (small; + GPT-2 XL, Pythia-2.8B in appendix) · Conmy 2304.14997 (small) · Merullo 2310.08744 (**Medium**; + Large/XL preliminary) · Makelov 2311.17030 (small) · Wu et al. reply 2401.12631 (small) · Syed 2310.10348 (small) · Shi 2410.13032 (small) · Chen 2605.12671 (small; + Pythia-160M) · Zhang & Nanda 2309.16042 (small) · McDougall 2310.04625 (small; + Medium, Pythia) · Gong 2607.01940 (small; + Medium/Large) · Bhaskar 2406.16778 (small) · Li & Janson 2409.09951 (small) · O'Neill & Bui 2405.12522 (small) · Nainani 2411.16105 (small) · Chhabra 2503.01896 (small) · Naser Moghadasi 2605.22719 (small) · uit de Bos & Garriga-Alonso 2407.15166 (small) · Méloux 2510.00845 (small; + Llama-3.2-1B) · Franco 2602.13483 (small; + Pythia-160M, Gemma-2 2B) · Wu, Tonin, Cevher 2606.16920 (small, XL; + Pythia) · Mueller 2504.13151 and Arad 2511.18409 (small among four models).

**IOI experiments, no GPT-2 (4).** Tigges 2407.10827 (Pythia) · Li & Subramani 2605.08348 (Gemma, Llama, Qwen, OLMo) · Venkatesh 2605.08853 (Pythia, Qwen2.5) · Adhikari 2510.25013 (attention-only toys, symbolic IOI).

**No IOI experiment; IOI is background or a worked sketch (8).** Goldowsky-Dill 2304.05969 · Heimersheim & Nanda 2404.15255 (no experiments at all) · McGrath 2307.15771 (Chinchilla 7B, Counterfact) · Rushing & Nanda 2402.15390 (The Pile) · Méloux 2502.20914 (**toy MLPs only**) · Palumbo 2407.13594 (toy models; IOI sketched in an appendix and explicitly not evaluated) · Saraipour & Zhang 2508.16109 (syllogisms) · Bayat Makou 2606.06267 (Literal Sequence Copying, Pythia).

Papers in the third group are frequently cited as though they contained IOI results. They do not.

---

## Part 1 — Index by evidence question

### 1.1 Is the circuit necessary for IOI?

| Paper | Model | Finding |
| --- | --- | --- |
| Wang et al. 2211.00593 | GPT-2 small | Knocking out all Name Mover Heads gives "only 5% drop in logit difference" (§3.4). Their own headline evidence against simple component necessity. |
| Gong et al. 2607.01940 (CoAx) | GPT-2 small | Ablating the documented name-mover primaries moves IOI accuracy 1.00 → 0.97 and logit difference by 0.22 from a clean 2.53 (§1, Table 4). Ablating primaries plus their eight backups drops it by 1.15, against 0.60 predicted by summing single-head ablations — 1.9× super-additive (§C.3.2). Counterfactual patching attributes 55% of the repair to backups that are dormant in the intact model (§3.2). |
| McDougall et al. 2310.04625 | GPT-2 small | Two Negative Heads (L10H7, L11H10) account for 39% of the self-repair observed after ablating the three Name Mover Heads (§4.1). |
| Li & Subramani 2605.08348 | Gemma, Llama, Qwen (not GPT-2) | Ablating the shared IOI circuit produces near-zero or negative accuracy drops in every model at K ≤ 10% (Table 4, Table 5); Appendix L: "random ablation hurts more than shared-circuit ablation." |
| Venkatesh 2605.08853 | Pythia, Qwen2.5 (not GPT-2) | On Qwen2.5-0.5B and 1.5B, ablating the single top IOI head flips the sign of the logit difference (§5.1). On Pythia, 2–5 head ablations are needed to reach 80% task damage (Table 1). |

**Status: tested, and the result depends on whether components are ablated singly or jointly.** Single-component necessity fails on GPT-2 small because of self-repair. Set-level necessity is recovered only when backups are removed together. No paper reports a clean necessity result for the 26-head circuit as originally specified.

### 1.2 Is it sufficient?

| Paper | Model | Finding |
| --- | --- | --- |
| Wang et al. 2211.00593 | GPT-2 small | Mean-ablating everything outside the circuit leaves `|F(M)−F(C)| = 0.46`, "or only 13% of F(M)=3.56. In other words, C achieves 87% of the performance of M" (§4). |
| Miller et al. 2407.08734 | "GPT-2" | The same quantity ranges from below 0% to well over 100% depending on six methodological choices; the edge-level, specific-token-position variant — which "best represents the hypothesis of Wang et al." — has "a median score well over 100%" (§4.1). |
| Shi et al. 2410.13032 | GPT-2 small | IOI is significantly more faithful than random circuits up to 90% of model size (§4.2, Figure 2). Passes the flexible sufficiency test. |
| Conmy et al. 2304.14997 | GPT-2 small | The 9 heads ACDC recovers "are sufficient to complete the IOI task" (Appendix F.2) — asserted, no accompanying number. |
| Hanna et al. 2403.17806 | GPT-2 small | Activation-patching IOI circuits reach normalized faithfulness above 0.8; EAP and EAP-IG plateau at 0.6 (§4.3). |
| O'Neill & Bui 2405.12522 | GPT-2 small | Wang circuit (26 heads) logit difference 4.11 vs full model 3.55; their 40-head SAE circuit 3.62 (Table 4). |
| uit de Bos & Garriga-Alonso 2407.15166 | gpt2-small | Over 1,000,000 clean/corrupted input pairs, the KL divergence between model and circuit has mean 5.15, median 5.12, max 14.64 (Table 3). "the circuits for the IOI and docstring tasks fail to behave similarly to the full model even on completely benign inputs from the original task" (Abstract). |

**Status: tested and passed under the original protocol; the reported number is not robust to the protocol, and it holds on average rather than per example.** Sufficiency measured as an average over the distribution and sufficiency measured per input give different verdicts — Miller et al. report an inter-quartile range up to 50%, and uit de Bos & Garriga-Alonso report a KL distribution centred well away from zero.

### 1.3 Is it minimal — does every component earn its place?

| Paper | Model | Finding |
| --- | --- | --- |
| Wang et al. 2211.00593 | GPT-2 small | Every node has "at least 1% of the original logit difference" impact (§4.2). Passes their own test, with the caveat "the individual contribution of some attention heads is small." |
| Shi et al. 2410.13032 | GPT-2 small | "Recall from Table 1 that the G-T and IOI canonical circuits are not minimal" (§4.2). "For IOI, we can remove about 20% of the edges. However, we notice that the faithfulness of IOI does not vary monotonically as more edges are knocked out." |
| Li & Janson 2409.09951 | GPT-2 small | Under optimal ablation the manual circuit is "approximately optimal for its size" — the Pareto frontier is only 29% below it. Under mean/resample/counterfactual ablation, smaller optimized circuits achieve 84–85% lower Δ (§3.2). The paper attributes the latter to spoofing artifacts of those ablation methods. |
| Chen et al. 2605.12671 | GPT-2 small | A three-edge sheaf reaches 86.7% IOI accuracy in isolation (§4); removing any one of the three leaves performance essentially unchanged. |
| Bhaskar et al. 2406.16778 | GPT-2 small | Edge Pruning finds a 98.8%-sparse IOI circuit as faithful as ACDC's at 96.8% — 2.65× fewer edges (§4.2). Comparison is against ACDC, not against Wang et al. |

**Status: tested and failed under Shi et al.'s edge-removal test. Contested — Li & Janson reach the opposite verdict, and the disagreement is traceable to the ablation method.**

### 1.4 Is it specific to IOI, or are the components used by other tasks?

| Paper | Model | Finding |
| --- | --- | --- |
| Merullo et al. 2310.08744 | **GPT-2 Medium** | 78% head overlap (25/32) between the IOI circuit and the Colored Objects circuit at a top-2% importance threshold (§4). Forcing IOI-style inhibition behavior raises Colored Objects accuracy from 49.6% to 93.7% (§5). |
| Hanna et al. 2403.17806 | GPT-2 small | Cross-task faithfulness is near zero for most task pairs; overlap does not predict it (§5). The smallest EAP circuit containing ≥90% of the manual IOI circuit's nodes achieves 0% faithfulness (Appendix F). |
| Li & Subramani 2605.08348 | Gemma, Llama, Qwen | "circuits turn out not to be task-specific: ablating one task's circuit damages another task's performance about as much as that task's own circuit does" (Abstract). |
| McDougall et al. 2310.04625 | GPT-2 small | 76.9% of L10H7's effect on the OpenWebText training distribution is copy suppression (§3.3.2) — the negative name mover is a general mechanism, not an IOI-specific one. |
| Saraipour & Zhang 2508.16109 | GPT-2 small | Heads 10.7 and 11.10 act as negative heads in syllogism tasks; Truth Modulation Heads "align with the S-Inhibition category from IOI" (§4). |
| Tigges et al. 2407.10827 | Pythia | "Unlike the other heads described so far, this behavior is specific to IOI-type tasks; their behavior across the entire data distribution has not yet been characterized" (§3.2), about name-mover heads. |

**Status: tested; the components are substantially shared with other tasks.** Note the contradiction: Merullo reports 78% component overlap between IOI and Colored Objects in GPT-2 Medium, while Hanna reports near-zero cross-task *faithfulness* for IOI in GPT-2 small. These are different models and different quantities — overlap of component sets versus behavioral transfer — and Hanna's own conclusion is that the two do not track each other.

### 1.5 Are there rival circuits that explain IOI comparably well?

| Paper | Model | Finding |
| --- | --- | --- |
| Chen et al. 2605.12671 | GPT-2 small | Two sheaves, both 100% IOI accuracy, both ~3.5–4% edge density, with edge IoU 4.1% (Table 1). Across 20 sheaves, the shared core is 11 edges of a 7382-edge union, mutual IoU 0.15% (Table 3). **Node-level IoU on IOI is 64.2%** (Appendix D, Table 8) — the near-disjointness is in routing, not in which heads participate. |
| Méloux et al. 2510.00845 | gpt2-small, Llama-3.2-1B | Bootstrap-resampled IOI circuits share a mean pairwise Jaccard of 0.67 on gpt2-small and 0.34–0.39 on the Llama models (Table 4). Different EAP variants on gpt2-small IOI overlap at 0.071 (§5.3). |
| Méloux et al. 2502.20914 | **Toy MLPs only** | Non-identifiability demonstrated on Boolean-gate MLPs and one MNIST MLP. **IOI is cited only as background; no IOI or GPT-2 experiment exists in this paper.** |
| Franco et al. 2602.13483 | GPT-2 Small, Pythia-160M, Gemma-2 2B | Per-prompt IOI circuits cluster into families. In GPT-2 Small the split is by role order (ABBA vs BABA) with no substructure from surface wording; in Pythia-160M it is by surface wording (§3.1). |
| Wu, Tonin, Cevher 2606.16920 | GPT-2 small, GPT-2 XL, Pythia-160M, Pythia-2.8B | EAP-IG circuits vary under resampling and under prompt rephrasing; "rephrasing variance arises because prompts with different templates tend to activate different circuits in the model" (Abstract). |
| Miller et al. 2407.08734 | Tracr | Two different "ground truth" circuits for the same Tracr model depending on ablation method (Figure 11). |

**Status: tested, and rival circuits are found.** The strongest IOI-specific evidence is Chen et al., with the node-overlap caveat attached. Bayat Makou et al. 2606.06267 add the necessary control: on a different task, structurally distinct circuits proved functionally interchangeable under cross-condition transfer, so structural difference alone does not establish mechanistic difference. That control has not been run on IOI.

### 1.6 Does it double-dissociate from other circuits?

**No published double-dissociation test located.** The design would be: ablate the IOI circuit and show IOI performance falls while task B is spared, then ablate task B's circuit and show the reverse. The nearest published work runs only one arm or reaches the opposite conclusion:

- Li & Subramani 2605.08348 run the cross-task ablation matrix — the correct design — and find no dissociation: ablating another task's circuit damages the target task about as much as its own. Their IOI column is the extreme case, where the own-circuit effect is near zero or negative.
- Merullo et al. 2310.08744 demonstrate shared components between IOI and Colored Objects, which is the opposite of a dissociation.
- Hanna et al. 2403.17806 report an asymmetric cross-task faithfulness matrix, which is a single dissociation at most.

**Status: searched, no published double-dissociation test located.**

### 1.7 Are confounds (position, frequency, template, length) controlled?

| Confound | Papers | Finding |
| --- | --- | --- |
| Template | Wang et al. (15 templates, per-template ablation means, §2.1); Miller et al. (§4.1); Franco et al. 2602.13483 (§3.1); Wu et al. 2606.16920 | Miller: faithfulness is "systematically greater for the prompts of form BABA than prompts of form ABBA." Franco et al.: GPT-2 Small's per-prompt IOI circuits split cleanly into an ABBA cluster and a BABA cluster. Wu et al.: "prompts with different templates tend to activate different circuits in the model." Controlled, and shown to change both the score and the traced mechanism. |
| Token position | Wang et al. (per-(head, position) circuit); Miller et al. (§4.1); Zhang & Nanda (Appendix F) | Miller: ablating all positions gives "consistently ... lower faithfulness scores" than ablating only circuit positions. Zhang & Nanda: corrupting S2 misses at least two of three Name Mover Heads under every metric; corrupting S1+IO recovers all three but then finds no S-Inhibition Heads (Tables 4, 5). |
| Held-out lexical items | Mueller et al. 2504.13151 | The MIB private test set "contains names and direct objects that are not contained in the public train or test set" (§2.1). |
| Lexical / distractor content | Naser Moghadasi & Ghaderi 2605.22719 | 45 of 300 prompts using the object "the keys" account for 42 of 61 failures (93.3% vs 7.5%, Fisher exact p = 8.79 × 10⁻³³); conditioning on the keys-free subset drops the count of significant SAE features from 146 to 5 (§IV-C, §IV-F). |
| Knockout-procedure artifact | Nainani et al. 2411.16105 | "S2 Hacking": on DoubleIO and TripleIO the base circuit *outperforms* the full model (faithfulness 1.285 and 2.586, Table 1), which they trace to the mean-ablation knockout rather than to model behavior (§4). |
| Content of the transferred object | uit de Bos & Garriga-Alonso 2407.15166 | The worst-performing IOI inputs "often seem to involve romantic items"; the Conmy et al. IOI object list has only eight values (§3). |
| Name frequency | — | No published test located **on IOI**. Bayat Makou et al. 2606.06267 run the frequency-band manipulation on a different task (Literal Sequence Copying in Pythia) and find frequency-specific circuits to be functionally interchangeable. |
| Sequence length | — | No published test located. Adhikari 2510.25013 lists it as future work: "this paper doesn't explore how this minimal circuit behaves when subjected to varying sequence lengths." |

**Status: partially.** Template, position, and held-out lexical items are controlled in at least one paper each and all three are shown to change conclusions. Name frequency and sequence length: searched, no published control located.

### 1.8 Does it replicate across models, scales, seeds?

| Axis | Papers | Finding |
| --- | --- | --- |
| GPT-2 small → Medium | Merullo et al. 2310.08744 | Circuit reproduces with "minor differences," but the negative mover head behaves differently: in GPT-2 small it attends to all names; in GPT-2 Medium "this head attends only to the S2 token" (§3). |
| GPT-2 Large / XL | Merullo et al., Appendix I | Top-10 head overlap with Colored Objects falls to 5/10 (Large) and 0/10 (XL). |
| Pythia 70M–12B | Tigges et al. 2407.10827 | The same three-step algorithm, with all path-patching step metrics "generally above 50%" and the core step "above 70%" (§4.2). Two named deviations: copy-suppression heads flip sign relative to GPT-2, and Pythia-160m's circuit has no duplicate-token heads. |
| Pythia vs Qwen2.5 | Venkatesh 2605.08853 | Circuit concentration tracks attention architecture, not scale: GQA models need 1 ablation to reach 80% task damage, MHA models need 2–5 (Table 1). |
| GPT-2 / Qwen / Gemma / Llama | Mueller et al. 2504.13151; Arad et al. 2511.18409 | IOI is localizable in all four with EAP-IG; CMD 0.01–0.04 and CPR 1.6–3.2 for the best methods. |
| Larger models, negative-head mechanism | Saraipour & Zhang 2508.16109 | "the heads most responsible for enabling opposite syllogism performance in the larger models are not the negative heads" (Appendix D). |
| Training seeds (same architecture, different init) | — | No published test located for the IOI circuit. Nearest: Bhaskar et al. run 12 **discovery** seeds at 97.5% sparsity with pairwise IoU 0.5–0.7 (Appendix D) — that varies the search, not the trained model. |

**Status: replicates across models and scales at the level of the algorithm, with named exceptions in the negative/copy-suppression components. Across training seeds: no published test located.** GPT-2 was released as a single run without intermediate checkpoints, which is the practical reason.

### 1.9 Does the faithfulness result depend on the ablation method?

This is the best-established finding in the follow-up literature. Every paper that varied the ablation method found the conclusion moved.

| Paper | Model | Effect |
| --- | --- | --- |
| Miller et al. 2407.08734 | "GPT-2" | Resample vs mean ablation differs significantly at the node level (p = 1e-5) but not at the edge level; node vs edge, all-positions vs circuit-positions, averaging order, and ABC-dataset size all shift the number (§4.1). "The task cannot be separated from the ablation methodology" (§6). |
| Li & Janson 2409.09951 | GPT-2 small | On IOI at 1,000 edges, optimal ablation admits circuits with 32% lower Δ than counterfactual, 62% lower than mean, 88% lower than resample (§3.2). For single components, Δ_opt is 11.1% of Δ_zero, 33.0% of Δ_mean, 17.7% of Δ_resample (Table 1). |
| Conmy et al. 2304.14997 | GPT-2 small | ACDC edge-level AUC on IOI: 0.869 with corrupted activations, 0.539 with zero ablation (Tables 2, 3). |
| Shi et al. 2410.13032 | GPT-2 small | "for G-T and IOI, knocking down the complete model has less impact than knocking down the candidate circuit. This pattern appears with the STR ablation scheme but is absent with zero-ablation" (§4.2). |
| Zhang & Nanda 2309.16042 | GPT-2 small | Symmetric token replacement and Gaussian noising "detect different sets of heads as important" for any fixed metric (§3.1, Table 1). |
| O'Neill & Bui 2405.12522 | GPT-2 small | ACDC node-level IOI AUC 0.777 (random ablation) vs 0.424 (zero ablation); SP 0.797 vs 0.479 (Table 6). |
| Mueller et al. 2504.13151 | 4 models | "Circuits found with CF ablations outperform those found with mean or optimal ablations" (§3.3). |

The metric also matters independently of the ablation. Conmy et al.: ACDC's edge-level IOI AUC falls from 0.869 (KL) to 0.589 (logit difference), and logit-difference optimization "does not find Negative Name Movers at any threshold" (Appendix F.3). Hanna et al.: the EAP shortfall on IOI holds "only with logit diff, not KL divergence" (§4.3). Zhang & Nanda: probability as a metric "must fail to detect negative model components, if corruption reduces the correct token probability to near zero" (§4.2).

**Status: tested and confirmed, repeatedly and by independent groups.**

### 1.10 Does the circuit co-emerge with the behavior during training?

| Paper | Model | Finding |
| --- | --- | --- |
| Tigges et al. 2407.10827 | Pythia 70m–2.8b, 154 checkpoints | Name-mover heads emerge at 2–8 × 10⁹ tokens "during or just before IOI behavior appears" (§3.2). Head identity is not stable — Pythia-160m head (4,6) acquires name-mover behavior after 4 × 10⁹ tokens and loses it at 3 × 10¹⁰ — while the algorithm persists (§4.1). |
| Li & Subramani 2605.08348 | OLMo-2-1B, 20 checkpoints | IOI circuit reuse peaks in the first ~76B tokens and then declines to 18–37%; necessity is negative at 17 of 20 checkpoints (Tables 16, 21). |
| Chhabra, Zhu, Khalili 2503.01896 | GPT-2 small | Fine-tuning dynamics, not pretraining: fine-tuning on clean IOI amplifies existing mechanisms without introducing new ones ("Circuit Amplification", §4.1), and corrupted models recover the original circuit on retraining at 95–96% faithfulness (§5). |
| Adhikari 2510.25013 | Attention-only toys trained from scratch | "Emergence" here means emergence as a function of architectural capacity, not over training steps — the Limitations section disclaims training-dynamics analysis. |

**Status: tested in Pythia and OLMo-2. For GPT-2 small specifically, no published test located** — GPT-2 has no public pretraining checkpoints.

---

## Part 2 — Per-paper entries

### Wang, Variengien, Conmy, Shlegeris, Steinhardt — "Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 Small"

- **arXiv:** 2211.00593. **Venue:** ICLR 2023 (per `references.bib`; no venue line appears in the arXiv HTML itself).
- **Model:** GPT-2 small (12 layers, 12 heads/layer). **Task:** IOI, 15 templates, random single-token names/places/objects.
- **What it did.** Traced the IOI computation backward from the logits using path patching, producing a circuit of 26 attention heads in 7 classes. Characterized head classes by attention pattern and OV/QK projections. Proposed and applied three validation criteria — faithfulness, completeness, minimality.
- **Bears on:** necessity (partially), sufficiency, minimality, completeness, confounds (partially).

Key numbers, all verifiable in the text:

| Quantity | Value | Location |
| --- | --- | --- |
| Circuit size | 26 attention heads, "1.1% of the total number of (head, token position) pairs" | §1 |
| Model baseline | mean logit difference 3.56 over 100,000 examples; IO over S 99.3% of the time; mean IO probability 49% | §2, "Task description" |
| Faithfulness | `|F(M)-F(C)|=0.46`, "or only 13% of F(M)=3.56. In other words, C achieves 87% of the performance of M" | §4 |
| Completeness | greedy search finds subsets K with incompleteness score "up to 3.09 (87% of the original logit difference)" | §4.1 |
| Minimality | every node has "at least 1% of the original logit difference" impact | §4.2, Figure 7 |
| Naïve baseline circuit | "faithfulness score of 0.1, comparable to the full circuit C" | §4.3 |
| Name Mover knockout | knocking out all Name Mover Heads gives "only 5% drop in logit difference" | §3.4; Appendix F |
| MLP knockout | knocking out all MLPs after layer 1 drives logit difference to −1.1 | Appendix J |

**Ablation method (load-bearing for every comparison in this file):** mean ablation, with means taken over the `p_ABC` distribution (the same templates with three unrelated random names substituted), computed per template.

> "In this work, all knockouts are performed in a modified `p_IOI` distribution called `p_ABC`. It relies on the same generation procedure, but instead of using two names (IO and S) it used three unrelated random names (A, B and C)." (§2.1)

> "To ensure that grammatical information is constant when averaging, we compute the mean of a node across samples of the same template." (§2.1)

The paper states its own limits explicitly:

> "Our circuit shows significant improvements compared to a naïve (but faithful) circuit, but fails to pass the most challenging tests." (§1)

> "The first two methods of sampling K suggested to us that our circuit was complete, as every incompleteness score computed with those methods was small. However, the third resulted in sets K that had high incompleteness score: up to 3.09 (87% of the original logit difference). These greedily-found sets were usually not semantically interpretable (containing heads from multiple categories)" (§4.1)

> "These results ensure that we did not interpret irrelevant nodes, but do show that the individual contribution of some attention heads is small." (§4.2)

§4.4 constructs adversarial examples from the circuit hypothesis (adding a duplicated IO in a natural sentence) and reports that the mechanism there is not covered by the analysis: "the S-Inhibition Heads attend not only to S2, but also to the second occurrence of IO. As this pattern is not present in `p_IOI` nor in `p_ABC`, it is beyond the analysis presented in Section 3."

---

### Miller, Chughtai, Saunders — "Transformer Circuit Faithfulness Metrics Are Not Robust"

- **arXiv:** 2407.08734. **Venue:** COLM 2024 (per `references.bib`; the arXiv text names only "our anonymous reviewers at COLM 2024" in the acknowledgments).
- **Model:** written as "GPT-2" throughout, including Table 4; the paper never writes "GPT-2 small" for its own IOI experiments. Other case studies: a 4-layer attention-only model (Docstring), Pythia 2.8B (Sports Players), two Tracr compiled models.
- **Task:** IOI plus three others.
- **What it did.** Decomposed "ablation methodology" into a six-tuple (granularity, component type, ablation value, token positions, direction, set), tabulated seven prior circuit papers against it and found "each methodology differs from all of the others in at least one aspect," then re-measured the Wang et al. IOI circuit's faithfulness under systematically varied choices.
- **Bears on:** ablation-method dependence (primary), minimality, confounds (template format, token position), rival circuits.

Key numbers:

| Quantity | Value | Location |
| --- | --- | --- |
| Reference point | Wang et al.'s 87% logit difference recovery, "at specific token positions with Mean Node Ablations" | Figure 3 caption (§4.1) |
| Mean-ablation set size used by Miller et al. | 100 ABC prompts, "which differs from Wang et al. (2023)" | Figure 3 caption |
| Wang et al.'s mean-ablation set size | "around seven examples per template" | §4 |
| Resample vs. mean ablation | systematically lower faithfulness under resample, t-test p = 1e-5, "significant for Node Ablation but not Edge Ablation" | §4.1 |
| Per-example spread | inter-quartile range of logit difference recovered "stretching up to 50% across the dataset"; outliers "tens of thousands of percent" | §4.2 |

The paper reports IOI results graphically (Figures 3 and 4). Directional findings, all §4.1: edge-level complement ablation "returns substantially higher percentages" than node-level; ablating all token positions gives "consistently ... lower faithfulness scores" than ablating only the circuit's specified positions; faithfulness is "systematically greater for the prompts of form BABA than prompts of form ABBA"; faithfulness "monotonically increases with the size of the ABC dataset"; and computing the mean of per-example ratios rather than the ratio of means "return[s] substantially higher percentages."

> "The IOI circuit is specified as an edge-level circuit, but Wang et al. (2023) evaluate its faithfulness via a node-wise ablation methodology." (§4)

> "The original IOI work evaluated at specific token positions with Mean Node Ablations and obtained a logit difference recovery of 87%. Other methodologies giving faithfulness scores above 100% or below 0% would have given the authors significantly less confidence about the IOI circuit, and may have led them to include different edges." (Figure 3 caption)

> "It is concerning that the edge-level circuit with specific token positions has a median score well over 100%, as this best represents the hypothesis of Wang et al. (2023)." (§4.1)

> "The inter-quartile range (IQR) is also large, stretching up to 50% across the dataset. This is concerning: while the circuit matches the behavior on average, it does not match it for many examples." (§4.2)

> "Do you want your IOI circuit to include the mechanism that decides it needs to output a name? Then use zero ablations. Or do you want to find the circuit that, given the context of outputting a name, completes the IOI task? Then use mean ablations. The task cannot be separated from the ablation methodology." (§6)

> "It suggests that assessing the quality of automated methods by measuring the overlap with some 'ground truth' can be misleading, if the ground truth was discovered using a different ablation methodology." (§6)

Appendix F establishes the terminological bridge: Wang et al.'s "Path Patching" is "equivalent to Edge Resample Ablation in our terminology."

No replication across models or seeds for IOI. No frequency or sequence-length confound analysis.

---

### Hanna, Pezzelle, Belinkov — "Have Faith in Faithfulness: Going Beyond Circuit Overlap When Finding Model Mechanisms"

- **arXiv:** 2403.17806. **Venue:** not stated in the arXiv text.
- **Models:** GPT-2 small for all main experiments ("We focus on simple tasks that are feasible even for GPT-2 small, the model most often studied from a circuits perspective," §4.1). Appendix J replicates on GPT-2 XL and Pythia-2.8B with 100 examples per task.
- **Tasks:** IOI, Gender-Bias, Greater-Than, Country–Capital, SVA, Hypernymy, plus two Greater-Than variants.
- **What it did.** Introduced EAP-IG (edge attribution patching with integrated gradients) and compared it against EAP and against per-edge activation patching. Then argued that overlap with a manually found circuit is a poor proxy for faithfulness, using both within-task and cross-task evidence.
- **Bears on:** method comparison, faithfulness metric definition, task-specificity, rival circuits.

**Correction worth carrying:** this paper does **not** run ACDC. ACDC is mentioned twice in passing. The comparison baseline is per-edge activation patching, which the authors themselves flag as imperfect: "scoring each edge independently and then finding a circuit may be less accurate than e.g. ACDC" (§4).

| Quantity | Value | Location |
| --- | --- | --- |
| Activation-patching IOI circuit | normalized faithfulness "above 0.8" | §4.3, Figure 3 |
| EAP and EAP-IG IOI circuits | plateau at 0.6 | §4.3, Figure 3 |
| Overlap-vs-faithfulness on IOI | smallest EAP circuit containing ≥90% of the manually found IOI circuit's nodes achieves **0% faithfulness** | Appendix F |
| Same construction, Greater-Than | 51% faithful | Appendix F |
| GPT-2 small IOI baselines | clean logit diff 3.80; corrupted 0.03 | Table 1 (Appendix A) |
| Cross-task correlation | faithfulness vs. node overlap r = 0.87, vs. edge overlap r = 0.86, both p < 0.001 | §5, Figure 5 |

> "A circuit is faithful to model behavior on a task if we can corrupt all model edges outside the circuit while retaining the model's original task performance." (§2)

> "On IOI, EAP and EAP-IG are much less faithful than activation patching (though notably only with logit diff, not KL divergence). The activation patching circuit quickly achieves faithfulness above 0.8, while EAP and EAP-IG circuits plateau at 0.6." (§4.3)

> "the smallest EAP circuit for IOI that contains at least 90% of the manually-found IOI circuit's nodes achieves 0% faithfulness. The smallest EAP circuit for Greater-Than fulfilling that criterion does better, but is still only 51% faithful." (Appendix F)

> "We thus conclude that overlap is not a good predictor of cross-task faithfulness when overlaps are moderate." (§5)

> "cross-task faithfulness depends not on overlap generally, but on which specific nodes or edges overlap (e.g. the edge from the input to MLP 0 is often crucial)." (§6)

Cross-task faithfulness is asymmetric: "while the Hypernymy circuit (y-axis) is highly faithful on the Country-Capital task (x-axis), the reverse is not true" (§5). Completeness is acknowledged as untested: "it does not guarantee that they are complete, i.e. not missing any important (negative-acting) components" (§6). No seed replication.

---

### Conmy, Mavor-Parker, Lynch, Heimersheim, Garriga-Alonso — "Towards Automated Circuit Discovery for Mechanistic Interpretability" (ACDC)

- **arXiv:** 2304.14997. **Venue:** NeurIPS 2023 (per `references.bib`; not stated in the arXiv text).
- **Model for IOI:** GPT-2 small. Other tasks use a 4-layer attention-only model (Docstring), a 2-layer attention-only model (Induction), and Tracr-compiled transformers.
- **Tasks:** IOI, Docstring, Greater-Than, tracr-xproportion, tracr-reverse, Induction.
- **What it did.** Automated the third step of the standard circuit workflow: walk the computation graph in reverse topological order, delete each edge whose removal raises `D_KL(G||H)` by less than a threshold τ. Compared against Subnetwork Probing and Head Importance Score for Pruning, both adapted to the same interchange-intervention setting. Scored by ROC/AUC against the published circuits.
- **Bears on:** method comparison, minimality (indirectly), completeness (negative components), ablation-method dependence.

AUCs against the IOI canonical circuit, **Table 2** ("AUCs for corrupted activations, Random Ablation"):

| Metric | ACDC(E) | HISP(E) | SP(E) | ACDC(N) | HISP(N) | SP(N) |
| --- | --- | --- | --- | --- | --- | --- |
| KL | 0.869 | 0.789 | 0.823 | 0.880 | 0.668 | 0.842 |
| Loss (logit diff) | 0.589 | 0.836 | 0.707 | 0.777 | 0.728 | 0.797 |

**Table 3** (zero ablation) drops ACDC on IOI to 0.539 (edge, KL) and 0.447 (edge, loss).

Other IOI numbers: the Figure 1 run recovers 9 heads, all in the Wang et al. circuit, at τ = 0.0575 on N = 50 examples from a single template, in 8 minutes on an A100 (Appendix F.1). The authors' low-level implementation of the IOI ground-truth circuit has **1041 edges** (§4.1, Figure 14 caption). Appendix F.2 gives the ground-truth circuit's logit difference as 3.24 versus 4.11 for the full model, with KL 0.44; Appendix C.3 states "The IOI circuit has a logit difference of 3.55" — these two figures are inconsistent within the paper.

> "All nine heads found in Figure 1 belong to the IOI circuit, which is a subset of 26 heads out of a total of 144 heads in GPT-2 small. Additionally, these 9 heads include heads from three different classes (Previous Token Heads, S-Inhibition Heads and Name Mover Heads) and are sufficient to complete the IOI task, showing that ACDC indeed can recover circuits rather than just subgraphs." (Appendix F.2)

> "The IOI recovery runs were not able to recover negative heads when optimizing for logit difference. Even when optimizing for low KL divergence, the negative components were only recovered when very small thresholds were used (Figure 15)." (§4.1)

> "This is a case where KL divergence performs better than logit difference maximisation (which does not find Negative Name Movers at any threshold), but still is far from optimal (many extraneous heads are found)." (Appendix F.3)

> "Additionally, a more fundamental limitation to measuring the false and true positive rates of circuit recovery methods is that the ground-truth circuits are reported by practitioners and are likely to have included extraneous edges and miss more important edges. ... Since these interpretability works are carried out by humans who often report limitations of their understanding, our 'ground-truth' is not 100% reliable, limiting the strength of the conclusions that can be drawn from the experiments in this section." (§4.1)

> "A limitation with all existing methods is that they optimize a single metric. This means they systematically miss internal model components such as the 'negative' components found in previous work (IOI, Docstring) that are actively harmful for performance." (§4.1)

The IOI corrupted distribution is Wang et al.'s ABC dataset (Appendix F.1). Appendix L introduces **reset networks** (permuted Q/K/V head dimensions) as a hallucination control; SP and HISP partially optimize them, ACDC less so.

The abstract's headline numbers — "5/5 of the component types" and "68 of the 32,000 edges" — are **Greater-Than, not IOI** (confirmed in Appendix G).

---

### Merullo, Eickhoff, Pavlick — "Circuit Component Reuse Across Tasks in Transformer Language Models"

- **arXiv:** 2310.08744. **Venue:** ICLR 2024 (per `references.bib`; not stated in the arXiv text).
- **Model: GPT-2 Medium, not GPT-2 small.** This is the single most commonly mis-stated fact about this paper.

> "Because of the poor performance of GPT2-Small on the Colored Objects task, we use the larger GPT2-Medium model. This means we must first reproduce the IOI results from Wang et al. (2022) on the larger model." (§3)

  Appendix I adds a preliminary logits-only path-patching analysis on GPT-2 Large and GPT-2 XL.
- **Tasks:** IOI and Colored Objects (main); Greater Than and World Capitals (Appendix H, as low-overlap controls).
- **What it did.** Re-derived the IOI circuit in GPT-2 Medium, ran the same path-patching pipeline on Colored Objects, compared the two head sets at a top-2% importance threshold, then intervened on Colored Objects to force IOI-style behavior and checked the predicted downstream signature on mover heads.
- **Bears on:** task-specificity (primary), replication across scale, rival explanations.

| Quantity | Value | Location |
| --- | --- | --- |
| Head overlap, IOI vs. Colored Objects | 25/32 = 78%, at the top-2% importance threshold | Abstract; §1; §4 |
| Colored Objects baseline | 49.6% accuracy (49.7% in one sentence of §5) | §2.1; §5; Figure 5 caption |
| After forcing IOI-style inhibition + negative mover behavior | 93.7%, "the intervention introduces zero new mistakes" | §5 |
| Negative mover head intervention alone | 78.1% | §5 |
| Inhibition head interventions alone | 81.5% | §5 |
| Mover-head attention shift | −8.7% to incorrect colors, +2.7% to the correct color | §5 |
| Correlation of intervention effect with path-patching effect | Spearman 0.69 | §5 |
| Control tasks | Greater Than shares 3/18 = 16.7% with IOI; World Capitals shares 25% | Appendix H |
| Scale | 5 of top 10 heads shared in GPT-2 Large; 0 of top 10 in GPT-2 XL | Appendix I |

Shared heads (GPT-2 Medium numbering): mover heads 15.14, 16.15, 17.4, 18.5, 19.15; induction head 9.3; duplicate token head 6.4. IOI-only: three inhibition heads and negative mover head 19.1. Colored-Objects-only: content gatherer heads 11.6, 11.7, 12.15.

> "Figure 3 visualizes this overlap and the relative importance of each head, which shows a very large overlap between the heads performing this function; thresholding at the 2% most important heads for each circuit, we find that 25/32, or 78% of the circuit is shared." (§4)

> "We show that part of the circuit described here boils down to a more generic algorithm for copying from a list of potential options, rather than strictly indirect object identification." (§3)

> "This evidence together suggests that the inhibition-mover subcircuit is itself a manipulable structure within the model that is invariant to the highly different input domains that we used in our experiments." (Figure 5 caption)

> "It is worth noting that such overlap is not trivial–i.e., it is not as though any two circuits will contain the same components or even overlapping algorithmic steps." (§4)

> "A limitation of this study is that we are not able to confirm the generality of the circuit beyond the tasks studied here." (Appendix J)

A GPT-2 Medium / GPT-2 small mechanism difference is reported directly: "Wang et al. (2022) find that the negative mover heads in GPT2-Small attend to all names and hypothesize that they hedge the prediction to avoid high loss. In contrast, we find that in GPT2-Medium, this head attends only to the S2 token and demotes its likelihood as the next prediction" (§3).

The inhibition head IDs are internally inconsistent: (12.3, 13.4, 13.13) in §5 and Appendix C.3; (12.3, 13.4, 13.14) in Appendix B.3 and the Figure 6 caption.

---

### Tigges, Hanna, Yu, Biderman — "LLM Circuit Analyses Are Consistent Across Training and Scale"

- **arXiv:** 2407.10827. **Venue:** not stated in the arXiv text.
- **Models: the Pythia suite only.** Behavioral evaluation 70M–12B; circuit finding 70m–2.8b; IOI algorithm metrics 160M–2.8B; component tracking on Pythia-160m. **GPT-2 is never run in this paper.**
- **Tasks:** IOI, Gendered-Pronoun, Greater-Than, SVA.
- **What it did.** Extracted circuits with EAP-IG at all 154 Pythia checkpoints, dated the emergence of functional head types with six published head-scoring metrics, reverse-engineered Pythia-160m's IOI circuit by path patching, and defined three ratio metrics for the algorithm's three steps to track across checkpoints and scales.
- **Bears on:** training co-emergence (primary), replication across scale, circuit stability.

| Quantity | Value | Location |
| --- | --- | --- |
| Faithfulness criterion | minimal circuit reaching ≥80% of whole-model performance | §2.2 |
| Name-mover head emergence | 2–8 × 10⁹ tokens, across models | §3.2 |
| Induction head emergence | "soon after they have seen 2×10⁹ tokens" | §3.2 |
| Pythia-160m head (4,6) | acquires name-mover behavior after 4 × 10⁹ tokens, loses it at 3 × 10¹⁰ | §4.1 |
| IOI algorithm metrics | "generally above 50%"; copy-suppression + name-mover step "above 70%" | §4.2, Figure 4B–D |
| Circuit size vs. model size | Pearson r = 0.72 for IOI | §5 |

> "We find that task abilities and the functional components that support them emerge consistently at similar token counts across scale. Moreover, although such components may be implemented by different attention heads over time, the overarching algorithm that they implement remains." (Abstract)

> "the name-mover head (4,6) suddenly stops exhibiting this behavior at 3×10^10 tokens, having acquired it after 4×10^9 tokens." (§4.1)

> "Generalization across model scales also seems promising, as IOI circuit metrics from Pythia-160m are also high in larger Pythia variants. However, there is variation: while the name-mover, copy-suppression, and S-inhibition heads are at work in all models' circuits, the Pythia-160m circuit does not involve duplicate-token heads, while others do. So small differences exist amid big-picture similarity." (§4.2)

> "In the original IOI circuit, copy suppression heads hurt performance, downweighting the correct name. In contrast, we find (Appendix D) that they contribute positively to the Pythia IOI circuit by downweighting the incorrect name" (§3.2)

On completeness, they decline the Wang et al. test: "ensuring that a circuit is entirely complete ... is challenging, and no definitive method of verifying this has emerged. The most notable existing method, from Wang et al. [71], requires comparing circuit and model performance under a wide variety of ablations, and is seldom used due to its complexity and computational cost" (§2.2). No seed variation (Pythia ships one seed per size) and one model family only, both acknowledged in Limitations.

---

### Li & Subramani — "How Much Do Circuits Tell Us? Measuring the Consistency and Specificity of Language Model Circuits"

- **arXiv:** 2605.08348. **Venue:** not stated in the arXiv text (ICML template markers present).
- **Models:** Gemma 2 2B, Gemma 2 2B Instruct, Llama-3.2-3B, Llama-3.2-3B Instruct, Qwen3-4B, Qwen3-8B, OLMo-2-1B (the last for pretraining dynamics, 20 checkpoints). **No GPT-2.**
- **Tasks:** Addition, Boolean Logic, IOI, CopyColors MCQA, ARC Easy, ARC Challenge. IOI setup follows Wang et al. and uses the MIB dataset and S2-IO flip counterfactual.
- **What it did.** Extracted a per-example EAP circuit for 1000 examples per task per model, defined the shared component set (components in ≥P% of per-example circuits), zero-ablated it against a capacity-matched random control, then ablated each task's circuit and evaluated every other task.
- **Bears on:** task-specificity (primary), necessity, consistency across inputs.

> "First, circuits should be **consistent**: if a circuit truly captures how a model solves a task, the same components should recur for different instances of that task. Second, circuits should be **specific**: a task's circuit should be meaningfully different from the circuits of unrelated tasks." (§1)

> "However, circuits turn out not to be task-specific: ablating one task's circuit damages another task's performance about as much as that task's own circuit does." (Abstract)

> "These findings suggest that circuit discovery at the level of attention heads and MLP layers primarily identifies general-purpose model infrastructure rather than task-specific mechanisms." (§1)

Headline cross-task numbers at K = 10% (§5): Llama-3.2-3B Addition, 99% own-circuit drop vs. 99% mean other-circuit drop; ARC Challenge 41% vs. 40%. Circuit overlap at K = 10% "typically ranges from 0.46 to 0.89," against an analytic chance baseline of K/(2−K) ≈ 5%.

**The IOI-specific result is the striking one and cuts against the headline.** In Table 5 (own/other accuracy drop, percentage points), the IOI column is near zero or negative for every model at every K — for example at K = 10%: Gemma 2B 0/0, Llama-3B −5/12, Qwen-4B 14/11, Qwen-8B 3/1. Table 4 necessity for IOI is ≤ 0.05 for all six models at K ≤ 10%. Appendix L states it plainly:

> "The IOI columns are consistently negative across K, reflecting the anomaly noted in the main text: random ablation hurts more than shared-circuit ablation." (Appendix L)

Ablation is **zero ablation**, scored by top-1 accuracy under argmax decoding — not logit-difference recovery. Sufficiency is named but not measured. No seed variation; one extraction method (EAP) only, acknowledged as a limitation.

---

### Makelov, Lange, Nanda — "Is This the Subspace You Are Looking for? An Interpretability Illusion for Subspace Activation Patching"

- **arXiv:** 2311.17030. **Venue:** not stated in the arXiv text.
- **Models:** GPT-2 small for IOI; GPT-2 XL for factual recall / ROME.
- **Task:** IOI (three templates, train/test split over names, objects, places, and templates), plus CounterFact.
- **What it did.** Showed that a learned one-dimensional subspace in MLP8 can appear to mediate the IOI position variable while lying largely in `ker W_out`, i.e. in directions provably disconnected from the output. Proposed decomposing the found direction into nullspace and rowspace components and re-patching along the rowspace alone as a diagnostic.
- **Bears on:** localization validity, ablation/patching-method dependence, rival explanations.

Table 1 (fractional logit difference decrease / interchange accuracy), GPT-2 small IOI:

| Patched object | FLDD | Interchange accuracy |
| --- | --- | --- |
| full MLP8 | −8% | 0.0% |
| v_MLP (learned 1-D) | 46.7% | 4.2% |
| v_MLP rowspace | 13.5% | 0.2% |
| full residual stream | 123.6% | 54.8% |
| v_resid | 140.7% | 74.8% |
| v_resid rowspace | 127.5% | 63.1% |

> "Counterintuitively, even if a subspace intervention makes the model's output behave as if the value of a feature was changed, this effect may be achieved by activating a dormant parallel pathway leveraging another subspace that is causally disconnected from model outputs." (Abstract)

> "Specifically, our results suggest that every MLP layer between two components communicating some feature through residual connections is likely to contain a subspace which appears to mediate the feature when activation patched." (§1)

> "In particular, patching along only the causally-relevant component of the subspace (the one in (ker W_out)^⊥) destroys the effect of the subspace patch; we find this a convincing reason to be suspicious of the explanatory faithfulness of these subspaces." (§8)

Appendix B.5 replaces MLP8's weights with random matrices and still finds an illusory subspace.

---

### Wu, Geiger, Huang, Arora, Icard, Potts, Goodman — "A Reply to Makelov et al. (2023)'s 'Interpretability Illusion' Arguments"

- **arXiv:** 2401.12631. **Venue:** not stated in the arXiv text.
- **Model:** GPT-2 small. **Task:** IOI, same generator as Wang et al. and Makelov et al.
- **What it did.** Argued that Makelov's nullspace diagnostic flags directions Makelov himself calls non-illusory (on Makelov's own toy network, the "non-illusory" direction retains only 20% of its effect under the rowspace-only intervention). Ran a new DAS sweep on IOI in GPT-2 small scored by interchange intervention accuracy rather than FLDD.
- **Bears on:** localization validity, metric choice.

Numbers: at layer 8, DAS reaches **70% IIA** on the residual stream and **4% IIA** on MLP activations — "which is approximately the same as Makelov et al.'s results" (§5.2). Individual heads at layer 8 give 0% IIA; head 6 plus head 10 together reach under 20%; roughly 11 heads are needed to approach the ceiling for the IO-name variable (§5.4, §5.5).

> "Fundamentally, we reject the label 'illusions' for these phenomena. These are simply discoveries about distributed representations." (§1)

> "we agree with Makelov et al. that, for example, their MLP-in-the-middle 'illusion' will be common (see Section 7 in the paper). Except it is not an 'illusion' in any useful sense. It is a simple fact about the geometry of representations." (§3.3)

> "Thus, we interpret 4%, which is much lower than the task performance, as a failure to find any relevant structure." (§4.2)

**Where they agree:** both find DAS in MLP8 gives near-zero interchange accuracy (4.2% vs 4%) and DAS in the layer-8 residual stream works (74.8% vs 70%). **Where they differ:** whether the nullspace test is a valid detector, whether the phenomenon warrants the word "illusion," and whether FLDD or interchange accuracy is the right metric.

---

### Méloux, Portet, Peyrard — "Mechanistic Interpretability as Statistical Estimation: A Variance Analysis"

- **arXiv:** 2510.00845 (v4 line printed in the HTML). **Venue:** not stated in the text (ICML template markers present).
- **Models:** gpt2-small, Llama-3.2-1B, Llama-3.2-1B-Instruct. **Tasks:** IOI, SVA, Greater-Than.
- **What it did.** Treated circuit discovery as statistical estimation. Measured the variability of exact causal-mediation edge scores, then measured how much discovered circuits change under bootstrap resampling, meta-dataset resampling, prompt paraphrasing, counterfactual-noise amplitude, and estimator/aggregation choice. Four estimators studied: EAP, EAP-IG (inputs), EAP-IG (activations), clean-corrupted.
- **Bears on:** circuit stability, rival circuits, ablation-method dependence.

IOI stability under bootstrap resampling (n = 100), mean pairwise Jaccard between discovered circuits:

| Model | Circuit error | Jaccard mean | Jaccard CV |
| --- | --- | --- | --- |
| gpt2-small | 0.11 | **0.67** | 0.19 |
| Llama-3.2-1B | 0.66 | **0.39** | 0.85 |
| Llama-3.2-1B-Instruct | 0.69 | **0.34** | 0.76 |

Under meta-dataset resampling and prompt paraphrasing, gpt2-small IOI Jaccard rises to 0.88 and 0.89. Across estimator/aggregation/counterfactual choices on gpt2-small IOI, the discovered circuit's **size ranges from 5 to 21 edges** and Jaccard-to-median from 0.042 to 1.000, while circuit error stays flat at 0.10–0.14 (Table 9).

> "We uncover a fundamental instability at this base layer: exact, single-input CMA scores exhibit high intrinsic variability, implying that the causal effect of a component is a volatile random variable rather than a fixed property." (Abstract)

> "In IOI, the overlap between EAP-IG-inputs and Clean-corrupted is also negligible (0.071). This implies that different EAP variants are not converging on the same circuit, but are instead isolating different artifacts of the high-variance edge distribution." (§5.3)

> "We observe a notable degradation in stability for larger models. While gpt2-small yields relatively clustered results, Llama-3.2 (1B and Instruct) exhibits higher variability." (§5.2)

> "Non-identifiability is a theoretical property ... Estimator instability (what we measure) is an empirical symptom ... High instability is consistent with non-identifiability, but does not prove it" (§6.1)

> "As a preliminary guideline, a mean pairwise Jaccard index above 0.8 under bootstrap resampling (with n≥100 resamples) could serve as a reasonable minimum bar for reporting a circuit as stable." (§6.2)

Variation is over data resamples and hyperparameters, **not** over training seeds.

---

### Syed, Rager, Conmy — "Attribution Patching Outperforms Automated Circuit Discovery"

- **arXiv:** 2310.10348. **Venue:** Proceedings of the 7th BlackboxNLP Workshop, pages 407–416, November 15, 2024, ACL (printed on the anthology PDF header).
- **Model for IOI:** GPT-2 small. **Tasks:** IOI, Docstring, Greater-Than.
- **What it did.** Introduced Edge Attribution Patching (EAP): score every edge by a first-order Taylor approximation to activation patching, keep the top k. Compared EAP against ACDC by ROC/AUC on the three tasks.
- **Bears on:** method comparison, faithfulness of the linear approximation.

> "The ROC curves in Figure 3 suggest the performance of EAP is better than ACDC overall: it has the maximal AUC when applied to the IOI and greater than tasks, while ACDC used with the KL Divergence metric outperforms EAP in the docstring task." (§4.1)

**Numeric AUCs are not printed** — Figure 3 shows the ROC curves only. The one IOI number in the text is that "there are only 6 edges outside of the interval [−0.25, 0.25] that aren't part of the IOI circuit" (§4.2, Figure 4). Note that they use task-specific metrics rather than KL divergence, because attribution patching has a zero gradient at the KL minimum (§3.3). Their approximation-quality check (R² = 0.27, best-fit gradient 0.531) is on **Docstring, not IOI** (§5.1).

Activation patching was not run on IOI: "Activation patching was not included in the other tasks as it was too computationally expensive to run on the GPT-2 small models used by IOI and Greater-Than" (§4.1).

---

### Arad, Belinkov, Chen, Kim, Mohebbi, Mueller, Sarti, Tutek — "Findings of the BlackboxNLP 2025 Shared Task: Localizing Circuits and Causal Variables in Language Models"

- **arXiv:** 2511.18409. **Venue:** BlackboxNLP 2025 shared task findings.
- **Models:** Llama-3.1 8B, Gemma-2 2B, Qwen-2.5 0.5B, GPT-2 Small (117M), restricted to model/task pairs where accuracy ≥ 75%.
- **Tasks:** IOI, Arithmetic, MCQA, ARC (circuit track); RAVEL and others (causal-variable track). IOI: 10000 train / 10000 val / 1000 public + 1000 private test.
- **What it did.** Ran the MIB circuit-localization and causal-variable tracks as a shared task, scoring submissions on a private test set with CPR and CMD under counterfactual ablation.
- **Bears on:** replication across models, method comparison.

IOI results, private test set. **CMD (lower is better)** for GPT-2 Small: Random 0.75; EAP (mean) 0.29; EAP (CF) 0.03; EAP-IG-inputs (CF) 0.03; EAP-IG-activations (CF) 0.03; best submissions 0.02. **CPR (higher is better)** for GPT-2 Small: EAP (mean) 0.29; EAP (CF) 1.20; EAP-IG-inputs (CF) 1.85; NAP (CF) 0.28; best submission Hybrid-Ens 2.43.

> "The indirect object identification (IOI) task, first proposed by Wang et al. (2023), is one of the most studied tasks in MI." (§2.1)

> "That said, there is no clear winner; the best method appears to depend on the chosen metric." (§3.4)

> "We do not report results for ARC or IOI, as no submissions were made for these tasks." (Table 4 caption, causal-variable track)

---

### Venkatesh — "Architecture, Not Scale: Circuit Localization in Large Language Models"

- **arXiv:** 2605.08853. **Venue:** not stated in the text. Single author.
- **Models:** Pythia-160M, Pythia-1.4B, Pythia-6.9B (multi-head attention); Qwen2.5-0.5B, Qwen2.5-1.5B, Qwen2.5-7B (grouped-query attention). **No GPT-2.**
- **Tasks:** IOI (primary), induction, factual recall.
- **What it did.** Held task fixed and varied attention architecture and scale, measuring how concentrated the IOI circuit is (top-head ablation effect; number of greedy ablations to reach 80% task damage).
- **Bears on:** replication across models and scales.

Table 1 (IOI): Pythia-160M top-head score 0.108, 5 heads to 80% damage; Pythia-1.4B 0.231, 2 heads; Pythia-6.9B 0.250, 3 heads; Qwen2.5-0.5B 0.772, 1 head; Qwen2.5-1.5B 1.860, 1 head; Qwen2.5-7B 0.948, 1 head.

> "Architecture predicts circuit geometry more reliably than scale. GQA models produce circuits that concentrate into one or two heads across all three tasks. MHA models produce circuits that spread across tens to hundreds of heads." (§1)

> "For Qwen2.5-0.5B and 1.5B, ablating the single top head causes logit difference to flip sign. The model actively predicts the wrong name after ablation." (§5.1)

> "Ablating a randomly chosen mid-layer head as a negative control causes no damage and in several cases improves logit difference. This confirms the effect is circuit-specific and not a general consequence of value zeroing." (§5.1)

> "We cannot fully separate architecture from training. Pythia and Qwen2.5 differ in training data, tokenizer, and training recipe in addition to attention mechanism." (§7, Limitations)

---

### Naser Moghadasi & Ghaderi — "Reading Task Failure Off the Activations: A Sparse-Feature Audit of GPT-2 Small on Indirect Object Identification"

- **arXiv:** 2605.22719. **Venue:** not formally stated (§V-C references IEEE Big Data scale; reference [40] is described as a companion submission).
- **Model:** GPT-2 small, with the layer-8 residual-stream SAE from the `gpt2-small-res-jb` release (24,576 features, hooked at `blocks.8.hook_resid_pre`).
- **Task:** IOI, 300 procedurally generated prompts (29 first names, 8 objects, 8 locations, 4 templates).
- **What it did.** Compared SAE feature activations on failed versus successful IOI trials, with Welch t-tests and Holm–Bonferroni correction across all 24,576 features, then ran three controls: causal ablation of the top feature, a raw-residual-stream AUC baseline, and a seed sweep.
- **Bears on:** sparse-autoencoder analysis of IOI, confounds, correlation vs. causation.

Accuracy 239/300 = 79.7%. Of 24,576 features, **146 clear Holm–Bonferroni at α = 0.05**; 105 reach |Cohen's d| > 0.8. Top feature 17,491: d = +2.93, mean activation 10.28 on failures vs 0.18 on successes; 42 of 61 failed trials activate it, 3 of 239 successful trials do.

The controls are the interesting part, and all three are negative:

> "Accuracy on the 45 keys prompts moved from 6.7% to 4.4% (a -2.2 pp shift in the wrong direction); on the other 255 prompts it was unchanged." (§IV-D, Control 1)

> "the raw residual stream reaches AUC = 0.929, essentially indistinguishable from the top-100 SAE features (0.927) and the full 24,576 SAE features (0.933)." (§IV-D, Control 2)

> "Feature 17,491 was the top feature in 1 of the 5 seeds (the one we originally ran, seed 42); in the other four runs the top feature was one of {7536, 7536, 10960, 19149}." (§IV-D, Control 3)

The dominant effect turns out to be a lexical confound: 45 prompts use "the keys," of which 42 fail (93.3%) versus 7.5% of the rest (Fisher exact p = 8.79 × 10⁻³³). Conditioning on the keys-free subset drops the significant-feature count from 146 to 5 (§IV-F).

> "The methodological lesson is that sparse-feature audits surface correlates, not causes, and that the distinction matters for the kinds of claims a downstream reader will infer." (§V-A)

---

### Palumbo, Mangal, Wang, Vijayakumar, Păsăreanu, Jha — "Validating Mechanistic Interpretations: An Axiomatic Approach"

- **arXiv:** 2407.13594. **Venue:** not stated in the text.
- **Models:** a two-layer ReLU decoder-only transformer trained by the authors on 2-SAT, and Nanda et al.'s modular-addition model. **No language model above toy scale.**
- **Task:** 2-SAT and modular addition. **IOI appears only as a worked sketch in Appendix I, with no numerical results.**
- **What it did.** Defined four axioms — ε-prefix equivalence, ε-component equivalence, ε-prefix replaceability, ε-component replaceability — that a mechanistic interpretation should satisfy, estimated ε from test-set violation counts with Clopper–Pearson intervals, and applied them to the two toy models.
- **Bears on:** formal criteria for validating an interpretation; a documented reason why the IOI circuit cannot be evaluated as stated.

> "We do not fully evaluate IOI with our axioms here as Wang et al. (2023) leaves key components of the interpretation unspecified. In particular, the authors do not clearly state how the model combines the information produced by redundant heads performing the same function, and the authors do not conclusively state what the duplicate-token suppressing information output by the S-inhibition heads represents." (Appendix I)

> "While causal abstraction is a very general framework for the validation of mechanistic interpretations, in practice, it uses the specific metric of interchange intervention accuracy (Geiger et al., 2022) to validate interpretations and this metric fails to directly evaluate the equivalence of internal representations." (§3)

---

### Shi, Beltran-Velez, Nazaret, Zheng, Garriga-Alonso, Jesson, Makar, Blei — "Hypothesis Testing the Circuit Hypothesis in LLMs"

- **arXiv:** 2410.13032. **Venue:** not stated in the arXiv text; the file contains a NeurIPS paper checklist.
- **Model for IOI:** GPT-2 small. "Both IOI and greater-than use GPT-2 small, while the other tasks use various small Transformers" (§4.1). Other circuits: Induction (2-layer attention-only), Docstring (4-layer attention-only), two Tracr models.
- **What it did.** Turned three idealized circuit criteria into statistical hypothesis tests — Equivalence (a sign-type test), Independence (HSIC permutation test), Minimality (a tail test against inflated circuits) — plus two relaxed tests, Sufficiency and Partial Necessity, scored against random-walk reference circuits.
- **Bears on:** minimality (primary), necessity, sufficiency, ablation-method dependence.

The three criteria, as printed in §1:

> "1. Mechanism Preservation: The performance of an idealized circuit should match that of the original model.
> 2. Mechanism Localization: Removing the circuit should eliminate the model's ability to perform the associated task.
> 3. Minimality: A circuit should not contain any redundant edges."

Results for IOI: fails all three idealized tests (Table 1); passes the relaxed Sufficiency test up to 90% model size and the relaxed Partial Necessity test under both reference distributions (§4.2, Table 2). Equivalence test statistic 0.24 — "the proportion of times C\* outperforms M on the task" (Table 3). Independence HSIC 0.001 at p = 0.01 (Table 4).

> "For IOI, we can remove about 20% of the edges. However, we notice that the faithfulness of IOI does not vary monotonically as more edges are knocked out, revealing the complex mechanisms of circuits (e.g., negative mover heads)." (§4.2)

> "All circuits except IOI are much worse than the original model at the task." (Appendix E.1)

> "Surprisingly, we observed that for G-T and IOI, knocking down the complete model has less impact than knocking down the candidate circuit. This pattern appears with the STR ablation scheme but is absent with zero-ablation." (§4.2)

> "These findings suggest that the knockdown metric alone is insufficient to assess circuit quality, particularly when using STR ablation, as it is sensitive to artifacts from the validation dataset." (§4.2)

> "The results suggest that while existing circuits do not strictly adhere to the idealized hypotheses, they are far from being random subnetworks." (§5)

Limitation stated by the authors: "the empirical study uses the original experimental setup, whereas existing work and our ablation studies show that circuits are not robust to changes in the experimental setup" (§5).

---

### Chen, Jin, Niu, Yin, Zhao, Guo, Metaxas, Wang, Yue, Penn — "All Circuits Lead to Rome: Rethinking Functional Anisotropy in Circuit and Sheaf Discovery for LLMs"

- **arXiv:** 2605.12671 (v1 line printed: `[cs.CL] 12 May 2026`). **Venue:** not stated; ICML style markers present.
- **Models:** GPT-2 Small (main), Pythia-160M (Appendix H). "All results are reported on GPT-2, as it is the only model commonly supported by all prior CSD methods" (§3, footnote).
- **Tasks:** IOI (flagship, an equal mix of BABA and ABBA), BLiMP, four DNA/AGA/ANA variants, Docstring.
- **What it did.** Named the implicit "Functional Anisotropy Hypothesis" — that a capability corresponds to a unique privileged mechanism — and attacked it with Overlap-Aware Sheaf Repulsion, which adds an explicit penalty on reusing edges from previously discovered sheaves. Then scaled to 20 sheaves per task, replicated non-uniqueness under ACDC / EAP / Edge Pruning, and proved an existence theorem.
- **Bears on:** rival circuits (primary), minimality, necessity.

| Quantity | Value | Location |
| --- | --- | --- |
| Two rival IOI sheaves | both 100% accuracy; edge density 3.56% and 3.97%; **edge IoU 4.1%** | Table 1 |
| Twenty IOI sheaves | shared core 11 edges of a 7382-edge union; mutual IoU 0.15%; all ≈99.6% accurate | Table 3 |
| Node-level IoU on IOI | **64.2%** | Appendix D, Table 8 |
| Seed-only baseline (no repulsion) | IOI two-sheaf IoU 18.5% | Appendix G, Table 10 |
| Ultra-sparse sheaf | 3 edges, 86.7% IOI accuracy in isolation, complement 31.3% | §4, Table 6 |
| Single-edge ablation of the 3-edge core in the full model | remove any one → 99.8–99.9%; remove any two → ~31.5% | Table 7 |
| Core removed, task decomposed | C_BABA reaches 94.9% on IOI-BABA; C_ABBA 96.7% on IOI-ABBA | §4 |
| ACDC, varying only head traversal order | interchange: `|E∩|` 174, `|E∪|` 608; zero: `|E∩|` 302, `|E∪|` 6951 | Table 4 |
| Pythia-160M IOI | mutual IoU 0.34–0.45%, accuracy ~80% | Appendix H, Table 11 |

> "We show that a single LLM task can instead be supported by multiple, structurally distinct circuits or sheaves that are simultaneously faithful, sparse, and complete." (Abstract)

> "Notably, their overlap is extremely small: the intersection-over-union, IoU (A,B), is only 4.1%, which is close to the overlap expected by chance." (§3.1)

> "In this sense, functional anisotropy appears not as a fundamental property of the model, but as an artefact of searching for a single solution in a space that admits many." (§3.2)

> "Locally, within the three-edge sheaf, removing any single edge leaves performance essentially unchanged." (§4)

> "Unless otherwise stated, inactive edges are zero-ablated: information is allowed to flow only through selected edges, and pruned edges contribute zero to downstream components." (§2.1)

**Caveat to carry with the 4.1% figure.** Node IoU on IOI is 64.2% (Appendix D, Table 8) — the near-disjointness is in routing, and the discovery objective penalizes edge sparsity only. The paper also warns that its own seed-only baseline of ~20% IoU "may be misinterpreted as algorithmic stability, given the gradient-based nature of the method" (Appendix G). "Sheaves" are a stronger object than circuits: they must reproduce behavior standalone under zero ablation.

---

### Méloux, Portet, Maniu, Peyrard — "Everything, Everywhere, All at Once: Is Mechanistic Interpretability Identifiable?"

- **arXiv:** 2502.20914. **Venue:** ICLR 2025 (per `references.bib`; not stated in the arXiv text). Author order in the arXiv file is Méloux, Portet, Maniu, Peyrard.
- **Models: toy MLPs only.** A two-hidden-layer MLP on XOR; MLPs of shape `(2,k,k,n)` on parallel Boolean gates; one `(784,128,128,3,3,3,1)` MLP on MNIST digits 0 and 1. **No transformer, no GPT-2, no IOI experiment.**
- **What it did.** Defined identifiability of a mechanistic explanation as the property that, under fixed validity criteria, a unique explanatory algorithm satisfies them. Then exhaustively enumerated circuits and variable-mappings in small trained networks and counted how many satisfy the criteria.
- **Bears on:** rival circuits — as a framework and a proof of concept, not as an IOI result.

> "An MI strategy is not identifiable if its standards of validity do not discriminate between two incompatible explanations." (§2.4)

> "Our experiments reveal overwhelming evidence of non-identifiability in all cases: multiple circuits can replicate model behavior, multiple interpretations can exist for a circuit, several algorithms can be causally aligned with the neural network, and a single algorithm can be causally aligned with different subspaces of the network." (Abstract)

> "Less than 2% of the trained networks contain exactly one valid minimal mapping, and no network contains exactly one circuit interpretation." (§4.1.1)

> "In our experiments, simplicity or sparsity cannot single out one explanation." (§5.2)

**The scope caveat, in the authors' own words:** "Our experiments focus on toy MLPs trained on toy tasks, which differ drastically from large language models (LLMs) trained on vast, complex datasets using Transformer architectures" (§5.4). **IOI appears in this paper exactly twice — once as a background citation to Wang et al. in §2.1, and once in the bibliography.** Any claim that this paper demonstrated non-identifiability on IOI or on GPT-2 is false.

Appendix C is separately useful: it collects phrasings from six circuit papers ("the curve circuit", "discover the circuit") showing uniqueness is assumed tacitly, and states "Identifiability is, to the best of our knowledge, never stated as an explicit assumption in existing works about circuits."

---

### Mueller et al. — "MIB: A Mechanistic Interpretability Benchmark"

- **arXiv:** 2504.13151. **Venue:** ICML 2025 (per `references.bib`; the arXiv text carries only the ICML keyword line).
- **Models:** GPT-2 Small (117M), Qwen-2.5 0.5B, Gemma-2 2B, Llama-3.1 8B, plus a purpose-trained InterpBench-style model (6 layers, 4 heads, d_model 64).
- **Tasks:** IOI, Arithmetic, MCQA, ARC in the circuit track; RAVEL and others in the causal-variable track. IOI is run on all five models in the circuit track and on GPT-2 Small only in the causal-variable track.
- **What it did.** Built a two-track benchmark with fixed splits, fixed counterfactual pairs, a private test set, and two new metrics; ran 11 circuit-localization baselines under three ablation types.
- **Bears on:** method comparison, replication across models, metric definition.

Metric definitions, as printed:

> "we split faithfulness into two metrics: (i) the integrated circuit performance ratio (CPR), and (ii) the integrated circuit-model distance (CMD). CPR prioritizes methods that locate components with a positive effect on model performance on the task; higher is better. CMD prioritizes methods that locate components with any strong effect on model performance, including negative effects; 0 is best." (§3.1)

Faithfulness is `f(C,N;m) = (m(C) − m(∅)) / (m(N) − m(∅))` with m the logit difference; CPR and CMD integrate it over circuit size k.

IOI results (public test, CMD lower is better): Random 0.75 (GPT-2), 0.72 (Qwen), 0.69 (Gemma), 0.74 (Llama); EAP-IG-activations (CF) 0.03 / 0.01 / 0.03 / 0.01; edge activation patching 0.02 on GPT-2 but 0.49 on Qwen. CPR (higher better): EAP-IG-inputs (CF) 1.85 / 1.63 / 3.20 / 2.08; edge activation patching 2.30 on GPT-2 (Tables 2, 14).

> "More surprisingly, edge activation patching (EActP) does not always perform best, despite computing exact IEs for each edge: it dominates for IOI on GPT-2, but not Qwen-2.5 or InterpBench." (§3.3)

> "Circuits found with CF ablations outperform those found with mean or optimal ablations; the latter two score similarly to each other." (§3.3)

> "Prior implementations of minimality require manual analysis of the circuit (Wang et al., 2023); our formulation is more general, though it is useful primarily as a relative comparison point, rather than an absolute measure." (§3.1, footnote 7)

**Is the Wang et al. circuit used as ground truth? No.** The only edge-level ground truth is the purpose-trained model, which "implements a simplified version of the IOI circuit described by Gupta et al. (2024)" (Appendix E). Wang et al. supply the task, the counterfactual definitions, and the four S-inhibition heads (7.3, 7.9, 8.6, 8.10) that scope the causal-variable baselines.

Completeness is acknowledged as untestable here: "there exist metrics such as completeness that cannot be tractably computed without access to the ground-truth set of causally relevant components" (Appendix B).

MIB's causal-variable track refits Wang et al.'s S-inhibition regression on its own data: Wang's reported `2.31·PositionSignal + 0.99·TokenSignal` becomes `0.048 + 2.005·PositionSignal + 0.768·TokenSignal` (Appendix F.5.4). SAE features do not beat neurons: "SAE and PCA features generally fail to improve upon neurons, i.e., standard dimensions of hidden vectors, as a unit of analysis" (§4.7).

---

### Zhang & Nanda — "Towards Best Practices of Activation Patching in Language Models: Metrics and Methods"

- **arXiv:** 2309.16042. **Venue:** not stated in the arXiv text. Note the printed title ends "Metrics and Methods," not "Metrics and Methodology."
- **Models:** GPT-2 small for IOI and greater-than; GPT-2 XL and GPT-2 large for factual recall; GPT-J for arithmetic; a 4-layer attention-only model for docstrings.
- **What it did.** Varied four degrees of freedom in activation patching — corruption scheme (Gaussian noising vs symmetric token replacement), evaluation metric (probability, logit difference, KL divergence), sliding-window vs single-layer MLP patching, and which tokens to corrupt — and measured whether the localization conclusion changed.
- **Bears on:** ablation-method dependence (primary), metric dependence, confounds.

The IOI results are the sharpest demonstration. Table 1 gives detection counts by head class under six corruption × metric combinations; for any fixed metric, the two corruption schemes detect different head sets. Under S2 corruption every combination misses at least two of the three Name Mover Heads (Tables 1, 5). Under S1+IO corruption all three Name Movers are found by five of six combinations, but then no S-Inhibition Heads are found at all (Table 4).

> "We remark that all the detections are in the IOI circuit as found by Wang et al. (2023). However, the discovery we achieved here appear far from complete, with some critical misses such as NM. This suggests that the extensive manual inspection and the use of path patching, a more surgical patching method, are both necessary to fully discover the IOI circuit." (§3.1)

> "Indeed, on 500 clean IOI prompts, the NMs assign an average of 0.58 attention probability to IO. ... with GN corruption, we see that the attention is shared between IO and S1 (0.26 and 0.21). This suggests that GN not only removes the relevant information but also disrupts the internal mechanism of NMs on IOI sentences." (§3.2)

> "In general, probability must fail to detect negative model components, if corruption reduces the correct token probability to near zero." (§4.2)

> "While this may seem an implementation detail, we find that this can greatly affect the localization outcomes." (§6, on which tokens to corrupt)

> "More broadly, this presents a challenge to any intervention techniques that introduce OOD inputs to the model or its internal layers, including ablations." (§6)

Their recommendations: symmetric token replacement over Gaussian noising; logit difference over probability; single-layer before sliding-window; try multiple corruption targets. The stated reason for preferring logit difference is IOI-specific — it "controls for" components that boost all names (§6).

---

### Goldowsky-Dill, MacLeod, Sato, Arora — "Localizing Model Behavior With Path Patching"

- **arXiv:** 2304.05969. **Venue:** not stated in the arXiv text.
- **Models:** a 2-layer attention-only transformer trained on OpenWebText (induction); GPT-2 small and GPT-2 XL (a number-continuation behavior).
- **IOI is not used.** There is no IOI experiment in this paper. It generalizes the method Wang et al. introduced.
- **Bears on:** method definition, metric choice.

> "Path patching was first introduced in Wang et al. (2022), where they considered a sender attention head that interacted with the key, query, or value inputs of one or more receiver attention heads." (§1)

> "In this work, we generalize path patching to test hypotheses containing any number of paths from input to output in an arbitrary computational graph." (§1)

Its one substantive comment on the IOI result is a metric criticism:

> "Wang et al. (2022) combine mean ablation with a simple form of path patching and identify a circuit of 26 attention heads that explain GPT-2 small's ability to identify indirect objects on a synthetic dataset. Their faithfulness metric is a difference of expectations, which is susceptible to the same possibility of cancellation described in Scheurer et al. (2023)." (§6.3)

Two further caveats worth quoting for any faithfulness discussion:

> "Therefore, it's important to interpret AUE-based metrics in terms of sufficiency and not completeness." (§7.1)

> "However, without a ground truth it's impossible to conclusively say which of the plots is more representative of the true mechanism." (§4, on path patching vs input corruption)

---

### Heimersheim & Nanda — "How to use and interpret activation patching"

- **arXiv:** 2404.15255. **Venue:** not stated in the arXiv text.
- **Models:** none run. This is a practitioner's guide with no experiments; the only model named is GPT-2 medium in an illustrative figure caption. IOI is used as a running example, attributed to Wang et al. on GPT-2 small.
- **Bears on:** interpretation caveats, corrupted-distribution choice.

The self-repair caveat, in full:

> "In some cases researchers have discovered 'Backup heads', components that are not normally doing the task but jump into action of other components are disrupted. For example, in IOI when one ablates a name mover head (a key component of the circuit) a backup name mover head will activate and then do the task instead." (§3.2)

> "It can be helpful to think of these as OR-gates where either component is sufficient for the model to work. This does not fit well into our attempts of defining a circuit, nor plays well with the circuit finding methods above. Despite the name mover heads being important, if we ablate them then, due to backup heads compensating, the name movers look less important. Fortunately, backup behaviour seems to be lossy ... (the Hydra effect paper found 0.7*X)." (§3.2)

The negative-component caveat:

> "This is problematic, because it makes it hard to judge the quality of a circuit analysis: it may look like we've fully recovered (or more than fully recovered!) performance, by finding half the positive components but excluding all negative ones. This is an unsolved problem." (§3.2)

And on scope:

> "More generally, activation patching is always based on prompt distributions, and does not make statements for model behaviour outside these specific distributions." (§3.2)

> "We typically make no claims that we have found the smallest such collection of components, we only test that this collection is sufficient." (§3.2)

§2.6 tabulates six different corrupted-prompt schemes for the same IOI sentence and what each one traces, which is the most compact statement anywhere of how much the corruption choice determines what "the IOI circuit" means.

---

### McGrath, Rahtz, Kramár, Mikulik, Legg — "The Hydra Effect: Emergent Self-repair in Language Model Computations"

- **arXiv:** 2307.15771. **Venue:** not stated in the arXiv text.
- **Model: Chinchilla 7B only. Task: factual recall on Counterfact (1,209 prompts), ablating whole attention and MLP layers.** **No IOI experiment and no GPT-2 run.**
- **Bears on:** self-repair as a confound on necessity tests — as a general result, established on a different model and task.

> "The Hydra effect (referred to in (Wang et al., 2022) as backup behaviour) complicates our understanding of what it means for a network component to be important because two natural-seeming measures of importance (unembedding and ablation-based measures) become much less correlated than we would naïvely expect." (§1)

> "These findings corroborate earlier work on neural network computations in GPT-2 Small (Wang et al., 2022) which reported a similar effect that the authors term 'backup heads'. The authors of (Wang et al., 2022) hypothesised that dropout (Srivastava et al., 2014) was responsible for self-repair behaviour, which we disprove as the model we study (Chinchilla 7B) was trained without any form of dropout or stochastic depth." (§6)

This refutes Wang et al.'s own stated hypothesis for backup behavior: "We hypothesize that this compensation phenomenon is caused by the use of dropout during training" (Wang et al. §3.4).

Headline numbers: 92% of the variance in downstream direct effect is explained by compensation at attention layer 23 of 32 (§4.2, Figure 7b); the Hydra effect plus reduced MLP erasure "collectively act to restore approximately 70% of the reduction in token logits" at middle layers (§6).

> "The Hydra effect poses a challenge to automating ablations: if we prioritise network components for ablation according to their total effect, we will be using a measure that does not fully reflect the computational structure of the intact network." (§6)

Note: the file's §2.2 attributes Counterfact to "Wang et al., 2022," which the reference list resolves to the IOI paper. This is a citation error in the source; Counterfact is from Meng et al.

---

### Rushing & Nanda — "Explorations of Self-Repair in Language Models"

- **arXiv:** 2402.15390. **Venue:** not stated in the arXiv text.
- **Models:** Pythia-1B / 410M / 160M, GPT-2 Small, GPT-2 Medium, Llama-7B, on **1 million tokens of The Pile** — the full pretraining distribution, not a narrow task. **No IOI experiment is run.**
- **Bears on:** whether self-repair invalidates circuit discovery.

> "Past literature has looked at self-repair in incomplete settings: self-repair was first discovered in the Indirect Object Identification distribution as 'Backup Behavior' (Wang et al., 2023), for which the behavior was explained partially as a byproduct of Copy Suppression (McDougall et al., 2023)." (§1)

> "A nontrivial fraction - possibly 30% - of the self-repairing of direct effects can be attributed to just the effect of ablations on the LayerNorm normalization factor." (§1)

Their assessment for circuit discovery is the most reassuring of the self-repair papers, with a caveat that points directly at IOI:

> "However, fortunately, circuit analysis only requires identifying whether a component is important or unimportant (i.e. whether it belongs in the sparse subgraph), not the precise effect of ablating it. So the fact that self-repair is imperfect across the general distribution (Section 2.2) helps reduce some of the concerns for circuit discovery efforts; because the 'importance' of various components is extremely heavy-tailed, even a significant fractional decrease in the estimated effect won't change which nodes are important." (§5.1)

> "However, this doesn't fully alleviate all concerns. In certain situations, self-repair can be lossless or overcompensate. This may happen on certain narrow distributions or may be induced depending on what tools you use. And if the degree of self-repair differs significantly between components, borderline components may be incorrectly included or excluded." (§5.1)

IOI is a narrow distribution, so the caveat applies to it directly. On the Backup Name Movers:

> "The fact that these 'Backup' heads can perform moving behavior suggests that they have the capability to perform Name Moving, but don't do so in the Indirect Object Identification task." (§5.3.1)

---

### McDougall, Conmy, Rushing, McGrath, Nanda — "Copy Suppression: Comprehensively Understanding an Attention Head"

- **arXiv:** 2310.04625. **Venue:** not stated in the arXiv text.
- **Models:** GPT-2 Small (primary), GPT-2 Medium and Pythia (Appendix B), Stanford GPT-2 Small E (Appendix Q).
- **Tasks:** the OpenWebText training distribution (primary), IOI (§4), induction/anti-induction (Appendix A). IOI is used on GPT-2 small: "we use the narrow Indirect Object Identification (IOI; Wang et al. (2023)) task to study self-repair, as this was studied in the GPT-2 Small model" (§4.1).
- **Bears on:** negative components, self-repair, task-specificity.

L10H7 in GPT-2 small is a Negative Name Mover Head in Wang et al.'s taxonomy. This paper explains it as **copy suppression**: attend back to a token that earlier components predicted, then write to decrease that token's logit.

| Quantity | Value | Location |
| --- | --- | --- |
| Effect of L10H7 explained by copy-suppression-preserving ablation on OpenWebText | 76.9% | Abstract; §3.3.2 |
| OV ablation alone / QK ablation alone | 81.1% / 95.2% | §3.3.2 |
| Vocabulary tokens whose OV diagonal is in the top-10 most negative of its column | 84.70% (98.86% in the bottom 5%) | §3.1 |
| Share of IOI self-repair explained by L10H7 and L11H10 after Name Mover ablation | **39%** | Abstract; §4.1 |
| Negative Heads' IO-minus-S1 attention once their Name Mover input is replaced | 0.08 (L10H7), 0.0006 (L11H10) | Appendix P |

> "We show that self-repair is implemented by several mechanisms, one of which is copy suppression, which explains 39% of the behavior in a narrow task." (Abstract)

> "Ideally, ablations would provide accurate measures of the importance of model components on given tasks, but negative and backup components complicate this assumption. Firstly, negative components may be ignored by attribution methods that only find the positive components that complete tasks. This means that these attribution methods will not find faithful explanations of model behavior. Secondly, backup components may counteract the effects of ablations and hence cause unreliable importance measurements." (§1)

§4.1 also separates two distinct self-repair mechanisms: Negative Heads attend *more* to the predicted token and suppress it less, while Backup Heads attend *less* and copy more. §4.2 finds that for most backup heads "projecting away from W_U[IO] does not change the heads' logit differences much," so the unembedding direction is not causally central to their repair.

---

### Gong, Zeng, Yuen, Lim — "Conditional Co-Ablation: Recovering Self-Repair Backups in Transformer Circuits"

- **arXiv:** 2607.01940. **Venue:** arXiv preprint.
- **Models:** GPT-2 small (IOI headline), GPT-2 medium/large for scale, plus Pythia, GPT-Neo, Gemma-2, OLMo-2, Llama-3.1, Qwen-2.5 for induction. IOI ground-truth head labels come from Wang et al.
- **What it did.** Defined a second-order score — the conditional growth in a head's ablation energy *after* a primary seed set has been removed — and used it to recover the eight documented Backup Name Mover Heads from among 141 candidates.
- **Bears on:** necessity (primary), completeness, ablation-method dependence.

| Quantity | Value | Location |
| --- | --- | --- |
| Backup-head recovery ROC-AUC, single ablation | 0.33 ± 0.00 | Table 1 |
| Backup-head recovery ROC-AUC, CoAx | **0.91 ± 0.00** | Table 1 |
| Best gradient baseline (AtP\* GradDrop) | 0.82 ± 0.03 | Table 1 |
| Ablating name-mover primaries only | IOI accuracy 1.00 → 0.97; logit difference drop 0.22 from clean 2.53 | §1, Table 4 |
| Ablating primaries + 8 backups jointly | drop 1.15, vs 0.60 predicted by summing singles — **1.9× super-additive** | §C.3.2 |
| Share of repair causally carried by dormant backups | 55% (per-seed 53, 53, 55, 57) | §3.2, §C.2.2 |
| Circuit completeness gap | first-order circuit 0.72; + CoAx backups 0.15; complete documented circuit 0.16; matched-random completion 0.61 | §3.3 |

> "In GPT-2-small IOI, for example, ablating the name-mover heads that write the answer reduces the task logit-difference by only 0.22 from a clean value of 2.53, because backup name-movers take over. The larger effect appears only when the backups are removed as well. This is not a noisy measurement artifact but rather a violation of additivity: the IOI name-mover module is 1.9× super-additive, so the effect of removing a set is not the sum of the effects of removing its members." (§1)

> "Self-repair is precisely a completeness failure (it is how the IOI backups were first noticed), so completeness is the criterion that most sharply separates CoAx from first-order discovery." (§3.3)

> "Component importance is therefore not merely an isolated-unit property: in robust circuits, the components that matter can become visible only under the interventions that make them necessary." (Abstract)

The 0.91 is a *completion* result seeded with the documented primaries, not standalone discovery: "as a standalone finder that must detect its own seed, CoAx peaks at 0.60 ... below the seed-free AtP⋆ (0.82). The 0.91 headline is thus a completion result with documented primaries as the seed" (§3.1). A simple co-activation control reaches comparable AUC (0.92–0.93) but over-ablates. The method does not transfer to the MLP-dominated greater-than circuit (1.5× over random, within one standard deviation).

---

### Bhaskar, Wettig, Friedman, Chen — "Finding Transformer Circuits with Edge Pruning"

- **arXiv:** 2406.16778. **Venue:** not stated in the arXiv text.
- **Models:** GPT-2 Small (117M) for all language tasks; CodeLlama-13B for a scaling case study; two Tracr models.
- **Tasks:** IOI-t1 (single template), IOI (30 templates from `fahamu/ioi`), Greater Than, Gendered Pronoun.
- **What it did.** Recast circuit discovery as continuous optimization over per-edge masks on a disentangled residual stream, with L0 regularization and a Lagrangian sparsity target; masked edges are replaced by interchange activations.
- **Bears on:** minimality, method comparison.

> "Specifically, on IOI, Edge Pruning finds a circuit of 98.8% sparsity that is as faithful and performs as well as the one found by ACDC at 96.8% sparsity—using over 2.65× fewer edges." (§4.2)

Table 1 (multi-template IOI, faithfulness as KL to the full model at 96.6 ± 0.1% sparsity): ACDC 0.92 / EAP 3.47 / Edge Pruning 0.25 at 200 examples; 0.88 / 3.66 / 0.22 at 400; ACDC unavailable / 3.78 / 0.20 at 100K. Runtimes on one H100: ACDC 18,783 s, EAP 21 s, Edge Pruning 2,756 s at 200 examples.

The only comparison with the Wang et al. circuit is a node-level ROC AUC in Figure 7, described qualitatively: "The AUC is slightly higher for Edge Pruning on IOI, and slightly lower on GT." **No numeric AUC appears in the text.**

> "Nevertheless, we emphasize that manually reverse-engineered circuits are not guaranteed to be optimal since they also investigate one ablation at a time without considering interactions between ablations." (Appendix B)

> "Finally, we note that even with perfect faithfulness to the model outputs, a circuit can misrepresent the necessary computations in the full model, thus leading to interpretability illusion (Makelov et al., 2024)." (Limitations)

Seed robustness: 12 discovery seeds at 97.5% sparsity give pairwise IoU 0.5–0.7 (Appendix D). This varies the search, not the trained model.

---

### Li & Janson — "Optimal ablation for interpretability"

- **arXiv:** 2409.09951. **Venue:** NeurIPS 2024 (per the published proceedings; not stated in the arXiv text).
- **Models:** GPT-2-small for IOI and Greater-Than; GPT-2-XL for factual recall and latent prediction; GPT-2 small/medium/large in Appendix H.
- **What it did.** Proposed replacing a component's activation with a single learned constant chosen to minimize the ablated model's expected loss, proved this is the lower bound over all total ablation methods, and argued the excess for other methods is attributable to "spoofing."
- **Bears on:** ablation-method dependence (primary), minimality.

Single-component ablation on IOI (Tables 1, 2): rank correlation with counterfactual ablation is 0.590 (zero), 0.825 (mean), 0.828 (resample), 0.833 (CF-mean), **0.907 (optimal)**. Median ratio of Δ_opt to Δ: 11.1% (zero), 33.0% (mean), 17.7% (resample).

> "For example, for IOI, at a circuit size of 1,000 edges, ablating excluded components with OA enables the existence of circuits with 32% lower Δ compared to CF, 62% lower Δ compared to mean ablation, and 88% lower Δ compared to resample ablation, and the improvement is even larger at smaller circuit sizes." (§3.2)

> "Unlike other ablation methods, OA indicates that the manual circuits are approximately optimal for their size." (§3.2, section heading)

> "Holding |Ẽ| fixed, the Pareto-optimal Δ_opt is 29% below the Δ_opt of the manual circuit on IOI and 42% below the Δ_opt of the manual circuit on Greater-Than. However, for the other ablation methods, optimized circuits with fewer edges than the manual circuit achieve 84-85% lower Δ than the manual circuit on IOI, and 70-84% lower Δ on Greater-Than." (§3.2)

Their circuit-discovery method finds a 385-edge IOI circuit with Δ_CF = 0.220, "52% fewer edges than the smallest ACDC-identified circuit with comparable Δ_CF" (§3.2).

An IOI-specific diagnosis of why resample ablation misbehaves: "resample ablation loss is relatively low for Greater-Than but relatively high for IOI, indicating that token parallelism is an important requirement for CF to work well" (Appendix F.3).

**This paper is the strongest published argument that the Wang circuit is *not* larger than necessary.** The 84–85% headroom seen under mean, resample, and counterfactual ablation is attributed to spoofing artifacts of those ablation methods rather than to circuit bloat.

---

### O'Neill & Bui — "Sparse Autoencoders Enable Scalable and Reliable Circuit Identification in Language Models"

- **arXiv:** 2405.12522. **Venue:** not stated in the arXiv text.
- **Models:** GPT-2 Small for IOI and greater-than; GPT-2 Medium/Large/XL for wall-time scaling only; a 2-layer attention-only model, Pythia-160M and OPT-125M for induction; four Tracr models.
- **What it did.** Trained a small tied-weight SAE on cached attention-head outputs from ~10 hand-built positive/negative prompt pairs per task, took the argmax feature code per head, and scored heads by how often their code appears only in positive examples.
- **Bears on:** method comparison, sufficiency.

Table 4 (IOI, GPT-2 Small):

| Circuit | Attn. heads | Logit difference |
| --- | --- | --- |
| GPT-2 (clean) | 144 | 3.55 |
| GPT-2 (corrupted) | 144 | −3.55 |
| Wang et al. ground-truth | 26 | **4.11** |
| Theirs | 40 | **3.62** |
| Random complement | 40 | −2.23 |

> "Our circuit achieves a logit difference of 3.62, surpassing the full GPT-2 model's average of 3.55 ... However, our circuit performs slightly worse than the ground-truth circuit identified by [Wang et al.]" (§4.3)

**The commonly circulated "3.62 beats 3.55" framing is incomplete.** Their circuit is larger (40 heads vs 26) and scores lower (3.62 vs 4.11) than the Wang circuit. Table 4's caption states it directly: "Our predicted circuit actually improves on the performance of the full model, albeit not as much as the ground-truth circuit."

Their node-level ROC AUC on IOI is 0.854, against ACDC 0.777 (random ablation) / 0.424 (zero ablation), HISP 0.728, SP 0.797 / 0.479 (Table 6). The zero-vs-random gap for ACDC and SP is another instance of ablation-method dependence.

> "The circuits found by previous researchers through manual inspection may be incomplete [Wang et al.] or include edges that are correlated with model behaviour but not causally active [Zhang & Nanda]." (§6.1)

---

### Nainani, Vaidyanathan, Yeung, Gupta, Jensen — "Adaptive Circuit Behavior and Generalization in Mechanistic Interpretability"

- **arXiv:** 2411.16105. **Venue:** not stated in the arXiv text.
- **Model: GPT-2 small only. Task: IOI only,** with two new prompt formats — DoubleIO (both S and IO duplicated) and TripleIO (IO appears three times).
- **What it did.** Ran the unmodified Wang et al. circuit on the two variants, found it *outperforms* the full model, diagnosed the cause, then re-ran the full path-patching discovery pipeline on each variant.
- **Bears on:** confounds (primary), generalization.

Table 1 (200 prompts per variant):

| Task | Model logit diff | Circuit logit diff | Faithfulness |
| --- | --- | --- | --- |
| Base IOI | 3.484 | 3.119 | 0.895 |
| DoubleIO | 2.118 | 2.722 | **1.285** |
| TripleIO | 1.227 | 3.174 | **2.586** |

> "The IOI circuit vastly outperforms the full model on prompt variants where the IOI algorithm would completely fail. Despite this, most of the attention heads in the circuit still retain their functionalities as specified in Wang et al. (2023)." (§1)

> "We refer to this phenomenon as S2 Hacking. Note that this phenomenon only occurs in the base IOI circuit, as it is a byproduct of the knockout procedure for evaluating the circuit and not actually how the full model solves the task." (§4)

Table 2: newly discovered variant circuits have 100% node overlap with the base circuit and 91.66% / 84.61% edge overlap, needing only added input edges (10 for DoubleIO, 20 for TripleIO).

> "Our findings reveal that the circuit generalizes surprisingly well, reusing all of its components and mechanisms while only adding additional input edges." (Abstract)

Note the internal inconsistency: §3.2 gives the DoubleIO model logit difference as 2.138 while both tables give 2.118; and Table 2's TripleIO faithfulness prints as 0.778 where 0.974/1.227 = 0.794.

---

### Chhabra, Zhu, Khalili — "Neuroplasticity and Corruption in Model Mechanisms: A Case Study Of Indirect Object Identification"

- **arXiv:** 2503.01896. **Venue:** not stated in the arXiv text.
- **Model:** GPT-2-small only. **Tasks:** IOI (primary), Greater-Than (Appendix N).
- **What it did.** Fine-tuned GPT-2-small on clean IOI for 1–100 epochs, and separately on label-poisoned IOI variants, re-running the full Wang et al. circuit-discovery pipeline at each stage. Then fine-tuned corrupted models back on clean data.
- **Bears on:** training/fine-tuning dynamics, circuit stability.

Clean fine-tuning amplifies rather than restructures. Table 1: faithfulness stays 98.4–99.9% across 1–100 epochs while the model's own logit difference rises from 6.32 to 26.83 and sparsity from 1.92% to 2.68%.

> "Concurrently, we observe that task-specific fine-tuning enhances the underlying mechanisms of circuits without introducing novel mechanisms, even in longer training scenarios. The enhancement stems from two sources: (1) amplified capabilities of existing circuit components and (2) emergence of new components that replicate prior mechanisms. We term this phenomenon Circuit Amplification." (§4.1)

Backup Name Mover Heads convert into Name Mover Heads: L10H10's logit attribution rises "from 0.4 to 1.8 on the IOI task" (§4.1).

Corruption is localized to circuit components. Subject Duplication poisoning drives "the average logit difference ... from 3.55 to -11.06 after just 5 epochs" (§4.2), with L9H9 flipping sign and Negative Name Movers flipping to suppress S instead of IO.

Retraining on clean data restores the original circuit: faithfulness 95% (Name Moving reversal) and 96% (Subject Duplication reversal), §5.

---

### Adhikari — "Emergence of Minimal Circuits for Indirect Object Identification in Attention-Only Transformers"

- **arXiv:** 2510.25013. **Venue:** arXiv preprint.
- **Models: attention-only transformers trained from scratch** — no MLPs, no layer norm, 8-dimensional residual stream, 8-token vocabulary. **Task: a symbolic IOI abstraction,** 6-token sequences over two templates. No pretrained model is analyzed.
- **Bears on:** minimality, architectural requirements.

A one-layer, one-head model fails; a one-layer, **two-head** model reaches perfect accuracy; a two-layer one-head model also solves it, primarily through query-composition (ablation drops: Q-composition ≈100%, V ≈93.33%, K ≈26.67%).

> "Surprisingly, a single-layer model with only two attention heads achieves perfect IOI accuracy, despite lacking MLPs and normalization layers." (Abstract)

> "Furthermore, a detailed analysis of this model uncovers a highly compact and interpretable circuit where the solution is computed via a direct additive combination of the two heads' outputs, rather than a complex, multi-hop pipeline found in GPT-2 small." (§1)

> "We argue that the circuits in large, broadly pre-trained models may be overly complex due to multi-task pressures, whereas task-constrained training can reveal more parsimonious mechanisms." (§1)

Despite the title, this is not a training-dynamics result: the Limitations section states "We do not investigate the developmental interpretability or training dynamics that lead to the emergence of these specialized circuits." Emergence here is with respect to architectural capacity.

---

### Saraipour & Zhang — "From Indirect Object Identification to Syllogisms: Exploring Binary Mechanisms in Transformer Circuits"

- **arXiv:** 2508.16109. **Venue:** not stated in the arXiv text.
- **Models:** GPT-2 small (primary); GPT-2 XL, Pythia 1.4B, Qwen3-1.7B, LLaMA3.2-1B (Appendix D).
- **Tasks:** three syllogism formats. **IOI is not run** — it appears as background and as the interpretive frame for the discovered heads.
- **Bears on:** task-specificity, replication across scale.

The IOI-relevant claim is that the same heads carry analogous roles in a different binary task:

> "Notably, mean-ablating head 10.7 improves model performance beyond the baseline. Head 10.7 has previously been characterized as a negative head in prior work (Wang et al., 2022)." (§3.1)

> "Similarly, many of the Truth Modulation Heads align with the S-Inhibition category from IOI, suggesting a shared functional role. We identify the Correct Truth Inhibition Heads as the original inhibition heads from IOI, given their role in reinforcing focus on the incorrect token." (§4)

> "This provides strong evidence that Negative Truth Heads encode the direction of the less contextualized logit in a binary setting, effectively operating in the antidirection. We believe this behavior remained unnoticed in IOI because, in that context, Mary ≠ ¬John." (§4)

The scale result is negative: Table 7 shows the simple-syllogism logit difference collapsing in larger models (GPT-2 XL 0.1112; LLaMA 3.2-1B negative), and "the heads most responsible for enabling opposite syllogism performance in the larger models are not the negative heads" (Appendix D). The authors label these findings "empirical and exploratory."

Note an internal inconsistency: the abstract says "a circuit comprising five attention heads achieves over 90% of the original model's performance," while §1 says three heads / 90% for Simple Syllogism and five heads plus four MLPs / ~85% for Opposite Syllogism.

---

### uit de Bos & Garriga-Alonso — "Adversarial Circuit Evaluation"

- **arXiv:** 2407.15166. **Venue:** not stated in the arXiv text.
- **Model:** gpt2-small. **Circuits evaluated:** the IOI circuit (Wang et al. 2022), the docstring circuit, the greater-than circuit.
- **What it did.** Sampled 1000 clean and 1000 corrupted inputs per task, formed all 1 million pairs, and measured the KL divergence between the full model's output and the circuit's output under resample ablation — then examined the tail rather than the mean.
- **Bears on:** sufficiency (worst case), confounds.

> "Our results show that the circuits for the IOI and docstring tasks fail to behave similarly to the full model even on completely benign inputs from the original task, indicating that more robust circuits are needed for safety-critical applications." (Abstract)

Table 3, KL divergence over 1,000,000 input pairs:

| Task | mean | std | min | 50% | 99.9% | max |
| --- | --- | --- | --- | --- | --- | --- |
| IOI | 5.15 | 1.70 | 0.03 | 5.12 | 10.81 | 14.64 |
| greater-than | 2.09 | 1.04 | 0.08 | 2.07 | 4.63 | 5.31 |
| docstring | 3.91 | 1.45 | 0.10 | 3.66 | 9.46 | 12.07 |

> "The table of summary statistics (Table 3) ... shows that each circuit's worst-case performance is quite far from its mean performance. For the IOI and docstring tasks, the standard deviation is quite large, the worst points we found are more than 5 standard deviations away from the mean" (§3)

The IOI failure has a content signature:

> "One striking feature of the worst-performing input pairs for the IOI task is that they often seem to involve romantic items. ... A plausible hypothesis is that parts of the model outside of the circuit are dormant in normal contexts but activate when romantic items are involved." (§3)

Two design details matter for comparability. They used the Conmy et al. data distributions, whose IOI object list has only eight values (ring, kiss, ...). And "we mixed all clean inputs with all corrupted inputs, whereas the original datasets paired them up in more restrictive ways" (§3) — the pairing is looser than Wang et al.'s.

---

### Franco, Tassis, Rohr, Crovella — "Finding Interpretable Prompt-Specific Circuits in Language Models"

- **arXiv:** 2602.13483. **Venue:** not stated in the arXiv text. Boston University.
- **Models:** GPT-2 Small, Pythia-160M, Gemma-2 2B.
- **Task:** IOI, balanced across two high-level templates (ABBA vs BABA role order) and 15 low-level templates (surface wording), plus a four-language multilingual IOI case study.
- **What it did.** Introduced ACC++, which extracts a circuit from a single forward pass by identifying the low-dimensional subspace contents ("signals") that cause attention on a token pair. Traced a circuit per prompt, represented each as a set of edge–singular-vector pairs, and clustered prompts by pairwise Jaccard distance.
- **Bears on:** rival circuits, template confounds.

> "We find that prompt-specific circuits form well-defined clusters, and across clusters, heads receive systematically different signals corresponding to distinct mechanisms for identifying the IO name." (Abstract)

> "In GPT-2 Small, the dendrogram splits cleanly into one ABBA cluster (left) and one BABA cluster (right), with no clear substructure related to low-level template. On the other hand, Pythia-160M has a larger number of smaller clusters, each aligned with low-level template groups. This shows that IOI prompt sensitivity is strong in both models, but the relevant form of variation is model-dependent: GPT-2 is strongly sensitive to role order, whereas Pythia is more sensitive to surface wording." (§3.1)

This is the same ABBA/BABA split Miller et al. found to change measured faithfulness, arriving from a different direction: Miller shows the score differs by template format, Franco et al. show the traced mechanism does.

The multilingual result is that components are shared across languages while signals are often language-specific, with cross-language circuit distances tracking linguistic relatedness (Abstract, §3.2).

---

### Bayat Makou, Niu, Dutta, Gurevych — "Many Circuits, One Mechanism: Input Variation and Evaluation Granularity in Circuit Discovery"

- **arXiv:** 2606.06267. **Venue:** not stated in the arXiv text. UKP Lab, TU Darmstadt.
- **Models:** five Pythia models, 70M–1.4B. **Task: Literal Sequence Copying across four token-frequency bands plus a control. IOI is not run** — it appears as background and in the related-work discussion.
- **What it did.** Held the task fixed and varied input token-frequency statistics, extracted 75 circuits, and tested whether the resulting structural differences correspond to functional ones via cross-band edge transfer and causal interchange interventions.
- **Bears on:** rival circuits, confounds — by analogy, since the task is not IOI.

> "we show that the resulting structural differences exhibit apparent specialization but do not correspond to functional differences, a pattern we term phantom specialization." (Abstract)

> "band-specific edges transfer broadly across bands, a core shared across most bands recovers at least 99% of circuit performance, and causal interchange interventions confirm that internal representations are interchangeable across frequency bands." (Abstract)

> "Standard evaluation practice obscures this pattern: source-level evaluation inflates apparent faithfulness, while edge-level evaluation reveals the many-to-one mapping from structure to function." (Abstract)

Their critique of Merullo et al. is directly relevant to the task-specificity question:

> "Merullo et al. (2024) showed that IOI and Colored Objects circuits share ∼78% of attention heads in GPT-2 Medium, but used source-level (head) granularity, a single extraction per task, no systematic transfer matrix, and no statistical controls." (§2.2)

And of Tigges et al.:

> "Tigges et al. (2024) tracked IOI and successor circuits across 300B tokens of Pythia training and across scales up to 2.8B, finding algorithmic stability despite component-level fluctuations; however, they vary time and scale, not input distribution, and use source-level (head) granularity without testing whether the structural variation they document is functionally irrelevant." (§2.2)

The general lesson — that structural difference is not evidence of mechanistic difference without a transfer test — has not been applied to IOI by these authors, and the frequency-band manipulation they use is precisely the name-frequency confound no one has tested on IOI.

---

### Wu, Tonin, Cevher — "Demystifying Variance in Circuit Discovery of LLMs"

- **arXiv:** 2606.16920. **Venue:** ICML 2026 Workshop on Mechanistic Interpretability (per `references.bib`; not stated in the arXiv text). EPFL LIONS.
- **Models:** GPT-2 small, GPT-2 XL, Pythia-160M, Pythia-2.8B. **Tasks:** IOI among others; logit difference is the metric for IOI.
- **What it did.** Decomposed the variance of EAP-IG circuit discovery into three kinds and proposed CEAP, a conductance-based variant with a theoretical guarantee.
- **Bears on:** rival circuits, stability.

> "This includes resampling variance, where the circuit changes when we probe with a new batch of data from the same distribution; rephrasing variance, where the discovered circuit shifts when the prompts are rephrased; and sample-wise variance, where a circuit with low population unfaithfulness exhibits large fluctuations in unfaithfulness across individual samples." (Abstract)

> "We further show that rephrasing variance arises because prompts with different templates tend to activate different circuits in the model." (Abstract)

> "Regarding sample-wise variance, we argue that it is largely benign: extremely poor unfaithfulness scores often stem from how unfaithfulness is defined, rather than from defects in the measured circuits." (Abstract)

An IOI-specific difficulty is recorded in the experimental setup:

> "The only exception is GPT-2 small on IOI, where we fix the graph size to 6000 edges (about 20% of all possible edges), which is the maximum graph size we experimented with; even at this size, the unfaithfulness remains above 0.2." (Appendix)

Per-model pairwise Jaccard curves for IOI appear as Figures 11 (GPT-2 XL), 17 (Pythia-2.8B), 23 (GPT-2 small), and 29 (Pythia-160M); the plotted values are not printed in the text.

---

## Part 3 — Comparability warnings

Different papers measure "faithfulness" differently. The numbers below are on different scales, computed under different ablations, against different reference distributions, on different models. Most cross-paper comparisons of a faithfulness number are invalid.

### 3.1 What each paper actually measures

| Paper | Model(s) for IOI | Metric | Ablation / corruption | Reference distribution |
| --- | --- | --- | --- | --- |
| Wang et al. 2211.00593 | GPT-2 small | `\|F(M)−F(C)\|` on mean logit difference; reported as % of F(M) | Mean ablation of the complement, per-template means | `p_ABC` — same templates, three unrelated random names |
| Miller et al. 2407.08734 | "GPT-2" | Logit difference recovered (%), swept over methodology | Mean **and** resample; node **and** edge; all positions **and** circuit positions | `p_ABC`, with 100 prompts (Wang used ~7 per template) |
| Hanna et al. 2403.17806 | GPT-2 small | Normalized faithfulness `(m − b′)/(b − b′)` ∈ [0,1] | Resample of all non-circuit **edges** from a corrupted input | Paired corrupted prompt; loss also varied (task metric vs KL) |
| Conmy et al. 2304.14997 | GPT-2 small | `D_KL(G‖H)`; separately AUC vs the canonical circuit | Interchange intervention; zero ablation reported as an alternative | Wang et al.'s ABC dataset, N = 50 from one template |
| Syed et al. 2310.10348 | GPT-2 small | ROC AUC vs the canonical circuit | Interchange (linear approximation) | Task-specific metric, not KL |
| Shi et al. 2410.13032 | GPT-2 small | `F_τ(M,C) = E[\|s(M(x),y) − s(C(x),y)\|²]`; lower is better | Symmetric token replacement **and** zero ablation | Random-walk subgraphs as the null |
| Mueller et al. 2504.13151 | GPT-2, Qwen, Gemma, Llama | CPR and CMD — integrals of `(m(C) − m(∅))/(m(N) − m(∅))` over circuit size | Counterfactual (reported), plus mean and optimal (compared) | Empty circuit ∅ as denominator; fixed counterfactual pairs |
| Li & Janson 2409.09951 | GPT-2 small | Δ = expected loss increase; Δ_opt as the lower bound | Zero, mean, resample, counterfactual, CF-mean, **optimal** | Learned constant `a*` for optimal ablation |
| Bhaskar et al. 2406.16778 | GPT-2 small | KL to the full model, at matched sparsity | Interchange ablation (zero only for Tracr) | Per-template placeholder swap |
| Tigges et al. 2407.10827 | Pythia only | ≥80% of whole-model logit difference | Corrupted-input patching of everything outside the circuit | Counterfactual input |
| Li & Subramani 2605.08348 | Gemma, Llama, Qwen, OLMo | Top-1 accuracy under argmax decoding | **Zero ablation** | Capacity-matched random circuit as the control |
| Chen et al. 2605.12671 | GPT-2 small, Pythia-160M | Task accuracy of the isolated subgraph, plus complement accuracy | **Zero ablation**, standalone execution | Chance ≈ 50% for the binary contrast |
| Méloux et al. 2510.00845 | gpt2-small, Llama-3.2-1B | Circuit error (fraction of flipped predictions), KL, pairwise Jaccard | Corrupted patching, mean, mean-positional, zero (all swept) | Bootstrap / meta-dataset / paraphrase resamples |
| Nainani et al. 2411.16105 | GPT-2 small | Circuit logit difference ÷ model logit difference | Mean ablation, following Wang et al. | Wang et al.'s knockout procedure |
| O'Neill & Bui 2405.12522 | GPT-2 small | Logit difference; separately ROC AUC vs the canonical circuit | Name-swap counterfactual ("corrupted") activations | Corrupted cache with the subject's name swapped |
| uit de Bos & Garriga-Alonso 2407.15166 | gpt2-small | KL divergence, reported as a full distribution over 10⁶ input pairs | Resample ablation of everything outside the circuit | Conmy et al.'s IOI distribution, with clean and corrupted inputs fully crossed rather than paired |
| Franco et al. 2602.13483 | GPT-2 Small, Pythia-160M, Gemma-2 2B | Pairwise Jaccard distance between per-prompt circuits (edge–singular-vector pairs) | None — single forward pass, no patching or ablation | Other prompts of the same task |
| Wu et al. 2606.16920 | GPT-2 small/XL, Pythia-160M/2.8B | Unfaithfulness; pairwise Jaccard vs edge count | EAP-IG / CEAP scoring with counterfactual patching | Resampled batches, rephrased prompts, individual samples |

### 3.2 Comparisons that are invalid

- **Wang's 87% against Hanna's 0.6 or 0.8.** Wang reports logit difference recovered as a percentage under mean node ablation of the complement; Hanna reports normalized faithfulness in [0,1] under resample ablation of all non-circuit *edges*, for a different circuit found by a different method. Different scale, different ablation target, different circuit.
- **Wang's 87% against Miller's numbers.** They are the same quantity in name only. Miller changed the ABC dataset size (100 prompts vs ~7 per template), the averaging order (mean of ratios vs ratio of means), and the ablation granularity. Miller's own point is that the number is not well defined without the full methodology.
- **Any AUC comparison across ablation types.** ACDC's IOI edge AUC is 0.869 with corrupted activations and 0.539 with zero ablation (Conmy Tables 2, 3). O'Neill & Bui report the same instability (0.777 vs 0.424 node-level). AUCs from different papers are comparable only if the ablation matches.
- **Any AUC comparison against the Wang circuit as ground truth.** Conmy et al. state the problem themselves: "the ground-truth circuits are reported by practitioners and are likely to have included extraneous edges and miss more important edges ... our 'ground-truth' is not 100% reliable." Miller et al. add that ground truth discovered under one ablation methodology cannot fairly score methods that use another.
- **Merullo's GPT-2 Medium head IDs against anyone's GPT-2 small head IDs.** Merullo's mover heads sit at layers 14–19 of a 24-layer model; ACDC's sit at layers 9–11 of a 12-layer model. Merullo also reports a substantive behavioral difference in the negative mover head between the two sizes.
- **Li & Subramani's IOI necessity numbers against GPT-2 small necessity claims.** Their models are Gemma, Llama, Qwen, and OLMo; their ablation is zero ablation; their metric is top-1 accuracy. Their near-zero IOI effect is not evidence about GPT-2 small.
- **Chen et al.'s 4.1% edge IoU against any node-level overlap claim.** Node IoU on IOI in the same paper is 64.2% (Appendix D).
- **The SAE circuit's 3.62 as evidence of beating the Wang circuit.** Same paper's Table 4 gives the Wang circuit 4.11 with 26 heads against their 3.62 with 40.
- **Tigges' cross-scale consistency as evidence about GPT-2.** No GPT-2 model is run in that paper. The copy-suppression heads have the opposite sign in Pythia.
- **Méloux et al. 2502.20914 as evidence about IOI.** No transformer and no IOI experiment appears in that paper.
- **McGrath et al.'s Hydra numbers as evidence about GPT-2 small IOI.** That paper runs Chinchilla 7B on Counterfact with layer-level ablations. The GPT-2-small IOI self-repair numbers come from McDougall et al. (39% of repair from two negative heads) and Gong et al. (0.22 of 2.53 masked attribution, 1.9× super-additivity).
- **uit de Bos & Garriga-Alonso's mean KL of 5.15 against Wang's 87%.** Different quantity entirely: a distribution of KL divergences under resample ablation with fully crossed clean/corrupted pairs, versus a ratio of mean logit differences under mean ablation with Wang's own pairing. Their looser pairing is itself a design difference that the paper flags.
- **Bayat Makou et al.'s phantom-specialization result as an IOI result.** That paper runs Literal Sequence Copying on Pythia. Its bearing on IOI is methodological — that structural difference requires a transfer test before it counts as mechanistic difference — not empirical.

### 3.3 Comparisons that are valid

- Within Miller et al., across their swept methodologies — this is a controlled comparison by design.
- Within Li & Janson, across ablation types on the same circuits and model.
- Within MIB / the BlackboxNLP shared task, across methods — fixed splits, fixed counterfactuals, one metric definition.
- Within Conmy et al., across ACDC / SP / HISP — the baselines were adapted to use the same metric and the same corrupted activations.
- Within Chen et al., across their 20 sheaves.
- Within Méloux et al. 2510.00845, across resampling regimes on the same model and task.

### 3.4 Two vocabulary traps

- **"Path patching" is not one thing.** Miller et al. establish that Wang et al.'s path patching "is equivalent to Edge Resample Ablation in our terminology" (Appendix F). Goldowsky-Dill et al. generalized the operation to arbitrary path sets in a treeified graph. Papers using the term may mean either.
- **"Faithfulness" is not one thing.** Wang et al.: circuit performance matches the model's. Hanna et al.: behavior survives corrupting everything outside the circuit. Conmy et al.: KL between circuit and model output distributions. Shi et al.: squared score difference. Chen et al.: standalone task accuracy under zero ablation. Nainani et al.: a ratio that can exceed 1 and does. The word does not license comparison.

---

## Part 4 — Open questions

Two categories, kept separate. "Searched, no published test located" means targeted searches were run and nothing was found; it is a claim about the search, not a claim that the work does not exist. "Not searched" means the topic was outside the searches run for this document.

### 4.1 Searched, no published test located

**A double dissociation involving the IOI circuit.** The design — ablate the IOI circuit, show IOI falls while task B is spared; ablate task B's circuit, show the reverse — has not been run on IOI. The nearest published work (Li & Subramani 2605.08348) runs the full cross-task ablation matrix on other models and finds no dissociation at all. Searches: "double dissociation" combined with mechanistic interpretability, circuits, IOI, and selectivity terms.

**Name-token frequency as a confound on the IOI circuit.** Wang et al. sample names from a fixed list; no paper appears to have stratified IOI by name frequency in the training corpus and asked whether the circuit or its measured faithfulness changes. Bayat Makou et al. 2606.06267 run exactly this manipulation, on Literal Sequence Copying in Pythia, and find that frequency-band-specific circuits are functionally interchangeable — but they do not run IOI. Searches: IOI combined with token frequency, name frequency, and frequency confound terms.

**Sequence length as a confound.** No length-stratified evaluation of the IOI circuit located. Adhikari 2510.25013 names it as future work. The variants that do exist (Nainani et al.'s DoubleIO and TripleIO) change the number of name occurrences rather than sentence length.

**The IOI circuit across training seeds of the same architecture.** No test located. GPT-2 was released as one run with no intermediate checkpoints, and no paper appears to have trained multiple GPT-2-small-scale models and compared their IOI circuits. Tigges et al. use Pythia, which ships one seed per size. Bhaskar et al.'s 12 seeds vary the discovery algorithm, not the trained model. Naser Moghadasi & Ghaderi's five seeds vary dataset generation.

**Circuit co-emergence with IOI behavior in GPT-2 specifically.** Tigges et al. answer this for Pythia and Li & Subramani for OLMo-2. GPT-2 lacks public pretraining checkpoints, which leaves the question unanswerable for the model the canonical circuit was found in.

**A completeness test on the IOI circuit run to Wang et al.'s own standard by anyone else.** Wang et al. report failing their own greedy completeness search (incompleteness score up to 3.09, 87% of the original logit difference). Tigges et al. explicitly decline to run it: the method "is seldom used due to its complexity and computational cost" (§2.2). Mueller et al. state that completeness "cannot be tractably computed without access to the ground-truth set of causally relevant components" (Appendix B) and substitute a purpose-trained model with a known circuit. Gong et al. 2607.01940 report a completeness gap of 0.72 for the first-order circuit closing to 0.15 once backups are added, which is the closest published follow-up.

**An IOI faithfulness evaluation that reports per-example distributions rather than averages, outside Miller et al.** Miller et al. report the inter-quartile range reaching 50% and outliers in the tens of thousands of percent (§4.2), and uit de Bos & Garriga-Alonso report the KL tail (§3). No other paper located reports the spread.

### 4.2 Not searched

The following were outside the scope of the searches run and should not be treated as absent from the literature:

- Non-English IOI beyond the four-language case study in Franco et al. 2602.13483.
- IOI in encoder or encoder-decoder architectures.
- IOI under quantization, distillation, or other compression.
- IOI circuits in instruction-tuned or RLHF'd descendants of the models studied.
- Human or psycholinguistic work on indirect object resolution, which might supply an external criterion for what the model ought to be computing.
- Formal-verification or proof-carrying approaches to the IOI circuit beyond Palumbo et al. 2407.13594.
- The blog-post and LessWrong literature, which contains additional IOI results that were not indexed here because they could not be cited with stable section references.

### 4.3 Contradictions left standing

These are recorded rather than resolved.

- **Minimality.** Shi et al. 2410.13032: the IOI circuit is not minimal, ~20% of edges removable. Li & Janson 2409.09951: under optimal ablation the manual circuit is approximately optimal for its size, and the apparent slack under other ablation methods is a spoofing artifact. Both are correct within their own ablation regime.
- **Task-specificity.** Merullo et al. 2310.08744: 78% head overlap between IOI and Colored Objects in GPT-2 Medium. Hanna et al. 2403.17806: cross-task faithfulness for IOI is near zero in GPT-2 small, and overlap does not predict faithfulness. Bayat Makou et al. 2606.06267 add that head-level overlap without a transfer matrix is weak evidence either way.
- **Whether self-repair invalidates circuit discovery.** Rushing & Nanda 2402.15390: mostly not, because importance is heavy-tailed — with an explicit caveat for narrow distributions. Gong et al. 2607.01940: yes for IOI specifically, where first-order methods leave a completeness gap of 0.72.
- **Whether the MLP8 subspace result on IOI is an illusion.** Makelov et al. 2311.17030 say yes and propose a nullspace diagnostic. Wu et al. 2401.12631 accept the empirical finding, reject the diagnostic, and reject the framing. Both report ~4% interchange accuracy for MLP8 and ~70% for the residual stream.
- **The origin of backup behavior.** Wang et al. 2211.00593 hypothesize dropout during training. McGrath et al. 2307.15771 report the same effect in Chinchilla 7B, "trained without any form of dropout or stochastic depth."
- **What the negative name mover heads do across model sizes.** Wang et al.: in GPT-2 small they attend to all names and hedge. Merullo et al.: in GPT-2 Medium the head "attends only to the S2 token and demotes its likelihood." Tigges et al.: in Pythia the copy-suppression heads contribute *positively*, by downweighting the incorrect name.
