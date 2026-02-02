#!/usr/bin/env python3
"""
Build a unified JSONL index of texts across the workspace (stdlib only).

Output: JSON Lines, one object per document/message/post.

Each record (best-effort):
  - source: tg_daily | tg_daily2025 | tg_literary | lj | ig | book
  - date: YYYY-MM-DD (if known)
  - year: YYYY (if known)
  - path: relative path to source file
  - title: inferred short title/topic (if any)
  - text: clean text (no metadata, no reactions)
  - url: if present (IG MD first line or LJ url line)
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable, Iterator


ROOT = Path(__file__).resolve().parents[2]


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)


def ensure_dir(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def strip_md_metadata(md: str) -> tuple[str | None, str | None, str]:
    """
    For our per-post MD:
      - first line: "# YYYY-MM-DD — topic"
      - meta lines: *Datetime*, *From*, *Message ID*, etc.
      - then blank line, then body
      - optionally Links:/Reactions: blocks at end
    """
    lines = md.splitlines()
    title = None
    date = None
    if lines and lines[0].startswith("# "):
        title_line = lines[0][2:].strip()
        title = title_line
        # accept both em dash and hyphen as separators
        m = re.match(r"^(\d{4}-\d{2}-\d{2})\s*(?:—|-|–)\s*(.+)$", title_line)
        if m:
            date = m.group(1)
            title = m.group(2).strip()
        else:
            # fallback: infer date from filename-like prefix inside the title line
            m2 = re.match(r"^(\d{4}-\d{2}-\d{2})\b", title_line)
            if m2:
                date = m2.group(1)
                # keep full title_line as title

    # drop header until first blank line
    parts = md.split("\n\n", 1)
    body = parts[1] if len(parts) == 2 else md

    # remove trailing blocks
    body = re.sub(r"\n\nReactions:.*$", "", body, flags=re.S)
    body = re.sub(r"\n\nLinks:\n(?:- .*\n?)+$", "", body, flags=re.S)
    body = body.strip()
    return date, title, body


def detect_url_from_md(md: str) -> str | None:
    # IG caption md: first line is url
    first = md.splitlines()[0].strip() if md.strip() else ""
    if first.startswith("http://") or first.startswith("https://"):
        return first
    # LJ cleaned md: has "*URL*:" line in header
    m = re.search(r"^\*URL\*:\s*(https?://\S+)\s*$", md, flags=re.M)
    if m:
        return m.group(1).strip()
    return None


def iter_md_files(base: Path) -> Iterator[Path]:
    if base.exists():
        yield from sorted(base.glob("*.md"))


def add_md_dir(records: list[dict], base_dir: Path, source: str) -> None:
    for p in iter_md_files(base_dir):
        md = p.read_text(encoding="utf-8", errors="ignore")
        url = detect_url_from_md(md)

        if source == "ig":
            # IG caption md: url + blank + caption
            lines = md.splitlines()
            if not lines:
                continue
            # strip url line + optional blank
            body_lines = lines[1:]
            if body_lines and body_lines[0].strip() == "":
                body_lines = body_lines[1:]
            text = "\n".join(body_lines).strip()
            if not text:
                continue
            date = p.stem[:10] if re.match(r"\d{4}-\d{2}-\d{2}", p.stem[:10]) else None
            title = None
        else:
            date, title, text = strip_md_metadata(md)
            if not text:
                continue

        year = date[:4] if date else None
        records.append(
            {
                "source": source,
                "date": date,
                "year": year,
                "path": rel(p),
                "title": title,
                "url": url,
                "text": text,
            }
        )


def add_books(records: list[dict], root: Path) -> None:
    for fname, book_id in [("Дурге 1-2-3.txt", "durge_1-2-3"), ("Откуда ноги растут.txt", "otkuda_nogi_rastut")]:
        p = root / fname
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            continue
        records.append(
            {
                "source": "book",
                "date": None,
                "year": None,
                "path": rel(p),
                "title": book_id,
                "url": None,
                "text": text,
            }
        )


def main() -> int:
    ap = argparse.ArgumentParser(description="Build unified JSONL index of texts.")
    ap.add_argument("--out", required=True, help="Output JSONL path (e.g., data/text_index/index.jsonl)")
    ap.add_argument("--include-ig", action="store_true", help="Include Instagram captions (can be large).")
    args = ap.parse_args()

    out_path = Path(args.out)
    ensure_dir(out_path)

    records: list[dict] = []

    # Telegram exports
    add_md_dir(records, ROOT / "data/olydaily_export/posts_md", "tg_daily")
    add_md_dir(records, ROOT / "data/daily2025_export/posts_md", "tg_daily2025")
    add_md_dir(records, ROOT / "data/vi_vse_nepr_export/posts_md", "tg_literary")

    # LiveJournal cleaned
    add_md_dir(records, ROOT / "data/lj_export_clean/posts_md", "lj")

    # Instagram captions (optional; huge)
    if args.include_ig:
        add_md_dir(records, ROOT / "data/ig_captions_md", "ig")

    # Books
    add_books(records, ROOT)

    with out_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"[done] records={len(records)} out={rel(out_path)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


