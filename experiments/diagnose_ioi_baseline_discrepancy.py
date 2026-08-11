"""Why does Xu (arXiv:2606.05378) get 57% on IOI where Wang et al. get 99.3%?

Wang et al. report GPT-2 small predicting the indirect object over the subject 99.3% of the
time, over 100,000 examples. Xu reports "top-1 13%, IO-vs-subject 57%" on the same model and
task, and concludes "GPT-2 small does not solve IOI at 124M parameters". If Xu is right, the
gate on the I6 study fails and several pre-registered predictions rest on a baseline that is
not there.

The two papers' templates differ by one character. Wang's prompt ends at "to" and the answer
is " Mary", a leading-space token. Xu's prompt as printed ends "to " -- the space is already
consumed -- so the answer token would have to be "Mary" without one, which BPE treats as a
different and far rarer token.

This runs both variants on the same names, places and objects, and reports both metrics, so
the discrepancy is either reproduced or explained rather than argued about.

    python diagnose_ioi_baseline_discrepancy.py --n 500
"""
from __future__ import annotations

import argparse
import itertools
import random

import torch

import utils as C

NAMES = ["Mary", "John", "Tom", "James", "Dan", "Sid", "Martin", "Amy", "Anna", "Sarah",
         "Michael", "Chris", "Alex", "Sam", "Kate", "Emily", "Jack", "Luke", "Paul", "Mark"]
PLACES = ["store", "garden", "restaurant", "school", "hospital", "office"]
OBJECTS = ["drink", "kiss", "ring", "bone", "basketball", "computer"]


def build(n: int, trailing_space: bool, seed: int) -> list[tuple[str, str, str]]:
    """(prompt, correct answer, incorrect answer). Half ABBA, half BABA, as both papers use."""
    rng = random.Random(seed)
    out = []
    for i in range(n):
        a, b = rng.sample(NAMES, 2)
        place, obj = rng.choice(PLACES), rng.choice(OBJECTS)
        # ABBA: "When A and B ... B gave" -> IO is A.  BABA: "When B and A ... B gave" -> IO is A.
        name1, name2 = (a, b) if i % 2 == 0 else (b, a)
        subject = b
        io = a
        tail = "to " if trailing_space else "to"
        p = f"When {name1} and {name2} went to the {place}, {subject} gave a {obj} {tail}"
        # the answer carries its leading space only when the prompt has not consumed one
        sp = "" if trailing_space else " "
        out.append((p, f"{sp}{io}", f"{sp}{subject}"))
    return out


def measure(model, tok, rows, chunk: int) -> dict:
    """IO-over-S rate, mean logit difference, and whether the IO is the argmax over all tokens."""
    io_over_s, logit_diff, top1 = [], [], []
    for i in range(0, len(rows), chunk):
        batch = rows[i:i + chunk]
        prompts = [r[0] for r in batch]
        enc = tok(prompts, return_tensors="pt", padding=True)
        ids = enc["input_ids"].to(model.cfg.device)
        # index each example's own final token, never a pad
        last = enc["attention_mask"].sum(dim=1) - 1
        with torch.no_grad():
            logits = model(ids)
        final = logits[torch.arange(len(batch)), last.to(logits.device)]
        for j, (_, ans, wrong) in enumerate(batch):
            a_id = tok.encode(ans)[0]
            w_id = tok.encode(wrong)[0]
            d = float(final[j, a_id] - final[j, w_id])
            logit_diff.append(d)
            io_over_s.append(d > 0)
            top1.append(int(final[j].argmax()) == a_id)
    t = torch.tensor
    return {"n": len(rows),
            "io_over_s_pct": 100 * float(t(io_over_s, dtype=torch.float).mean()),
            "mean_logit_diff": float(t(logit_diff).mean()),
            "top1_pct": 100 * float(t(top1, dtype=torch.float).mean())}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--seed", type=int, default=42)     # Xu's stated RNG seed
    ap.add_argument("--chunk", type=int, default=25)
    a = ap.parse_args()

    model, tok = C.load_model(a.device)
    torch.manual_seed(a.seed)

    print(f"{'variant':<34}{'IO>S %':>9}{'logit diff':>13}{'top-1 %':>10}")
    results = {}
    for label, trailing in (("Wang: prompt ends 'to'", False),
                            ("Xu: prompt ends 'to ' (space)", True)):
        rows = build(a.n, trailing, a.seed)
        r = measure(model, tok, rows, a.chunk)
        results[label] = r
        print(f"  {label:<32}{r['io_over_s_pct']:>8.1f}{r['mean_logit_diff']:>13.3f}"
              f"{r['top1_pct']:>10.1f}")

    print(f"\n  Wang et al. report 99.3% IO-over-S and a mean logit difference of 3.56.")
    print(f"  Xu reports 57% IO-over-S and 13% top-1.")
    print("\n  Example prompt, each variant:")
    for label, trailing in (("Wang", False), ("Xu", True)):
        p, ans, _ = build(1, trailing, a.seed)[0]
        print(f"    {label:<5} {p!r}  ->  {ans!r}  (token id {tok.encode(ans)[0]})")

    C.save("ioi_baseline_discrepancy", {"seed": a.seed, "variants": results},
           __import__("pathlib").Path("results"))


if __name__ == "__main__":
    main()
