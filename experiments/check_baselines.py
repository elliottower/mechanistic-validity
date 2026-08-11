"""Reproduce published baselines before trusting anything else this pipeline computes.

Two rounds of results were discarded for want of this check, and both would have failed it
in seconds.

The first ran on hand-written prompts instead of the published datasets. The second scored
`logits[:, -1, :]` on a right-padded batch, so for most examples it read an <|endoftext|>
position rather than the end of the prompt. In both rounds IOI's logit difference sat near
0.5 against Wang et al.'s published 3.56, in the output, unremarked, while the numbers built
on top of it were discussed at length.

A pipeline that cannot reproduce a known quantity has no standing to report an unknown one.
This runs first and fails loudly.

    python check_baselines.py
"""
from __future__ import annotations

import sys

import torch

import utils as C

# Quantity, source, and the tolerance we will accept. Tolerances are wide on purpose: the
# point is to catch an order-of-magnitude error, not to claim an exact replication of a
# number computed on a different prompt sample.
CHECKS = [
    {
        "name": "IOI logit difference",
        "published": 3.56,
        "cite": "Wang et al. 2023, §4: F(M) = 3.56",
        "tol_frac": 0.35,
    },
    {
        "name": "IOI accuracy",
        "published": 1.00,
        "cite": "GPT-2 small solves IOI on the MIB set; anything near 0.5 is chance",
        "tol_frac": 0.10,
    },
]


def main() -> int:
    model, tok = C.load_model("cpu")
    ioi = C.load_ioi(model, 200)
    with torch.no_grad():
        logits = model(model.to_tokens(ioi.clean))
    got = {
        "IOI logit difference": float(C.ioi_logit_diff(logits, ioi).mean()),
        "IOI accuracy": float(C.accuracy(logits, ioi, "ioi").mean()),
    }

    failed = 0
    print(f"{'quantity':<26}{'measured':>10}{'published':>11}{'':>4}source")
    for c in CHECKS:
        v, p = got[c["name"]], c["published"]
        ok = abs(v - p) <= c["tol_frac"] * abs(p)
        failed += not ok
        print(f"{c['name']:<26}{v:>10.4f}{p:>11.2f}  {'ok ' if ok else 'FAIL'} {c['cite']}")

    # A padding error is invisible in the mean but obvious in the token lengths.
    lens = ioi.last
    print(f"\nprompt lengths {min(lens)}-{max(lens)} tokens, batch padded to "
          f"{model.to_tokens(ioi.clean).shape[1]}; metrics index each example's own end")

    if failed:
        print(f"\n{failed} baseline(s) failed. Nothing downstream is trustworthy.")
    else:
        print("\nbaselines reproduce; downstream results may be computed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
