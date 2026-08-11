# Results that answer a different document

These were produced by implementations that diverge from the pre-registrations they claim to
run — checked independently and confirmed for I3, I6, E1, I4 and M7. They are kept because
deleting them would hide that the divergence happened, and they are kept *here* because leaving
them beside a pre-registration they do not implement invites exactly the misreading the freeze
exists to prevent.

| File | Sits under | Actually tests | Why it is void |
|---|---|---|---|
| `e1_double_dissociation.json` | criterion I6 | criterion I6 | ran zero/resample/native ablation with a permutation test; the frozen protocol specifies mean ablation, normalized D, 200 size- and layer-matched random controls, and a bootstrap CI |
| `e5_intervention_reach.json` | criterion E1 | criterion E1 | ran zero/resample/native/gaussian from a natural-text pool; the frozen protocol's mean-over-ABC against resample-from-ABC arm — the one contrast Miller et al. ran — is absent |

## The label collision that produced these filenames

The 2026-08-08 pre-registration numbers its five studies E1 through E5 internally. Those labels
collide with the framework's own criterion identifiers E1 through E6, and the two numbering
schemes do not line up:

| Pre-registration's label | Criterion actually tested |
|---|---|
| E1 | I6, double dissociation |
| E2 | M7, selection correction |
| E3 | I10, rescue reversibility |
| E4 | I4, specificity |
| E5 | E1, intervention reach |

So `e1_double_dissociation.json` names the pre-registration's first study, not criterion E1, and
`e5_intervention_reach.json` names its fifth, which *is* criterion E1. Rewritten implementations
should name their output for the criterion, not for the pre-registration's internal ordering.

This is the second identifier collision on record in this project. The registry documents the
first: the paper assigns I11 to onset-offset coupling while the documentation site assigns I11
to directed information flow.
