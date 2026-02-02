#!/usr/bin/env python3
"""
Create a year-folder view for per-post Markdown files.

We do NOT move originals by default (so existing paths keep working).
Instead we copy into:
  <out-base>/YYYY/<filename>.md

Example:
  --input-dir data/daily2025_export/posts_md
  --out-dir   data/daily2025_export/posts_by_year
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def year_from_filename(name: str) -> str | None:
    # expects YYYY-MM-DD__...
    if len(name) < 4:
        return None
    y = name[:4]
    return y if y.isdigit() else None


def main() -> int:
    ap = argparse.ArgumentParser(description="Copy per-post .md files into year subfolders.")
    ap.add_argument("--input-dir", required=True, help="Directory containing per-post .md files.")
    ap.add_argument("--out-dir", required=True, help="Output base directory (will create YYYY subfolders).")
    ap.add_argument("--mode", choices=["copy", "move"], default="copy", help="copy (default) keeps originals; move relocates.")
    args = ap.parse_args()

    in_dir = Path(args.input_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    md_files = sorted(in_dir.glob("*.md"))
    copied = 0
    skipped = 0
    years: dict[str, int] = {}

    for p in md_files:
        y = year_from_filename(p.name)
        if not y:
            skipped += 1
            continue
        y_dir = out_dir / y
        y_dir.mkdir(parents=True, exist_ok=True)
        dest = y_dir / p.name
        years[y] = years.get(y, 0) + 1

        if args.mode == "copy":
            shutil.copy2(p, dest)
        else:
            shutil.move(str(p), str(dest))
        copied += 1

    # write a tiny readme
    readme = out_dir / "README.md"
    lines = [
        "# Posts by year",
        "",
        f"Source: `{in_dir}`",
        f"Mode: **{args.mode}**",
        "",
        "Folders:",
    ]
    for y in sorted(years.keys()):
        lines.append(f"- `{y}/` — {years[y]} files")
    if skipped:
        lines.append("")
        lines.append(f"Skipped (couldn't infer year from filename): {skipped}")
    readme.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

    print(f"[done] processed={len(md_files)} {args.mode}d={copied} skipped={skipped} out={out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



