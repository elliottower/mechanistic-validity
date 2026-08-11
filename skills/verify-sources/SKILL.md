---
name: verify-sources
description: Back every claim about a source with a quotation that resolves in that source, checked mechanically. Use when writing or reviewing any assertion about what a paper says, building an audit or literature review, filling a related-work section, or before shipping prose that cites anything.
---

# Verify sources

A claim about what a paper says is worth exactly as much as the quotation behind it. This
skill makes that checkable instead of trusted.

## The rule

**Never assert what a source says without a quotation that resolves in the source.** Not
from memory, not from a summary, not from another paper's characterisation of it, not from a
search result. Open the source, find the sentence, record it.

If the source cannot be obtained, say so and leave the claim unmade. An unverifiable claim
that is flagged costs a sentence; one that is not costs the paper.

## What this catches, and what it does not

It catches **fabrication**: quotations that do not exist, statuses unsupported by their own
source, summaries that conflate two different results.

It does **not** catch **misinterpretation**. A real, resolving quotation can still be
misread, cherry-picked, or attached to the wrong claim. Every serious error in the audit that
produced this skill had a green gate: a faithfulness metric that is a gap where lower is
better, read as higher-is-better; a paper's null arm quoted as its finding; a result credited
to activation patching when the source used exhaustive enumeration.

So the gate is necessary and not sufficient. After it passes, the remaining question — does
this quotation actually support this claim — is still yours.

## Format

One YAML per source document.

```yaml
source:
  citation: wang2023interpretability
  local: reference/wang_2023_ioi.pdf     # relative to --root
  sha256: 3f9a...                        # optional; a changed source fails loudly
  extract_cmd: pdftotext -layout         # pinned, so line numbers mean something
claims:
  faithfulness-87:
    statement: "The circuit recovers 87% of the model's logit difference."
    verified: true                       # schema rejects this without quotes
    quotes:
      - exact: "C achieves 87% of the performance of M."
        section: "§4"                    # at least one of section / page / line
    notes: "unlimited"
```

Anchoring follows the W3C Web Annotation Data Model's `TextQuoteSelector`: `exact`, plus
`prefix` and `suffix` when `exact` alone is ambiguous. Offsets are advisory — they belong to
your extraction, so switching `-layout` to `-raw` moves every one of them. The selector does
not move.

## Run it

```bash
uv run --with pydantic --with pyyaml \
  ~/Documents/GitHub/mechanistic-validity/skills/verify-sources/references/verify_claims.py \
  claims/ --root . --strict
```

`--strict` exits 1, so it can gate a build. Wire it into whatever produces the document and
an unsupported claim cannot ship.

## Two invariants that are not negotiable

**`verified: true` without quotes is rejected by the schema.** That combination is an
assertion wearing a check's clothing, so it is a load error rather than a warning.

**A quote that resolves nowhere fails and is never deleted.** An earlier version truncated
unresolvable quotes to their longest matching prefix, which silently discarded the tail. If a
quote straddles a page header or a footnote, split it into adjacent fragments that reassemble
the whole. If it cannot be split, leave it in place so the gate keeps failing.

## Matching is two-tier and the tiers are reported separately

Exact first, on text normalised for what extraction invents: combining diacritics, the
dotless i from an `fi` ligature, smart quotes, the Unicode minus, hyphenation across line
breaks, the spaces LaTeX pads into inline math. If that fails, the alphanumeric skeleton,
which strips everything else.

A match found only at the skeleton level is reported as `loose`, never as exact, because the
skeleton cannot tell `a - b` from `a + b`. Treat a run with many loose matches as a run to
inspect, not a run that passed.

## Setting up a new document

1. Put sources in `reference/`, one file per citation key.
2. Pin each: record `sha256` and `extract_cmd`.
3. Write one claim YAML per source with `verified: false` and `quotes: []` everywhere.
4. Fill quotes by reading the source. Sub-agents can do this; the gate is what makes their
   output trustworthy, not the prompt.
5. Wire `--strict` into the build.

## Reference implementation

`references/verify_claims.py` — 184 lines, standalone, no repo assumptions. Copy it anywhere.

## Related

`mechval` skill for the validity framework these audits are scored against.
