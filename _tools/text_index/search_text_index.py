#!/usr/bin/env python3
"""
Search JSONL text index (stdlib only).

Supports:
- substring search (case-insensitive by default)
- filter by source/year
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="Search text index JSONL.")
    ap.add_argument("--index", required=True, help="Path to index.jsonl")
    ap.add_argument("--query", required=True, help="Substring or regex to search")
    ap.add_argument("--regex", action="store_true", help="Treat query as regex")
    ap.add_argument("--case-sensitive", action="store_true", help="Case-sensitive search")
    ap.add_argument("--source", default=None, help="Filter by source (tg_daily/tg_daily2025/tg_literary/lj/ig/book)")
    ap.add_argument("--year", default=None, help="Filter by year (YYYY)")
    ap.add_argument("--limit", type=int, default=20, help="Max results to print")
    args = ap.parse_args()

    idx = Path(args.index)
    if not idx.exists():
        raise SystemExit(f"Index not found: {idx}")

    flags = 0 if args.case_sensitive else re.IGNORECASE
    pattern = re.compile(args.query, flags) if args.regex else None

    shown = 0
    matched = 0

    with idx.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue

            if args.source and rec.get("source") != args.source:
                continue
            if args.year and rec.get("year") != args.year:
                continue

            text = rec.get("text") or ""
            if not isinstance(text, str):
                continue

            ok = False
            if pattern:
                ok = bool(pattern.search(text))
            else:
                q = args.query if args.case_sensitive else args.query.lower()
                hay = text if args.case_sensitive else text.lower()
                ok = q in hay

            if not ok:
                continue

            matched += 1
            if shown >= args.limit:
                continue

            date = rec.get("date") or ""
            src = rec.get("source") or ""
            path = rec.get("path") or ""
            title = rec.get("title") or ""
            url = rec.get("url") or ""
            preview = " ".join(text.split())
            if len(preview) > 240:
                preview = preview[:237] + "…"

            print(f"- [{src}] {date} {title}".strip())
            print(f"  path: {path}")
            if url:
                print(f"  url: {url}")
            print(f"  {preview}")
            print("")
            shown += 1

    print(f"[done] matched={matched} shown={min(shown, args.limit)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



