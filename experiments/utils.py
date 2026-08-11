"""Shared pieces for the pre-registered experiments: circuits, tasks, ablations, metrics.

One module beside the experiments rather than a package to install into. Each experiment
folder holds its pre-registration, its code and its results, and imports what it shares from
here. Vendoring a copy into each folder is what produced three different definitions of the
IOI circuit across this project, so the sharing is deliberate; the shallowness is too.

Pure logic, no Modal and no CLI. Every experiment script imports from here so the circuit
definitions and the ablation procedure exist once. The Modal wrapper calls the same
functions, which is what keeps a cloud run and a local run comparable.

Circuit specifications are transcribed from the source PDFs pinned in the audit records,
not from memory or from a reimplementation. Each carries the sentence it came from.
"""
from __future__ import annotations

import json
import pathlib
import random
from dataclasses import dataclass, field

import torch

from mechval.paths import EXPERIMENT_DATA as DATA

# Results live beside the experiment that produced them, not in a shared dump.
# The caller passes its own directory; nothing here guesses a location.
MODEL = "gpt2"
_MODELS: dict = {}   # (name, device) -> (model, tokenizer)
SEED_POOL = 12345          # for the shared natural-text activation pool only

# --------------------------------------------------------------------------- circuits

# Wang et al. 2023, "Interpretability in the Wild", 26 heads in seven classes.
#
# Three of the twenty-six are rendered parenthesised in the source's Figure 2 --
# "0.1 3.0 (0.10) 5.5 6.9 (5.8 5.9)" -- and arrive in the body as a later addition:
# "we identify 3 new heads influencing positively the logit difference: 5.9, 5.8 and 0.10."
# So the paper supports two component sets, 23 without them and 26 with, and which one an
# ablation uses is exactly the sort of unstated choice Miller et al. show moves faithfulness
# by tens of percentage points. Both are defined; experiments report the 26-head set, which
# is what the pre-registration commits to, and the 23-head set as a robustness check.
IOI_CORE: dict[str, list[tuple[int, int]]] = {
    "name_mover":          [(9, 9), (9, 6), (10, 0)],
    "negative_name_mover": [(10, 7), (11, 10)],
    "backup_name_mover":   [(9, 0), (9, 7), (10, 1), (10, 2),
                            (10, 6), (10, 10), (11, 2), (11, 9)],
    "s_inhibition":        [(7, 3), (7, 9), (8, 6), (8, 10)],
    "induction":           [(5, 5), (6, 9)],
    "duplicate_token":     [(0, 1), (3, 0)],
    "previous_token":      [(2, 2), (4, 11)],
}
IOI_LATER = {"induction": [(5, 8), (5, 9)], "duplicate_token": [(0, 10)]}
IOI_CLASSES = {k: v + IOI_LATER.get(k, []) for k, v in IOI_CORE.items()}

IOI_HEADS = [h for hs in IOI_CLASSES.values() for h in hs]          # 26
IOI_HEADS_CORE = [h for hs in IOI_CORE.values() for h in hs]        # 23
assert len(IOI_HEADS) == 26 and len(IOI_HEADS_CORE) == 23

# Hanna et al. 2023, "How Does GPT-2 Compute Greater-Than?": "MLP 9 relies on a9.h1, while
# MLP 8 relies on a8.h11, a8.h8, a7.h10, a6.h9, a5.h5, and a5.h1; we add these to our
# circuit." MLPs 8-11 carry the year-span computation.
GT_HEADS = [(5, 1), (5, 5), (6, 9), (7, 10), (8, 8), (8, 11), (9, 1)]
GT_MLPS = [8, 9, 10, 11]


@dataclass
class Circuit:
    name: str
    heads: list[tuple[int, int]]
    mlps: list[int] = field(default_factory=list)


IOI_CIRCUIT = Circuit("ioi", IOI_HEADS)
IOI_CIRCUIT_CORE = Circuit("ioi_core23", IOI_HEADS_CORE)
GT_CIRCUIT = Circuit("greater_than", GT_HEADS, GT_MLPS)

# --------------------------------------------------------------------------- tasks



@dataclass
class Batch:
    """Clean and corrupted prompts with the token ids the metric compares.

    `last` is the index of each prompt's final real token. TransformerLens right-pads a
    batch with <|endoftext|>, so reading logits at position -1 reads padding for every
    prompt shorter than the longest one. IOI prompts run 15 to 20 tokens, so that was most
    of them, and it dragged the measured logit difference to 0.50 against a published 3.56.
    Every metric indexes here instead.
    """
    clean: list[str]
    corrupt: list[str]
    answer: list[int]        # IOI: token id that should win. greater-than: the year YY.
    wrong: list[int]         # IOI: token id it should beat. greater-than: -1.
    meta: dict
    last: list[int] = field(default_factory=list)


def _last_positions(model, prompts: list[str]) -> list[int]:
    """Index of the final real token per prompt, accounting for the prepended BOS."""
    return [len(model.tokenizer.encode(t)) for t in prompts]


def _final(logits, batch: Batch):
    """Logits at each example's own final token."""
    idx = torch.tensor(batch.last, device=logits.device).clamp(max=logits.shape[1] - 1)
    return logits[torch.arange(logits.shape[0], device=logits.device), idx, :]


def _load(csv: str, n: int, model) -> "pd.DataFrame":
    """Published rows only, filtered to those whose clean and corrupted tokenise alike.

    The length filter matches the reference loader: a corrupted prompt of a different
    length cannot be used to build a cache that lines up with the clean run.
    """
    import pandas as pd
    df = pd.read_csv(DATA / csv)
    keep = [i for i, r in df.iterrows()
            if model.to_tokens(r["clean"]).shape[1]
            == model.to_tokens(r["corrupted"]).shape[1]]
    return df.loc[keep[:n]] if n else df.loc[keep]


def load_ioi(model, n: int = 0) -> Batch:
    """MIB's IOI dataset. `corrupted` is the ABC distribution, as Wang et al. define it."""
    df = _load("ioi_gpt2.csv", n, model)
    return Batch(df["clean"].tolist(), df["corrupted"].tolist(),
                 df["correct_idx"].astype(int).tolist(),
                 df["incorrect_idx"].astype(int).tolist(),
                 {"task": "ioi", "n": len(df), "source": "MIB ioi/gpt2.csv"},
                 _last_positions(model, df["clean"].tolist()))


def load_greater_than(model, n: int = 0) -> Batch:
    """MIB's greater-than dataset. `corrupted` substitutes the 01 year."""
    df = _load("greater_than_gpt2.csv", n, model)
    return Batch(df["clean"].tolist(), df["corrupted"].tolist(),
                 df["correct_idx"].astype(int).tolist(),
                 [-1] * len(df),
                 {"task": "greater_than", "n": len(df),
                  "source": "MIB greater-than/gpt2.csv"},
                 _last_positions(model, df["clean"].tolist()))


def load_gender_bias(model, n: int = 0) -> Batch:
    """MIB's gender-bias dataset. Scored as a logit difference like IOI."""
    df = _load("gender_bias_gpt2.csv", n, model)
    return Batch(df["clean"].tolist(), df["corrupted"].tolist(),
                 df["clean_answer_idx"].astype(int).tolist(),
                 df["corrupted_answer_idx"].astype(int).tolist(),
                 {"task": "gender_bias", "n": len(df),
                  "source": "MIB gender-bias/gpt2.csv"},
                 _last_positions(model, df["clean"].tolist()))


def load_sva(model, n: int = 0) -> Batch:
    """MIB's subject-verb agreement dataset.

    `plural` gives the clean form; the metric compares the plural and singular verb
    continuations, so the answer/wrong pair is built from the two inflections the dataset
    contrasts through its clean/corrupted pair.
    """
    df = _load("sva_gpt2.csv", n, model)
    tok = model.tokenizer
    ans, wrong = [], []
    for _, r in df.iterrows():
        # The corrupted prompt flips number, so the correct continuation for the clean
        # prompt is the incorrect one for the corrupted prompt and vice versa.
        ans.append(tok.encode(" are")[0] if int(r["plural"]) else tok.encode(" is")[0])
        wrong.append(tok.encode(" is")[0] if int(r["plural"]) else tok.encode(" are")[0])
    return Batch(df["clean"].tolist(), df["corrupted"].tolist(), ans, wrong,
                 {"task": "sva", "n": len(df), "source": "MIB sva/gpt2.csv"},
                 _last_positions(model, df["clean"].tolist()))


# --------------------------------------------------------------------------- metrics

def ioi_logit_diff(logits, batch: Batch) -> torch.Tensor:
    """Logit of the indirect object minus logit of the subject, at the final position."""
    last = _final(logits, batch)
    a = torch.tensor(batch.answer, device=last.device)
    w = torch.tensor(batch.wrong, device=last.device)
    return last.gather(1, a[:, None]).squeeze(1) - last.gather(1, w[:, None]).squeeze(1)


def gt_prob_diff(logits, batch: Batch, tok) -> torch.Tensor:
    """P(year > YY) - P(year < YY) over the two-digit continuations, as Hanna et al. define it."""
    probs = _final(logits, batch).softmax(-1)
    out = []
    two_digit = torch.tensor([tok.encode(f"{d:02d}")[0] for d in range(100)],
                             device=probs.device)
    for i, yy in enumerate(batch.answer):
        p = probs[i, two_digit]
        out.append(p[yy + 1:].sum() - p[:yy].sum())
    return torch.stack(out)


def accuracy(logits, batch: Batch, task: str, tok=None) -> torch.Tensor:
    """Did the correct continuation beat the incorrect one? Per example, 1.0 or 0.0.

    Every task here reduces to that question, which is what makes cross-task comparison
    possible. Logit difference and probability difference have no common unit, so a
    specificity claim built on comparing them directly compares nothing.
    """
    if task == "greater_than":
        return (gt_prob_diff(logits, batch, tok) > 0).float()
    return (ioi_logit_diff(logits, batch) > 0).float()


# --------------------------------------------------------------------------- ablation

def natural_text_pool(model, tok, n_seq: int = 8, seq_len: int = 256) -> dict:
    """A shared pool of activations from real text, identical for every circuit.

    Drawn from the Pile. An earlier version generated word salad from a fixed vocabulary,
    which made the resample condition an ablation toward nonsense rather than toward
    plausible alternative activations.

    The pre-registration decides the criterion on ablations that involve no task-specific
    distribution, because IOI's ABC and greater-than's 01 corruptions are different kinds
    of object and using each task's own would confound the dissociation with the
    corruption mechanism.

    Returned flat: attention entries are (N, head, d_head) and MLP entries (N, d_model),
    with N = n_seq * seq_len positions to draw from. GPT-2's context is 1024, so the pool
    is several short sequences rather than one long one.
    """
    from datasets import load_dataset
    ds = load_dataset("NeelNanda/pile-10k", split="train")
    rng = random.Random(SEED_POOL)
    seqs = []
    for i in rng.sample(range(len(ds)), min(n_seq * 20, len(ds))):
        ids = tok.encode(ds[i]["text"])
        if len(ids) >= seq_len:
            seqs.append(ids[:seq_len])
        if len(seqs) == n_seq:
            break
    if len(seqs) < n_seq:
        raise RuntimeError(f"only {len(seqs)} sequences of length {seq_len} available")
    with torch.no_grad():
        _, cache = model.run_with_cache(torch.tensor(seqs))
    flat = {}
    for name in cache.keys():
        if name.endswith("attn.hook_z") or name.endswith("hook_mlp_out"):
            t = cache[name]                       # (batch, pos, ...)
            flat[name] = t.reshape(-1, *t.shape[2:])
    return flat


def ablate_hooks(circuit: Circuit, mode: str, pool=None, corrupt_cache=None):
    """Hook list that ablates the circuit's components under the named mode.

    mode is one of the pre-registered conditions:
      "zero"     Z, no distribution choice at all
      "resample" R, drawn from the shared natural-text pool
      "native"   N, the task's own corruption; reported but not decisive
    """
    if mode not in ("zero", "resample", "native"):
        raise ValueError(f"unknown ablation mode {mode!r}")
    hooks = []

    def head_hook(layer: int, head: int):
        def fn(z, hook):
            if mode == "zero":
                z[:, :, head, :] = 0.0
            elif mode == "resample":
                src = pool[hook.name]                          # (N, head, d_head)
                idx = torch.randint(0, src.shape[0], (z.shape[0], z.shape[1]))
                z[:, :, head, :] = src[idx, head, :].to(z.dtype)
            else:
                z[:, :, head, :] = corrupt_cache[hook.name][:, :, head, :]
            return z
        return f"blocks.{layer}.attn.hook_z", fn

    def mlp_hook(layer: int):
        def fn(out, hook):
            if mode == "zero":
                return torch.zeros_like(out)
            if mode == "resample":
                src = pool[hook.name]                          # (N, d_model)
                idx = torch.randint(0, src.shape[0], (out.shape[0], out.shape[1]))
                return src[idx].to(out.dtype)
            return corrupt_cache[hook.name]
        return f"blocks.{layer}.hook_mlp_out", fn

    for layer, head in circuit.heads:
        hooks.append(head_hook(layer, head))
    for layer in circuit.mlps:
        hooks.append(mlp_hook(layer))
    return hooks


# --------------------------------------------------------------------------- io

def save(name: str, payload: dict, results_dir: pathlib.Path) -> pathlib.Path:
    """Every run writes a file. Nothing is reported from stdout alone."""
    results_dir.mkdir(parents=True, exist_ok=True)
    p = results_dir / f"{name}.json"
    p.write_text(json.dumps(payload, indent=2, default=str))
    print(f"wrote {p}")
    return p


def load_model(device: str = "cpu", name: str | None = None):
    """A HookedTransformer, cached per (name, device).

    `name` defaults to MODEL. E4 loads six different runs of the same architecture, so the
    model is a parameter rather than a constant.
    """
    key = (name or MODEL, device)
    if key not in _MODELS:
        from transformer_lens import HookedTransformer
        m = HookedTransformer.from_pretrained(key[0], device=device)
        m.set_use_attn_result(False)
        _MODELS[key] = (m, m.tokenizer)
    return _MODELS[key]


# ------------------------------------------------------- shared measurement
def _slice(batch: Batch, i: int, j: int) -> Batch:
    return Batch(batch.clean[i:j], batch.corrupt[i:j],
                   batch.answer[i:j], batch.wrong[i:j], batch.meta,
                   batch.last[i:j])


def measure(model, tok, batch: Batch, task: str, hooks=None,
            chunk: int = 100, circ=None, mode=None, pool=None,
            score: str = "accuracy") -> torch.Tensor:
    """Per-example metric for one task, in chunks so activation caches stay bounded.

    Native mode needs the corrupted run's cache, which is the size of the batch times the
    whole activation set. Caching that for n=1000 at once costs gigabytes for no reason,
    so the corrupt cache is rebuilt per chunk and discarded.

    score="accuracy" is the default and is what a dissociation requires. IOI is scored by
    logit difference and greater-than by probability difference; those have no common unit,
    and IOI's baseline sits at 0.50 against greater-than's 0.83, so comparing raw deficits
    across the two measures headroom rather than mechanism. Accuracy puts both on 0--1.
    score="logit" is kept for faithfulness, where the quantity of interest is the logit
    difference itself rather than a comparison across tasks.
    """
    out = []
    for i in range(0, len(batch.clean), chunk):
        sub = _slice(batch, i, min(i + chunk, len(batch.clean)))
        h = hooks
        if mode == "native":
            with torch.no_grad():
                _, cc = model.run_with_cache(model.to_tokens(sub.corrupt))
            h = ablate_hooks(circ, "native", corrupt_cache=cc)
        with torch.no_grad():
            ids = model.to_tokens(sub.clean)
            logits = model.run_with_hooks(ids, fwd_hooks=h) if h else model(ids)
        if score == "accuracy":
            out.append(accuracy(logits, sub, task, tok))
        else:
            out.append(ioi_logit_diff(logits, sub) if task == "ioi"
                       else gt_prob_diff(logits, sub, tok))
    return torch.cat(out)
