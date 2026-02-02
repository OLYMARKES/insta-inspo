#!/usr/bin/env python3
"""
Convert olydaily_messages.json (produced by olydaily_to_md_json.py) into per-post Markdown files.

Filename format:
  YYYY-MM-DD__<message_id>__<topic_slug>.md

Where topic_slug is derived from the first meaningful words of the message text.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RU_STOPWORDS = {
    "и",
    "а",
    "но",
    "что",
    "это",
    "в",
    "во",
    "на",
    "по",
    "к",
    "ко",
    "у",
    "о",
    "об",
    "про",
    "за",
    "для",
    "из",
    "от",
    "до",
    "как",
    "я",
    "мы",
    "ты",
    "вы",
    "он",
    "она",
    "они",
    "оно",
    "мне",
    "меня",
    "моя",
    "мой",
    "мои",
    "тут",
    "там",
    "вот",
    "ну",
    "да",
    "нет",
    "уже",
    "еще",
    "ещё",
    "с",
    "со",
    "без",
    "чтобы",
    "если",
    "то",
    "ли",
    "же",
    "бы",
    "быть",
    "есть",
    "были",
    "будет",
    "буду",
    "очень",
    "просто",
}


def safe_slug(s: str, max_len: int = 80) -> str:
    s = s.strip().lower()
    # allow latin, cyrillic, digits, underscore, dash
    s = re.sub(r"[^0-9a-zа-яё_-]+", "_", s, flags=re.IGNORECASE)
    s = re.sub(r"_+", "_", s).strip("_")
    if not s:
        return "no_topic"
    return s[:max_len].strip("_") or "no_topic"


def topic_slug_from_text(text: str, words: int = 7) -> str:
    # take first non-empty line (most "topic-like")
    first = ""
    for line in text.splitlines():
        line = line.strip()
        if line:
            first = line
            break
    if not first:
        return "no_topic"

    tokens = re.findall(r"[0-9A-Za-zА-Яа-яЁё]+(?:[-'][0-9A-Za-zА-Яа-яЁё]+)?", first)
    picked: list[str] = []
    for t in tokens:
        low = t.lower()
        if low in RU_STOPWORDS:
            continue
        picked.append(low)
        if len(picked) >= words:
            break

    if not picked:
        picked = [t.lower() for t in tokens[:words]] or ["no_topic"]

    return safe_slug("_".join(picked))


def next_available_path(out_dir: Path, base_name: str) -> Path:
    i = 1
    while True:
        name = f"{base_name}{'' if i == 1 else f'__{i}'}.md"
        p = out_dir / name
        if not p.exists():
            return p
        i += 1


@dataclass
class Msg:
    message_id: str
    dt_iso: str | None
    date: str | None
    time: str | None
    from_name: str | None
    text: str
    links: list[str]
    reactions: dict[str, int]
    media: dict[str, Any] | None


def load_messages(json_path: Path) -> list[Msg]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    msgs: list[Msg] = []
    for m in data.get("messages", []):
        text = m.get("text") or ""
        # we only create "posts" for messages with text
        if not isinstance(text, str) or not text.strip():
            continue
        mid = str(m.get("message_id") or "").strip()
        if not mid:
            continue
        msgs.append(
            Msg(
                message_id=mid,
                dt_iso=m.get("dt_iso"),
                date=m.get("date"),
                time=m.get("time"),
                from_name=m.get("from_name"),
                text=text.strip(),
                links=m.get("links") or [],
                reactions=m.get("reactions") or {},
                media=m.get("media"),
            )
        )
    return msgs


def write_index_tsv(rows: list[tuple[str, Msg]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        f.write("filename\tdate\ttime\tdt_iso\tpreview\n")
        for filename, m in rows:
            preview = m.text.replace("\n", " ").strip()
            if len(preview) > 160:
                preview = preview[:157] + "…"
            f.write(
                f"{filename}\t{m.date or ''}\t{m.time or ''}\t{m.dt_iso or ''}\t{preview}\n"
            )


def main() -> int:
    ap = argparse.ArgumentParser(description="Create per-post Markdown files from olydaily_messages.json.")
    ap.add_argument("--input-json", required=True, help="Path to olydaily_messages.json")
    ap.add_argument("--out-dir", required=True, help="Output directory for per-post .md files")
    ap.add_argument("--slug-words", type=int, default=7, help="How many words to use for topic slug")
    args = ap.parse_args()

    in_path = Path(args.input_json)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    msgs = load_messages(in_path)

    # Sort stable: dt_iso then id
    def sort_key(m: Msg):
        return (m.dt_iso or "", int(m.message_id))

    msgs = sorted(msgs, key=sort_key)

    index_rows: list[tuple[str, Msg]] = []
    written = 0

    for m in msgs:
        date = m.date or (m.dt_iso[:10] if m.dt_iso else "unknown-date")
        topic = topic_slug_from_text(m.text, words=max(1, args.slug_words))
        base_name = f"{date}__{m.message_id}__{topic}"
        out_path = next_available_path(out_dir, base_name)

        parts: list[str] = []
        # Minimal header, like IG/LJ style
        parts.append(f"# {date} — {topic.replace('_', ' ')}")
        if m.dt_iso:
            parts.append(f"*Datetime*: {m.dt_iso}")
        if m.from_name:
            parts.append(f"*From*: {m.from_name}")
        parts.append(f"*Message ID*: {m.message_id}")
        parts.append("")
        parts.append(m.text.rstrip())
        parts.append("")

        if m.links:
            parts.append("Links:")
            for u in m.links:
                parts.append(f"- {u}")
            parts.append("")

        if m.reactions:
            rx = " ".join([f"{k}{v}" for k, v in sorted(m.reactions.items(), key=lambda kv: (-kv[1], kv[0]))])
            parts.append(f"Reactions: {rx}")
            parts.append("")

        out_path.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")
        index_rows.append((out_path.name, m))
        written += 1

    write_index_tsv(index_rows, out_dir.parent / "index.tsv")
    print(f"[done] posts_written={written} out_dir={out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



