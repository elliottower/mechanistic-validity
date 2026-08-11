"""Generate the paper's tables and sections from the audit records.

Nothing in `paper/generated/` is written by hand. Every table traces to a YAML record whose
quotations the gate has resolved, so the paper cannot state a status its evidence does not
carry. Regenerating is how the paper stays honest when an audit changes.

    mechval-render              # every claim
    mechval-render ioi sae      # named ones
"""
from __future__ import annotations

import argparse
import sys

from mechval.paths import GENERATED, claims


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("claims", nargs="*", help="claim names; default is all")
    args = ap.parse_args()

    from mechval.render import criterion_table, section, views_page

    made, skipped = 0, []
    for c in (args.claims or claims()):
        criterion_table.write(c)
        section.write(c)
        if views_page.write(c) is None:
            skipped.append(c)
        made += 1
    print(f"{made} claims rendered into {GENERATED.relative_to(GENERATED.parent.parent)}")
    if skipped:
        print(f"no views table for {', '.join(skipped)} (no rival hypotheses recorded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
