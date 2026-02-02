#!/usr/bin/env python3
"""
Extract a clean transcript Markdown from a Telegram HTML export page
that contains voice message transcriptions inside <div class="text"> blocks.

Heuristics:
  - keep only non-empty text blocks that are not just a URL
  - drop very short blocks (likely metadata/links)
  - convert <br> to newlines and unwrap <a href="...">...</a> into the URL/text

Usage:
  python3 tools/transcripts/telegram_voice_html_to_clean_md.py \
    --input "циклы просто.html" \
    --out-md "04_ANALYSIS/cycles_motivation/10_transcript_clean.md" \
    --title "Циклы мотивации — транскрипт"
"""

from __future__ import annotations

import argparse
import html as htmllib
import re
from pathlib import Path


def html_text_to_plain(s: str) -> str:
    # <br> -> newlines
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    # links -> URL (keep visible text if no href)
    def _a(m: re.Match[str]) -> str:
        href = (m.group(1) or "").strip()
        label = (m.group(2) or "").strip()
        if href and label and label != href:
            return f"{label} ({href})"
        return href or label

    s = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', _a, s, flags=re.I | re.S)
    # drop remaining tags
    s = re.sub(r"<[^>]+>", "", s)
    s = htmllib.unescape(s)
    # normalize spaces
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def looks_like_url_only(s: str) -> bool:
    s2 = s.strip()
    return bool(re.fullmatch(r"https?://\S+", s2))


def extract_text_blocks(html: str) -> list[str]:
    # Grab all text divs inside "message default" blocks (joined or not).
    blocks = re.findall(
        r'<div class="message default clearfix(?: joined)?".*?>[\s\S]*?<div class="text">\s*([\s\S]*?)\s*</div>[\s\S]*?</div>\s*</div>',
        html,
        flags=re.I,
    )
    out: list[str] = []
    for raw in blocks:
        plain = html_text_to_plain(raw)
        if not plain:
            continue
        # drop common bot/service tails
        if "Создано ботом" in plain or "my_voice_messages_bot" in plain or "Ваше аудио довольно длинное" in plain:
            continue
        if looks_like_url_only(plain):
            continue
        # drop very short snippets (often headers/one-liners)
        if len(plain) < 80:
            continue
        out.append(plain)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract clean transcript MD from Telegram HTML export.")
    ap.add_argument("--input", required=True, help="Input .html path")
    ap.add_argument("--out-md", required=True, help="Output markdown path")
    ap.add_argument("--title", default="Транскрипт", help="Markdown title")
    args = ap.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.out_md)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    html = in_path.read_text(encoding="utf-8", errors="ignore")
    blocks = extract_text_blocks(html)

    parts: list[str] = []
    parts.append(f"# {args.title}")
    parts.append("")
    parts.append(f"Источник: `{in_path.name}`")
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("\n\n".join(blocks).strip())
    parts.append("")

    out_path.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")
    print(f"[done] blocks={len(blocks)} out={out_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


