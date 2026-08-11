# Mechanistic validity

A framework of validity criteria for mechanistic interpretability claims, and an audit of
sixteen published claims against it.

## Contents

```
paper/
    mechanistic_validity.tex    the paper
    supplement_audits.tex       per-claim audit tables, self-contained
    references.bib
    tmlr.sty  tmlr.bst          TMLR style
audits/
    *.yaml                      one record per audited claim: criterion statuses,
                                the quotations supporting each, and the rival
                                hypotheses each claim's evidence bears on
```

## Building

```bash
cd paper
pdflatex mechanistic_validity && bibtex mechanistic_validity
pdflatex mechanistic_validity && pdflatex mechanistic_validity
```

The supplement's tables are inlined, so the paper compiles from this directory alone.

## The audit records

Each YAML in `audits/` carries, per criterion, a status and the verbatim quotations from the
audited paper that support it, with the section and page they came from. Statuses are C
(established), PC (partially established), I (inconclusive), U (untested), D (disconfirmed),
and N/A (the claim's structure cannot pose the test). The tables in the supplement are
generated from these records, so the paper and the data cannot disagree.
