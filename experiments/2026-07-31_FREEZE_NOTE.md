# IOI Preregistrations

**Freeze commit:** `a1385af9fd0279dcd84c0f4dea617a1f13d0d416`

**None of the five studies below has been run.** No model was loaded, no corpus was
counted, no activation was cached, no fine-tuning was performed, and no result was
computed while these documents were written. Each contains a committed quantitative
prediction and the outcome that would falsify it. That is the point of the freeze commit:
it fixes the moment before any data was touched, so a reader can check whether the
predictions were written first.

Artifact availability was verified from published documentation and from the pinned
TransformerLens source. Reading a model card is not running an experiment, and the
distinction is maintained throughout: no model was executed.

All five target GPT-2 Small and the indirect object identification circuit of Wang et al.,
"Interpretability in the Wild" (arXiv:2211.00593). Each was selected because
`docs/IOI_LITERATURE.md` records no published test of it.

---

## The five

| File | Criterion | Question | Headline prediction |
|---|---|---|---|
| [`double_dissociation_ioi_vs_greater_than.md`](double_dissociation_ioi_vs_greater_than.md) | I6 | Does ablating the IOI circuit break IOI while sparing Greater-Than, and does the Greater-Than circuit show the mirror image? | The four-cell interaction contrast reaches ≥ 0.80, so the dissociation holds — and both cross-task cells still exceed their layer-matched random controls by more than 0.10, so it is impure. |
| [`name_frequency_and_sequence_length_confounds.md`](name_frequency_and_sequence_length_confounds.md) | I7 | Does the IOI effect survive controls for how frequent the name tokens are and how long the sequence is? | Frequency confounds the behavior and spares the mechanism: a ≥ 0.5 nat swing from the frequency contrast, accuracy holding above 70% in the adversarial cell, and cross-band circuit transfer retaining ≥ 90% of within-band faithfulness. |
| [`circuit_replication_across_training_seeds.md`](circuit_replication_across_training_seeds.md) | E4 | Is the circuit a property of the architecture and data, or of one training run? | Roles replicate and coordinates do not: mean cross-seed top-26 Jaccard ≥ 0.45 against a chance value of 0.099, sitting at least 0.10 below the within-seed bootstrap ceiling, with ≤ 30% of head coordinates shared by all five seeds. |
| [`head_level_minimality_retest.md`](head_level_minimality_retest.md) | I3 | Re-measured under Wang et al.'s own §4.2 minimality score, do all 26 heads still earn their place? | The original result replicates because the procedure is generous: ≥ 8 of 26 heads fail under single-head ablation, ≥ 23 of 26 clear under Wang et al.'s own subset rule, and all 26 clear under a greedy subset. |
| [`onset_offset_coupling.md`](onset_offset_coupling.md) | **I11** | Does the circuit's measured strength rise as the capability is acquired in training, fall as it is fine-tuned away, and return when the capability returns? | Both directions couple: within-seed Spearman ≥ 0.90 between behavior and name-mover strength across training in all five seeds, and ≥ 0.85 between capability and circuit strength across a 40-rung destruction-and-recovery dose ladder, with matched random sets falling at most half as far. |

Criterion labels follow `docs/paper/mechanistic_validity_v10.tex`. The mapping for the
first four is indicative; the fifth is the one the coordinator specified, and it is exact.

---

## Note on criterion I11

`onset_offset_coupling.md` tests **criterion I11, onset–offset coupling**, as defined at
`mechanistic_validity_v10.tex` line 406 and measured by metric A14 (line 869), adapted
from guideline 3 of the molecular Koch's postulates.

**There is an identifier collision in this repository that should be resolved.** The paper
assigns I11 to onset–offset coupling. The documentation site assigns I11 to a different
criterion: `docs/src/content/docs/framework/criteria/internal/directed-information-flow.md`
declares `criterion_id: "I11"` for **Directed Information Flow**, and the information-theory
lens pages repeat that mapping. Two criteria currently carry one identifier. The
preregistration uses the paper's definition, since that is what the criterion's stated
grounding in Fredricks and Relman describes, and it flags the collision rather than
resolving it unilaterally.

---

## Runnability with currently available artifacts

Four of the five are runnable now on one GPU in under a day each. Two turned on artifact
questions that were checked directly rather than assumed.

**The seed study is runnable.** GPT-2 Small has one public checkpoint, which rules out the
obvious approach and does not rule out the experiment. Stanford CRFM (Mistral) released
five separately seeded GPT-2 Small runs on OpenWebText — seeds 21, 49, 81, 343, 777 — all
five present in the pinned TransformerLens `supported_models.py`. Comparisons among the
five vary seed alone; comparisons against OpenAI GPT-2 Small vary seed, corpus, and recipe
together, and are reported separately and labelled confounded.

**The onset–offset study is runnable in both directions, and this corrects the paper.**
The disappearance half needs no pretraining checkpoints and runs on OpenAI GPT-2 Small
directly. The emergence half needs checkpoints, and they exist at GPT-2 Small scale: each
Stanford CRFM run carries **600 intermediate checkpoints** — every 10 steps to 100, every
50 to 2,000, every 100 to 20,000, every 1,000 to 400,000 — loadable through TransformerLens
by `checkpoint_value`. Pythia supplies 154 checkpoints per model across eight sizes from
70M, and OLMo-2 supplies stage-1 checkpoints from 1B.

`mechanistic_validity_v10.tex` line 1178 currently scores I11 as untestable on this claim
because "GPT-2 Small releases no pretraining checkpoints, so circuit emergence cannot be
dated." That is right about OpenAI's release and overreaches twice: it treats the criterion
as exhausted by its emergence half when the disappearance half needs no checkpoints, and
it generalizes from one release to the architecture when five checkpointed seeded GPT-2
Small runs are public. **That sentence should be corrected whether or not the study's
predictions hold.**

The scope cost is stated up front in the document and is not negotiable: an emergence
result on Stanford CRFM GPT-2 Small is a result about a GPT-2 Small architecture trained
on OpenWebText, not about Wang et al.'s 26 heads in OpenAI GPT-2 Small. A result on
Pythia-160M would be further still — a different architecture, tokenizer, and corpus, and
largely a replication of Tigges et al.

---

## Conventions shared by all five

**The ablation method is specified explicitly in every document.** `IOI_LITERATURE.md`
§1.9 records seven independent groups finding that the ablation choice moves the
conclusion, including sign flips. Each study names its primary ablation and its reference
distribution, and pre-registers a secondary protocol reported in full alongside rather
than in place of the primary.

**No cross-paper number comparisons.** §3.1–3.2 of the literature file documents that
"faithfulness" names at least six different quantities measured under different ablations
against different reference distributions on different models, and lists which comparisons
are invalid. Every quantity defined here lives inside one protocol.

**Every study has gates that run first and are reported whatever they return.** A circuit
whose own task does not depend on it, a model that cannot do the task, a frequency proxy
that fails to correlate with itself, and a training transition that falls between two
checkpoints are all live possibilities. Each is a finding rather than a reason to stop
reporting.

**Multiple comparisons are corrected within pre-declared families, and the number of
families is fixed in each document before any run.**

---

## Document hashes at freeze

SHA-256 of each file as committed, so a later edit is detectable:

| File | SHA-256 |
|---|---|
| `double_dissociation_ioi_vs_greater_than.md` | `68581dc0c01df559ac63c0bee621d6853fcd17a50e02d5fe15149e607116db87` |
| `name_frequency_and_sequence_length_confounds.md` | `5b21803b8acbbedc08ff68865e29a7f3d4501e2fdbee9d598cc627101b74b9b7` |
| `circuit_replication_across_training_seeds.md` | `961be4e98b9d62afc3e5929172e8f4a169a7796967bcc3023844f311efb7394f` |
| `head_level_minimality_retest.md` | `404755aed3f663d4c736b556c062d437e0d0c91aeaa8ceff841c716305f68602` |
| `onset_offset_coupling.md` | `e4b8e9caab6a9a416b7d9abb55648e66003b7c54e8b1130afcdd972f4635d0a1` |

Recompute with `shasum -a 256 *.md` from this directory. This README is excluded from its
own table.

**One post-freeze edit is on record.** `circuit_replication_across_training_seeds.md`
originally hashed to
`b6274897dd60736839d77ee53d2b26ae2c713f7598a4dd4ff204218c7a57e34b`. A block was added
recording the artifact facts verified while preparing `onset_offset_coupling.md` — the
five repository names, their seeds, the OpenWebText corpus, and TransformerLens support.
The block is marked as post-freeze in the document itself, and **no prediction, threshold,
gate, or analysis choice was changed.** The original hash is retained here so the edit is
auditable rather than silent.
