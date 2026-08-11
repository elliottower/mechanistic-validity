# Claimed errors in the frozen pre-registrations — verification packet

Nine claims below. Each says what our document asserts, what the source appears to say, and who
checked it. **Provenance is marked on every item**, because roughly half were verified by me
directly against a downloaded PDF and half come from sub-agents I have not independently
re-checked. Treat the two differently.

Nothing here has been edited into the frozen documents. Errors in a pre-registration get
recorded, not silently corrected — correcting one quietly would defeat the freeze.

The documents themselves:

| Pre-registration | Path |
|---|---|
| E4 cross-seed | `experiments/E4_replication_across_seeds/PREREG.md` |
| I3 minimality | `experiments/I3_head_level_minimality/PREREG.md` |
| I6 double dissociation | `experiments/I6_double_dissociation/PREREG.md` |
| I7 confounds | `experiments/I7_frequency_and_length_confounds/PREREG.md` |
| I11 onset/offset | `experiments/I11_onset_offset_coupling/PREREG.md` |
| E1 / I4 / I10 / M7 | `experiments/E1_intervention_reach/PREREG.md` (shared across the four folders) |

---

## 1. E4 quotes a sentence that is not in its source — VERIFIED BY ME

**Our document says**, in the Prior work section, attributing to Méloux et al. 2510.00845:

> "variation is over data resamples and hyperparameters, not over training seeds"

**The problem.** The string `seed` occurs **zero times** in arXiv:2510.00845. I ran
`grep -ci seed` on the extracted text and got 0.

**To check:** open arXiv:2510.00845 and search for "seed". The substance of our sentence is
correct — that paper does vary resamples and hyperparameters and not seeds — but it is written
as a direct quotation and no such sentence exists.

**Severity: high.** This is a fabricated quotation inside a frozen document. It is the exact
failure the audit quote-gate was built to catch, and pre-registrations are not covered by that
gate.

---

## 2. E4 attributes the 0.071 overlap to the wrong model — VERIFIED BY ME

**Our document says:**

> "Méloux et al. report that two edge-attribution variants on GPT-2 small IOI overlap at 0.071"

The same sentence is repeated in `E4_replication_across_seeds/run.py`'s docstring.

**The source says** (2510.00845, near line 544 of the extracted text):

> "Table 2 confirms this for LlamaInstruct. … In IOI, the overlap between EAP-IG-inputs and
> Clean-corrupted is also negligible (0.071)."

Table 2's caption reads: **"Hyperparameter sensitivity in Llama-3.2-1B-Instruct."**

**To check:** find Table 2 in 2510.00845 and read its caption, then find the 0.071 figure and
confirm which model's section it sits in.

**Severity: high.** This number is the stated justification for using a single extractor across
all five seeds. If it is a Llama result, it does not directly support a GPT-2 design choice.

---

## 3. Our stored Méloux PDF is a different paper from the one we cite — VERIFIED BY ME

`reference/meloux_2025_identifiable.pdf` is arXiv **2502.20914**, *"Everything, Everywhere, All
at Once: Is Mechanistic Interpretability Identifiable?"* (Méloux, Portet, Maniu, Peyrard, ICLR
2025).

Every pre-registration cites arXiv **2510.00845**, a different paper with an overlapping author
set. Two of our three numbers (0.67 and the 0.8 bar) are genuinely in 2510.00845 — I confirmed
the 0.8 verbatim: *"a mean pairwise Jaccard index above 0.8 under bootstrap resampling (with
n ≥ 100 resamples) could serve as a reasonable minimum bar for reporting a circuit as stable."*
Note it is introduced as "As a preliminary guideline", and our S3 repurposes it as a cross-seed
threshold, which is a different use.

**To check:** confirm 2502.20914 and 2510.00845 are distinct papers, and that the 0.67 and 0.8
figures belong to the latter.

**Note:** two sub-agents disagreed here. One reported the numbers were unlocatable; it was
grepping our stored PDF, which is the wrong paper. That is worth knowing as a caution about the
other agent-sourced items below.

---

## 4. I3 records a false claim about Wang et al. as a finding — VERIFIED BY ME

**Our `run.py` says**, presenting it as a result rather than an omission:

> "Wang et al. define minimality existentially and print no rule for choosing K. … There is no
> separate printed rule to replicate."

**Wang et al. §4.2 says:**

> "We need to exhibit for every v a set K such that the minimality score is high. For most
> heads, removing the class of heads G that v is a part of provides a reasonable minimality
> score, but in some instances a more careful choice is needed; we provide full details in
> Appendix K and display final results in Figure 7."

Appendix K is titled **"Minimality sets"** — *"The sets that were found for the minimality tests
are listed in Figure 20"* — and Figure 20 prints `K ∪ {v}` for all 26 nodes.

**To check:** open arXiv:2211.00593, go to Appendix K, and confirm Figure 20 lists a K set per
node.

**Severity: high.** We would have shipped a false claim about a paper as a contribution.

---

## 5. I3 misattributes Wang's Figure 6 — VERIFIED BY ME

Our `run.py` treats Figure 6's sampling strategies as the minimality protocol and concludes they
are identical to our three regimes. Figure 6 belongs to the **completeness** criterion, which
Wang introduces separately, and the greedy procedure is Algorithm 3 in Appendix M, described as
*"the procedure used to sample sets for checking the completeness criteria using greedy
optimization."*

**To check:** confirm Figure 6 and Algorithm 3 are about completeness, not minimality.

**Consequence:** Wang's actual K choice is neither of our three regimes. It is nested for the
name movers, cross-class for induction heads 5.8 and 5.9 (K = the negative heads), and
class-wide elsewhere.

---

## 6. I11 is not blocked, and the paper says it is — VERIFIED BY ME

The paper scores I11 as *"Untestable in GPT-2 small, which ships no pretraining checkpoints."*

Querying the HuggingFace refs API for `stanford-crfm/darkmatter-gpt2-small-x343` returns
**609 tags and 1 branch**, tags named `checkpoint-99000`, `checkpoint-9900`, and so on.

The claim is defensible about OpenAI's `gpt2` release and misleading about the architecture,
since five seeded GPT-2 small replications ship full trajectories. Our own frozen registry
already said so and asked for the sentence to be corrected either way.

**To check:** `https://huggingface.co/api/models/stanford-crfm/darkmatter-gpt2-small-x343/refs`

---

## 7. I7 claims no published length test exists — AGENT-SOURCED, NOT RE-CHECKED BY ME

**Our document says** the literature file records "No published test located" for sequence
length.

**The agent reports** that Wang et al. §4.4 runs one:

> "To ensure that the observed effect is not an artifact of the additional sentences, we
> included a control dataset using the same templates, but where the middle sentence contains S
> instead of IO."

and that Anani et al. 2602.22968 and Rai et al. 2605.09129 also vary IOI prompt length.

**To check:** all three. The frequency arm's claim is separately reported as surviving —
`frequen` occurs zero times in Wang et al. — so please check that too, since it is the half we
would keep.

---

## 8. E1 overstates its novelty — AGENT-SOURCED, NOT RE-CHECKED BY ME

**Our document says** the experiment "answers a question their design does not separate: how
much of the spread is the ablation value alone," referring to Miller et al. 2407.08734.

**The agent reports** Miller et al.'s Figure 3 already separates it:

> "Figure 3 also evaluates the effect of ablation value. We rerun the above experiment using
> Resample Ablations from the ABC distribution, and find that this results in a systematically
> lower faithfulness as compared with mean ablations (statically significant on a t-test with
> p = 1e − 5 for Node Ablation but not Edge Ablation)."

**To check:** whether Figure 3 holds the other dimensions fixed while varying ablation value. If
it does, our honest framing is "extends their two-value comparison to four," not "separates an
axis they conflate."

---

## 9. E1 misreads Wang's "26" — AGENT-SOURCED, NOT RE-CHECKED BY ME

**Our document says** "26 (head, position) pairs", twice.

**Wang et al. reportedly say:** *"We discover a circuit of 26 attention heads–1.1% of the total
number of (head, token position) pairs"* — so 26 counts heads, and the (head, position) space is
what 26 is 1.1% *of*.

**To check:** the sentence in arXiv:2211.00593.

---

## Also worth an independent look

**A contested baseline that gates everything.** Xu, arXiv:2606.05378, reportedly reports GPT-2
small at *"top-1 13%, IO-vs-subject 57%"* on IOI, against Wang's 99.3% over 100,000 examples.
Single-author preprint contradicting the origin directly, most likely a difference in how the
prompts are generated. It matters because I6's gate requires ≥95% and several predictions assume
a near-ceiling baseline. **Agent-sourced, not re-checked by me.**

**A decoy pattern that has now bitten five times.** Same surname, similar year, different paper.
Confirmed instances: Bal versus Bali; `chughtai2024_summing_up_the_facts.pdf` is
Chughtai–Cooney–Nanda on factual recall while our text cites Chughtai–Chan–Nanda 2023 on group
operations; `singh2024_needs_to_go_right...` is about induction heads while our text cites Singh
et al. 2025 on OthelloGPT; `mcgrath_2023_hydra_effect.pdf` is the Hydra Effect while our text
cites McGrath et al. 2021 on AlphaZero; and the two Méloux papers in item 3. When checking any
citation here, confirm title *and* author list *and* identifier together.
