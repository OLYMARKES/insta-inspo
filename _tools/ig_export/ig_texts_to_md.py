#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Optional

import ijson


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def safe_date_from_timestamp(ts: Optional[str]) -> Optional[str]:
    if not ts:
        return None
    # examples: "2025-12-15T07:28:53.000Z"
    d = ts[:10]
    return d if DATE_RE.match(d) else None


def build_path(out_dir: Path, date_str: str, ordinal: int) -> Path:
    """
    Deterministic naming:
    - first post of the day: YYYY-MM-DD.md
    - second: YYYY-MM-DD__2.md
    - ...
    """
    if ordinal <= 1:
        return out_dir / f"{date_str}.md"
    return out_dir / f"{date_str}__{ordinal}.md"


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract Instagram post captions into per-post Markdown files.")
    ap.add_argument("--input", required=True, help="Path to dataset JSON (array of post objects).")
    ap.add_argument("--out-dir", required=True, help="Output directory for .md files.")
    ap.add_argument("--limit", type=int, default=0, help="Limit number of posts (0 = no limit).")
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing .md files (recommended when regenerating).",
    )
    args = ap.parse_args()

    in_path = Path(args.input)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    limit = args.limit if args.limit and args.limit > 0 else None

    written = 0
    skipped_no_caption = 0
    skipped_no_date = 0
    skipped_no_url = 0
    per_day_counter: dict[str, int] = {}

    with in_path.open("rb") as f:
        for obj in ijson.items(f, "item"):
            if limit and written >= limit:
                break

            if not isinstance(obj, dict):
                continue

            caption = obj.get("caption")
            if not isinstance(caption, str) or not caption.strip():
                skipped_no_caption += 1
                continue

            date_str = safe_date_from_timestamp(obj.get("timestamp"))
            if not date_str:
                skipped_no_date += 1
                continue

            url = obj.get("url")
            if not isinstance(url, str) or not url.strip():
                skipped_no_url += 1
                continue

            per_day_counter[date_str] = per_day_counter.get(date_str, 0) + 1
            ordinal = per_day_counter[date_str]

            out_path = build_path(out_dir, date_str, ordinal)
            if out_path.exists() and not args.overwrite:
                # still count it as "written" for progress alignment? no — skip.
                continue

            # Requirement updated: add URL line, then only text.
            out_path.write_text(url.strip() + "\n\n" + caption.rstrip() + "\n", encoding="utf-8")
            written += 1

            if written % 200 == 0:
                print(f"[progress] written {written}", flush=True)

    summary = (
        f"[done] written={written}, skipped_no_caption={skipped_no_caption}, skipped_no_date={skipped_no_date}, skipped_no_url={skipped_no_url}"
    )
    print(summary, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


