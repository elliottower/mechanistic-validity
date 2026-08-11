"""Find a fetchable link for every source record that lacks one.

Queries Crossref, then arXiv, by title and first author. A match is accepted only when the
returned title matches the record's closely and the first author's surname appears in the
returned author list -- a title-only match is how you end up citing a different paper by
someone with the same surname, which has happened five times in this project already.

Anything that fails either test is left alone and listed, so a human decides rather than a
fuzzy match deciding silently.

    python resolve_source_links.py --check      # report what it would set
    python resolve_source_links.py              # write
"""
from __future__ import annotations

import argparse
import difflib
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

import yaml

SOURCES = pathlib.Path(__file__).resolve().parent / "sources"
UA = "mechanistic-validity/1.0 (mailto:elliot@elliottower.ai)"
TITLE_MIN = 0.87


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", (s or "").lower()).strip()


def close(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def surname(author: str) -> str:
    a = author.split(",")[0] if "," in author else author.split()[-1] if author else ""
    return norm(a)


def get(url: str) -> dict | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


def try_crossref(title: str, first: str, venue_want: str = "") -> tuple[str, str] | None:
    """Best candidate matching title and first author, preferring the venue we cite.

    Without the venue check this returns whichever record Crossref ranks first, which is often
    a secondary version -- the NBER working paper rather than the JASA article, a journal-club
    reprint rather than the Lancet original. Same work, wrong version of record.
    """
    q = urllib.parse.urlencode({"query.bibliographic": title, "rows": 8})
    d = get(f"https://api.crossref.org/works?{q}")
    if not d:
        return None
    best = None
    for it in d.get("message", {}).get("items", []):
        t = (it.get("title") or [""])[0]
        ts = close(t, title)
        if ts < TITLE_MIN:
            continue
        fams = {norm(a.get("family", "")) for a in it.get("author", [])}
        if first and surname(first) not in fams:
            continue
        container = (it.get("container-title") or [""])[0]
        vs = close(container, venue_want) if (venue_want and container) else 0.0
        # a strong venue match outweighs Crossref's own ranking
        score = ts + 1.5 * vs
        if best is None or score > best[0]:
            best = (score, it.get("DOI"), t, container)
    if not best:
        return None
    return best[1], best[2]


def try_arxiv(title: str, first: str) -> tuple[str, str] | None:
    q = urllib.parse.urlencode({"search_query": f'ti:"{title}"', "max_results": 3})
    try:
        req = urllib.request.Request(f"https://export.arxiv.org/api/query?{q}",
                                     headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            xml = r.read().decode()
    except Exception:
        return None
    for entry in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        tm = re.search(r"<title>(.*?)</title>", entry, re.S)
        im = re.search(r"<id>(.*?)</id>", entry)
        if not tm or not im:
            continue
        t = " ".join(tm.group(1).split())
        if close(t, title) < TITLE_MIN:
            continue
        fams = {surname(n) for n in re.findall(r"<name>(.*?)</name>", entry)}
        if first and surname(first) not in fams:
            continue
        return im.group(1).split("/abs/")[-1], t
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    todo = []
    for p in sorted(SOURCES.glob("*.yaml")):
        r = yaml.safe_load(p.read_text()) or {}
        if not (r.get("url") or r.get("doi")):
            todo.append((p, r))
    if a.limit:
        todo = todo[:a.limit]
    print(f"  {len(todo)} records without a link\n")

    found = unresolved = 0
    for p, r in todo:
        title = r.get("title", "")
        first = (r.get("authors") or [""])[0]
        if not title:
            print(f"  {p.stem:<34}no title in the record"); unresolved += 1; continue
        hit = try_crossref(title, first, r.get("venue", ""))
        kind = "doi"
        if not hit:
            time.sleep(0.4)
            hit = try_arxiv(title, first)
            kind = "arxiv"
        time.sleep(0.4)
        if not hit:
            print(f"  {p.stem:<34}no confident match"); unresolved += 1; continue
        ident, matched = hit
        url = (f"https://doi.org/{ident}" if kind == "doi"
               else f"https://arxiv.org/abs/{ident}")
        found += 1
        print(f"  {p.stem:<34}{kind:<6}{ident}")
        if not a.check:
            r["url"] = url
            if kind == "doi":
                r["doi"] = ident
            else:
                r["arxiv"] = ident
            p.write_text(yaml.safe_dump(r, sort_keys=False, allow_unicode=True, width=100))

    print(f"\n  resolved {found}, left for a human {unresolved}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
