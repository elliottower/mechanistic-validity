"""One provenance record per cited work.

Every entry in the bibliography gets a file in `claims/`, keyed by its citation key. Most carry
bibliographic provenance only -- who wrote it, where it appeared, and the url or DOI needed to
fetch it. Sixteen carry much more: those are the audited papers, and their records hold the
claim as stated plus every verbatim quotation the audit rests on.

Depth is recorded explicitly in each file so the difference is visible rather than inferred:

    audited     the paper is one of the sixteen; full extraction, quotations, pinned sha256
    quoted      quoted inside an audit's ref block; pinned artifact, some quotations
    cited       named in the paper; bibliographic provenance only

    python build_claim_records.py --check    # report, write nothing
    python build_claim_records.py
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent
BIB = ROOT / "paper" / "references.bib"
TEX = ROOT / "paper" / "mechanistic_validity.tex"
CLAIMS = ROOT / "sources"

FIELD = re.compile(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*$", re.S)


def strip_tex(s: str) -> str:
    s = re.sub(r"[{}]", "", s)
    s = re.sub(r"\\emph\{([^}]*)\}", r"\1", s)
    s = s.replace("\\&", "&").replace("--", "-").replace("\\", "")
    return " ".join(s.split())


def parse_bib(text: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for m in re.finditer(r"@(\w+)\s*\{([^,]+),(.*?)\n\}", text, re.S):
        kind, key, body = m.group(1).lower(), m.group(2).strip(), m.group(3)
        rec: dict[str, str] = {"type": kind}
        for line in re.split(r",\s*\n", body):
            fm = FIELD.search(line.strip())
            if fm:
                rec[fm.group(1).lower()] = strip_tex(fm.group(2))
        out[key] = rec
    return out


def cited_keys(tex: str) -> set[str]:
    used: set[str] = set()
    for grp in re.findall(r"\\cite[tp]?\*?(?:\[[^\]]*\])*\{([^}]*)\}", tex):
        used |= {x.strip() for x in grp.split(",") if x.strip()}
    return used


def authors(raw: str) -> list[str]:
    if not raw:
        return []
    return [" ".join(a.split()) for a in re.split(r"\s+and\s+", raw) if a.strip()]


def venue(rec: dict) -> str:
    for k in ("booktitle", "journal", "howpublished", "school", "publisher"):
        if rec.get(k):
            return rec[k]
    return ""


def identifier(rec: dict) -> dict:
    out = {}
    if rec.get("url"):
        out["url"] = rec["url"]
    if rec.get("doi"):
        out["doi"] = rec["doi"]
    note = rec.get("note", "")
    m = re.search(r"arXiv:\s*(\d{4}\.\d{4,5})", note)
    if m:
        out.setdefault("arxiv", m.group(1))
        out.setdefault("url", f"https://arxiv.org/abs/{m.group(1)}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    bib = parse_bib(BIB.read_text())
    used = cited_keys(TEX.read_text())

    sys.path.insert(0, str(ROOT / "src"))
    from mechval.audit import Audit                      # noqa: E402
    from mechval.paths import claims as audited_claims   # noqa: E402

    # the sixteen, and every work quoted inside one of their ref blocks
    audited_key, quoted = {}, {}
    for name in audited_claims():
        rec = Audit.load(name)
        audited_key[rec.source.citation] = name
        for c in rec.criteria.values():
            for r in c.refs:
                q = quoted.setdefault(r.citation, {"quotes": [], "local": None, "sha256": None})
                if r.text:
                    q["quotes"].append({"text": r.text, "section": r.section or "",
                                        "direction": r.direction})
                q["local"] = q["local"] or r.local
                q["sha256"] = q["sha256"] or r.sha256

    counts = {"audited": 0, "quoted": 0, "cited": 0, "uncited": 0}
    for key, rec in sorted(bib.items()):
        depth = ("audited" if key in audited_key
                 else "quoted" if key in quoted
                 else "cited" if key in used else "uncited")
        counts[depth] += 1
        if a.check:
            continue
        if depth == "audited":
            continue          # already written, and far richer than anything here
        doc = {
            "citation": key,
            "depth": depth,
            "title": rec.get("title", ""),
            "authors": authors(rec.get("author", "")),
            "year": rec.get("year", ""),
            "venue": venue(rec),
            **identifier(rec),
        }
        if depth == "quoted":
            q = quoted[key]
            if q["local"]:
                doc["local"] = q["local"]
            if q["sha256"]:
                doc["sha256"] = q["sha256"]
            doc["quotes"] = q["quotes"]
        CLAIMS.mkdir(exist_ok=True)
        (CLAIMS / f"{key}.yaml").write_text(
            yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100))

    print(f"  audited (the sixteen, full extraction) {counts['audited']:>4}")
    print(f"  quoted inside an audit ref block       {counts['quoted']:>4}")
    print(f"  cited in the paper                     {counts['cited']:>4}")
    print(f"  in the bibliography but never cited    {counts['uncited']:>4}")
    print(f"  {'-'*42}")
    print(f"  total records                          {sum(counts.values()):>4}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
