# Experiments

One folder per experiment, self-contained. Each holds the pre-registration that specifies it,
the code that runs it, the tests for that code, and the results it produced — so a reader can
check any single claim without leaving the directory.

```
<CRITERION>_<short name>/
    PREREG.md      frozen before anything ran; hash recorded in ../../preregistrations/README.md
    run.py         the implementation
    tests/         tests for this experiment's logic
    results/       this experiment's output, and nothing else
```

Shared across experiments, deliberately kept thin: `utils.py` (model loading, task loaders,
ablation hooks, metrics), `data/` (task CSVs with `PROVENANCE.md`), and `check_baselines.py`,
the gate that must pass before any result is meaningful.

## The nine

| Folder | Criterion | Question | Registered | Status |
|---|---|---|---|---|
| `I3_head_level_minimality` | Minimality | Do all 26 heads still earn their place under Wang et al.'s own score? | 2026-08-05 | implementation contradicts the frozen protocol; rewrite pending |
| `I6_double_dissociation` | Double dissociation | Does the IOI circuit dissociate from greater-than in both directions? | 2026-08-05 | implementation diverges from the frozen protocol; rewrite pending |
| `I7_frequency_and_length_confounds` | Confound control | Does the effect survive name-frequency and sequence-length controls? | 2026-08-05 | not implemented |
| `I11_onset_offset_coupling` | Onset coupling | Does circuit strength track capability as it is acquired and removed? | 2026-08-05 | runnable — checkpoints confirmed, see below |
| `E4_replication_across_seeds` | Cross-model generalization | Is the circuit a property of the architecture, or of one training run? | 2026-08-05 | implemented, not yet run |
| `E1_intervention_reach` | Intervention reach | How far does an intervention's effect propagate? | 2026-08-08 | implementation diverges; rewrite pending |
| `I4_specificity` | Specificity | Does ablating the circuit damage only its own task? | 2026-08-08 | superseded by published work; closing by citation |
| `I10_rescue_reversibility` | Rescue reversibility | Does restoring an ablated component restore the capability? | 2026-08-08 | implemented, diverges from registered design |
| `M7_selection_correction` | Selection correction | Does the copy-suppression figure survive re-estimation off its selected slice? | 2026-08-08 | first half implemented; threshold sweep has no code |

The first five were frozen together at commit `c643450`; the later four carry their own freeze
statements. All five of the first batch have been re-hashed after moving into this layout and
still match the freeze table, so the attestation covers these copies.

## Two corrections on record

**I11 is not blocked.** The paper says the criterion is untestable because GPT-2 small ships no
pretraining checkpoints. That is true of OpenAI's release and false of the architecture: each of
the five Stanford CRFM runs carries roughly 600 intermediate checkpoints, published as git tags
named `checkpoint-{STEP}` and resolvable through `revision=`. The frozen registry already said
so and asked for the paper's sentence to be corrected either way. Enumerating
`darkmatter-gpt2-small-x343` returns 609 tags against a single branch.

**I4 is answered in the literature.** Li & Subramani run the identical comparison and report that
circuits are not task-specific; Merullo et al. report that for this exact task pair there is
"virtually no overlap." Two published results pointing opposite ways close the criterion more
convincingly than one run of ours would, so it is closed by citation rather than re-derived.

`SCOOP_CHECK.md` records the prior-art check on all nine questions, together with the errors it
found in the frozen documents. Those errors are recorded rather than edited away — silently
correcting a frozen document would defeat the freeze.

## Running one

```bash
../.venv/bin/python check_baselines.py          # the gate; must pass first
cd I3_head_level_minimality && ../../.venv/bin/python run.py --n 1000
../../.venv/bin/python -m pytest tests/         # that experiment's tests
```
