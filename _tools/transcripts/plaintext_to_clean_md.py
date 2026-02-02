#!/usr/bin/env python3
"""
Convert a plain text transcript into a clean Markdown file.

Usage:
  python3 tools/transcripts/plaintext_to_clean_md.py \
    --input "Пластилин. МГПУ-исходный-текст.txt" \
    --out-md "04_ANALYSIS/cycles_motivation/30_plastilin_transcript_clean.md" \
    --title "Циклы мотивации — лекция «Пластилин МГПУ» (транскрипт)"
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # trim trailing spaces
    text = "\n".join([ln.rstrip() for ln in text.splitlines()])
    # collapse 3+ blank lines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description="Plaintext transcript to clean Markdown.")
    ap.add_argument("--input", required=True, help="Input .txt path")
    ap.add_argument("--out-md", required=True, help="Output .md path")
    ap.add_argument("--title", default="Транскрипт", help="Markdown title")
    args = ap.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.out_md)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    raw = in_path.read_text(encoding="utf-8", errors="ignore")
    body = normalize(raw)

    md = []
    md.append(f"# {args.title}")
    md.append("")
    md.append(f"Источник: `{in_path.name}`")
    md.append("")
    md.append("---")
    md.append("")
    md.append(body)
    md.append("")

    out_path.write_text("\n".join(md).strip() + "\n", encoding="utf-8")
    print(f"[done] out={out_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



