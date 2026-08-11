# Data provenance

Both files are the published MIB task datasets, copied verbatim from
`constrained-alignment-maps/data/mib/` on 2026-08-08. Nothing here is generated.

| file | source | rows | columns |
|---|---|---|---|
| `ioi_gpt2.csv` | MIB `ioi/gpt2.csv` | 1000 | clean, corrupted (ABC), corrupted_hard (ABB), correct_idx, incorrect_idx |
| `greater_than_gpt2.csv` | MIB `greater-than/gpt2.csv` | 1000 | clean, corrupted (01), correct_idx |

An earlier version of these experiments used hand-written prompt generators -- four IOI
templates, sixteen names, a synthesised year-span string. Every result computed on them was
discarded. The generators have been deleted rather than left in the file, so they cannot be
selected again by accident.
