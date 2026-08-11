# Audit YAML schema

One file per claim, `data/audits/<claim>.yaml`. Replaces `data/criteria/<claim>.csv`,
which recorded a status and a paraphrase and nothing that could be checked against a
source.

The rule this schema exists to enforce: **every status must be derivable from a verbatim
quote with a locator.** A criterion with no quotes is not an audit result; it is an
assertion, and the tooling marks it as such.

```yaml
claim: workspace
source:
  citation: gurnee2026verbalizable          # bib key
  title: Verbalizable Representations Form a Global Workspace in Language Models
  url: https://transformer-circuits.pub/2026/workspace/index.html
  local: null                               # path to a downloaded PDF, if one exists
  read_in_full: false                       # true only once someone has read it end to end

criteria:
  I1:
    name: Necessity
    status: C                               # C PC I U D N/A
    short: Four necessity demonstrations, three with controls
    verified: false                         # true only when quotes below were read from the source
    quotes:
      - text: >
          verbatim, no ellipsis inside a sentence, no paraphrase
        locator: "§4.2, Figure 6"           # section, figure or page. never just the paper
    reasoning: >
      Why those quotes yield that status. This is the auditor's argument and is expected
      to be arguable. It must not introduce facts absent from quotes.
    refs:                                   # post-origin work bearing on this criterion
      - citation: feucht2025dual
        text: >
          verbatim
        locator: "§5"
        direction: raises                   # raises | lowers | neutral
    notes: >
      Anything else. Contradictions found, cells that disagree with other artifacts,
      open questions. No length limit.
```

## The gate

`short` is what reaches the supplement. It may assert only what the quotes support.
`build/check_accountability.py` reports, per claim, how many criteria have zero quotes,
and no claim should enter the supplement until that count is zero.

`verified: false` with quotes present means the quotes came from an existing audit cell
rather than from the source. That is weaker than nothing, because it looks checked.

## Migration state

Everything migrated from `data/criteria/*.csv` starts at `verified: false`, `quotes: []`,
with the old paraphrase preserved under `notes` as `legacy_evidence`. Nothing is thrown
away and nothing is presented as verified that has not been.

## Known contradictions to resolve during verification

Recorded here so they are checked against the source rather than argued from the cells:

- **IOI, naive circuit.** `audit_tables_full/ACH_IOI.tex` says the naive circuit reaches
  faithfulness 0.1 against the full circuit's 0.46. `mechanistic_validity_v17.tex:786`
  says it "reaches comparable faithfulness". Wang et al. §4.3 decides it.
- **IOI verdict.** The main paper's case-study table says Underdetermined; the supplement's
  verdict table says Causally Suggestive. They may be scoring different readings, in which
  case each should say which.
- **SAE verdict.** Main paper says Disconfirmed for "SAE features as canonical units";
  supplement says Causally Suggestive for the primary reading. Same question.
- **J-space I4.** The long evidence reads "Tested three ways, and the audit's rationale
  asserts the opposite." The cell and its rationale disagree.
