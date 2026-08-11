# Prior-art check on the nine pre-registered experiments

Run 2026-08-10, one adversarial agent per question, each instructed to find the scoop rather
than confirm novelty. Every citation below was checked by downloading the PDF and grepping the
extracted text; abstract snippets and WebFetch summaries were not accepted as evidence.
Downloaded sources are in `reference/scooping-check/`.

## Verdicts

| Experiment | Verdict | Prior work that matters |
|---|---|---|
| M7 selection correction | **Novel** | No re-estimate of the 80% copy-suppression figure off its selected slice; no CSPA threshold sweep |
| I7 name frequency | **Novel** | Two metadata sweeps return zero papers crossing IOI with token frequency |
| I7 sequence length | Partially scooped | Wang §4.4 itself, Anani 2602.22968, Rai 2605.09129 all vary IOI length |
| E4 cross-seed | Partially scooped | Xu 2605.24059 (six seeds, TinyStories 51M); Bali 2602.16740; Gurnee 2401.12181 |
| I3 minimality | Partially scooped | Arcuschin et al. 2024 own the argument; nobody has measured it |
| I6 double dissociation | Partially scooped | Li & Subramani 2605.08348, opposite result on other models |
| E1 intervention reach | Partially scooped | Miller 2407.08734 Figure 3 already isolates the ablation-value axis |
| I10 rescue reversibility | Partially scooped | Standard interchange intervention; Hydra effect threatens interpretability |
| I4 specificity | **Scooped** | Li & Subramani ran the identical formalization and answered it |
| I11 onset-offset | pending | agent re-running after an API stall |

## Errors found in frozen pre-registrations

These are defects in the registered documents, so they are recorded here rather than silently
edited. Each needs an amendment entry naming it before the corresponding experiment is run.

**E4 — a quotation that does not exist in its source.** The document attributes to Méloux et al.
2510.00845 the sentence *"variation is over data resamples and hyperparameters, not over training
seeds."* The string "seed" occurs zero times in that paper. The claim is true in substance; the
quotation marks are not. This is the failure mode the audit quote-gate exists to catch, and
pre-registrations are not covered by that gate.

**E4 — the 0.071 overlap is the wrong model.** The document, and `run.py`'s docstring, say two
edge-attribution variants "on GPT-2 small IOI overlap at 0.071." In the source that number sits
under Table 2, captioned *"Hyperparameter sensitivity in Llama-3.2-1B-Instruct."* The sentence
reads *"In IOI, the overlap between EAP-IG-inputs and Clean-corrupted is also negligible
(0.071)"* — inside the Llama section. Load-bearing: it is the stated justification for using a
single extractor.

**Two different Méloux papers are being conflated.** `reference/meloux_2025_identifiable.pdf` is
arXiv 2502.20914, *Everything, Everywhere, All at Once: Is Mechanistic Interpretability
Identifiable?*. The numbers the pre-registrations use come from arXiv 2510.00845, a different
paper by an overlapping author set. The 0.67 bootstrap Jaccard and the 0.8 stability bar are
genuine and in 2510.00845 — verified verbatim, *"a mean pairwise Jaccard index above 0.8 under
bootstrap resampling (with n ≥ 100 resamples) could serve as a reasonable minimum bar"* — but
they are absent from the PDF the repository actually stores.

**I3 — the reason RW was not implemented is false.** `run.py` records as a finding that Wang et
al. "print no rule for choosing K." Wang §4.2 states the rule and Appendix K, titled *Minimality
sets*, prints `K ∪ {v}` for all 26 nodes in Figure 20. RW is implementable by transcription, and
it is neither R0, RC, nor RG: nested for the name movers, cross-class for induction heads 5.8 and
5.9, and class-wide elsewhere. `run.py` also misattributes Figure 6, which is the *completeness*
figure.

**I7 — "no published test located" is wrong for the length arm.** Wang §4.4 runs a length control:
*"To ensure that the observed effect is not an artifact of the additional sentences, we included a
control dataset using the same templates, but where the middle sentence contains S instead of
IO."* The frequency arm's claim survives: `frequen` occurs zero times in Wang et al.

**E1 — the novelty claim overstates.** The document says the experiment "answers a question their
design does not separate." Miller et al.'s Figure 3 does separate it, with a t-test at p = 1e-5.
The honest framing is an extension from two ablation values to four.

**E1 — "26 (head, position) pairs" misreads Wang.** The original is *"a circuit of 26 attention
heads -- 1.1% of the total number of (head, token position) pairs"*. 26 is a head count.

**Six pre-registrations cite `docs/IOI_LITERATURE.md`, which does not exist**, alongside
`preregistrations/README.md`, which also does not exist. The provenance chain points at nothing.

## Every implementation diverges from its registered design

Checked independently by the agents, and confirmed:

- **I3** — resample ablation from a Pile pool where the document commits to mean ablation over
  the ABC distribution. The ABC data is loaded and discarded. Under a different ablation the
  θ = 1% × F(M) bar is not commensurable with Wang's number.
- **I6** — zero/resample/native and a permutation test, against a registered design of mean
  ablation, normalized D, 200 size- and layer-matched random controls, and a bootstrap CI.
- **E1** — the missing arm is mean-over-ABC against resample-from-ABC, which is exactly the
  contrast Miller et al. ran.
- **I4** — registered controls replaced with MIB tasks, two of them scored with the IOI metric.
- **M7** — only the first half is implemented; the threshold sweep has no code.

## Two live threats to the study as a whole

**GPT-2 small's IOI baseline is contested.** Xu 2606.05378 reports *"top-1 13%, IO-vs-subject
57%"*, against Wang's 99.3% over 100,000 examples. A single-author preprint contradicting the
origin directly, most likely a generator difference — but I6's Gate A needs ≥95%, and several
predictions assume a near-ceiling baseline. Worth resolving before spending run time.

**Nanda's open problem 2.17 proposes E4 verbatim** and has stood open since December 2022:
*"Understand IOI in the Stanford mistral models -- these are GPT-2 Small replications trained on
5 different random seeds, does the same circuit arise?"* Four years without an answer is the
strongest available argument that the experiment is worth running, and it should be cited as
such rather than left out.

## Prior art that must be cited rather than claimed

- **I3** — Arcuschin, uit de Bos & Garriga-Alonso (2024) already argue the existential quantifier
  makes minimality choice-dependent: *"a non-minimal circuit can become minimal when you increase
  the granularity!"* Toy examples only, no measurement. Chhabra et al. 2503.01896 compute Wang's
  minimality score on IOI in fine-tuned GPT-2 without ever stating their K.
- **I6** — Hanna, Belinkov & Pezzelle 2503.11302 imports the neuroscience dissociation framing and
  reports a bidirectional result. Same author cluster as the greater-than paper already cited.
- **E4** — Gurnee et al. 2401.12181 use the same five Stanford models for the same question one
  level down, finding 1-5% of neurons universal. Xu 2605.24059 already runs the cross-seed
  ablation-transfer matrix at toy scale.
- **I4** — Merullo 2310.08744 reports that for our exact pair, *"preliminary work on other tasks
  ... (e.g., predicting numbers greater than some given integer) had virtually no overlap with the
  IOI circuit"*, which points opposite to Li & Subramani. Both are citable now.
