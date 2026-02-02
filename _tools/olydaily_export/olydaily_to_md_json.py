#!/usr/bin/env python3
"""
Parse Telegram HTML export (like olydaily.html) into:
- a clean Markdown file with messages grouped by day
- a JSON file with structured messages for downstream analysis

No third-party dependencies (stdlib only).
"""

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable


DIV_OPEN_RE = re.compile(r"<div\b", re.IGNORECASE)
DIV_CLOSE_RE = re.compile(r"</div>", re.IGNORECASE)


def count_div_delta(s: str) -> int:
    return len(DIV_OPEN_RE.findall(s)) - len(DIV_CLOSE_RE.findall(s))


def clean_text_from_html(fragment: str) -> str:
    # Convert <br> into newlines
    fragment = re.sub(r"(?i)<br\s*/?>", "\n", fragment)
    # Telegram export sometimes uses <div class="text"> with embedded links, emoji, spans, etc.
    # Strip tags
    fragment = re.sub(r"(?is)<[^>]+>", "", fragment)
    # Decode HTML entities
    fragment = html.unescape(fragment)
    # Normalize whitespace
    fragment = fragment.replace("\r\n", "\n").replace("\r", "\n")
    fragment = re.sub(r"[ \t]+\n", "\n", fragment)
    fragment = re.sub(r"\n{3,}", "\n\n", fragment)
    return fragment.strip()


def parse_tg_title_datetime(title: str) -> datetime | None:
    """
    Example: '17.07.2024 16:13:52 UTC+08:00'
    """
    title = title.strip()
    if not title:
        return None
    m = re.match(r"^(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})\s+UTC([+-]\d{2}:\d{2})$", title)
    if not m:
        return None
    dt_part, off_part = m.group(1), m.group(2)
    try:
        naive = datetime.strptime(dt_part, "%d.%m.%Y %H:%M:%S")
    except ValueError:
        return None
    sign = 1 if off_part[0] == "+" else -1
    hh = int(off_part[1:3])
    mm = int(off_part[4:6])
    tz = timezone(sign * timedelta(hours=hh, minutes=mm))
    return naive.replace(tzinfo=tz)


def extract_first_group(pattern: str, s: str, flags: int = re.I | re.S) -> str | None:
    m = re.search(pattern, s, flags)
    return m.group(1) if m else None


def extract_all_links(text_html: str) -> list[str]:
    links = re.findall(r'(?i)<a[^>]+href="([^"]+)"', text_html)
    # decode entities and drop tg internal anchors
    out: list[str] = []
    seen: set[str] = set()
    for u in links:
        u = html.unescape(u).strip()
        if not u or u.startswith("#"):
            continue
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def extract_reactions(message_html: str) -> dict[str, int]:
    # Telegram export nests <span> heavily, so naive "reactions block" capture gets truncated.
    # We match reaction items directly from the message HTML.
    items = re.findall(
        r'(?is)<span class="reaction">.*?<span class="emoji">\s*(.*?)\s*</span>.*?<span class="count">\s*(\d+)\s*</span>',
        message_html,
    )
    out: dict[str, int] = {}
    for emo, cnt in items:
        emo = clean_text_from_html(emo)
        try:
            out[emo] = int(cnt)
        except ValueError:
            continue
    return out


def extract_media(message_html: str) -> dict[str, Any] | None:
    # Very lightweight: detect media title like "Photo", "Video", "Voice message", etc.
    media_title = extract_first_group(r'<div class="title bold">\s*(.*?)\s*</div>', message_html)
    if not media_title:
        return None
    media_title = clean_text_from_html(media_title)
    media_desc = extract_first_group(r'<div class="description">\s*(.*?)\s*</div>', message_html)
    media_desc = clean_text_from_html(media_desc) if media_desc else None
    media_status = extract_first_group(r'<div class="status details">\s*(.*?)\s*</div>', message_html)
    media_status = clean_text_from_html(media_status) if media_status else None
    return {"title": media_title, "description": media_desc, "status": media_status}


@dataclass
class Message:
    source: str
    message_id: str | None
    dt_title: str | None
    dt_iso: str | None
    date: str | None
    time: str | None
    from_name: str | None
    text: str
    links: list[str]
    reactions: dict[str, int]
    media: dict[str, Any] | None


def iter_message_blocks(lines: Iterable[str]) -> Iterable[str]:
    """
    Stream out full HTML blocks for each 'message default' entry.
    Skips 'message service' blocks (date separators, channel created, etc).
    """
    buf: list[str] = []
    in_msg = False
    depth = 0

    for line in lines:
        if not in_msg:
            if 'class="message default' in line:
                in_msg = True
                buf = [line]
                depth = count_div_delta(line)
            continue

        buf.append(line)
        depth += count_div_delta(line)
        if depth <= 0:
            yield "".join(buf)
            in_msg = False
            buf = []
            depth = 0


def parse_message_block(block: str, source: str) -> Message | None:
    # message id
    message_id = extract_first_group(r'id="message(\d+)"', block)

    dt_title = extract_first_group(r'class="pull_right date details"\s+title="([^"]+)"', block)
    dt = parse_tg_title_datetime(dt_title) if dt_title else None
    dt_iso = dt.isoformat() if dt else None
    date_str = dt.date().isoformat() if dt else None

    # displayed time is inside that date div
    time_disp = extract_first_group(r'class="pull_right date details"[^>]*>\s*([^<]+)\s*</div>', block)
    time_disp = time_disp.strip() if time_disp else None

    from_name = extract_first_group(r'<div class="from_name">\s*(.*?)\s*</div>', block)
    from_name = clean_text_from_html(from_name) if from_name else None

    text_html = extract_first_group(r'<div class="text">\s*(.*?)\s*</div>', block)
    links = extract_all_links(text_html) if text_html else []
    text = clean_text_from_html(text_html) if text_html else ""

    # Many messages are media-only; keep them but mark media
    media = extract_media(block)

    # Reactions
    reactions = extract_reactions(block)

    # Skip completely empty messages with no text and no media (rare)
    if not text and not media:
        return None

    return Message(
        source=source,
        message_id=message_id,
        dt_title=dt_title,
        dt_iso=dt_iso,
        date=date_str,
        time=time_disp,
        from_name=from_name,
        text=text,
        links=links,
        reactions=reactions,
        media=media,
    )


def write_markdown(messages: list[Message], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Sort by dt_iso when present; fall back to message_id
    def sort_key(m: Message):
        return (m.dt_iso or "", int(m.message_id or 0))

    messages_sorted = sorted(messages, key=sort_key)

    parts: list[str] = []
    parts.append("# Olydaily — clean export (Telegram)\n")
    current_day: str | None = None

    for m in messages_sorted:
        day = m.date or "unknown-date"
        if day != current_day:
            parts.append(f"\n## {day}\n")
            current_day = day

        header_bits: list[str] = []
        if m.time:
            header_bits.append(m.time)
        if m.from_name:
            header_bits.append(m.from_name)
        header = " — ".join(header_bits) if header_bits else "message"
        parts.append(f"### {header}\n")

        if m.media and not m.text:
            parts.append(f"[{m.media.get('title','Media')}]")
            if m.media.get("status"):
                parts.append(f"*{m.media['status']}*")
            if m.media.get("description"):
                parts.append(f"*{m.media['description']}*")
            parts.append("")
        elif m.text:
            parts.append(m.text)
            parts.append("")

        if m.links:
            parts.append("Links:")
            for u in m.links:
                parts.append(f"- {u}")
            parts.append("")

        if m.reactions:
            # compact reactions line
            rx = " ".join([f"{k}{v}" for k, v in sorted(m.reactions.items(), key=lambda kv: (-kv[1], kv[0]))])
            parts.append(f"Reactions: {rx}")
            parts.append("")

    out_path.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")


def write_json(messages: list[Message], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": "Telegram HTML export",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "messages": [asdict(m) for m in messages],
        "counts": {
            "messages_total": len(messages),
            "messages_with_text": sum(1 for m in messages if bool(m.text)),
            "messages_media_only": sum(1 for m in messages if (not m.text and m.media)),
        },
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert Telegram HTML export into clean MD + JSON (stdlib-only).")
    ap.add_argument("--input-html", required=True, help="Path to Telegram-exported HTML (e.g., olydaily.html)")
    ap.add_argument("--out-dir", required=True, help="Output directory (e.g., data/olydaily_export)")
    ap.add_argument("--source-name", default="Olymarkes Daily", help="Label stored into JSON messages")
    ap.add_argument(
        "--out-prefix",
        default=None,
        help="Output filename prefix (default: input html basename without extension).",
    )
    args = ap.parse_args()

    in_path = Path(args.input_html)
    out_dir = Path(args.out_dir)
    prefix = args.out_prefix or in_path.stem
    out_md = out_dir / f"{prefix}_clean.md"
    out_json = out_dir / f"{prefix}_messages.json"

    if not in_path.exists():
        raise SystemExit(f"Input not found: {in_path}")

    messages: list[Message] = []
    with in_path.open("r", encoding="utf-8", errors="ignore") as f:
        for block in iter_message_blocks(f):
            msg = parse_message_block(block, source=args.source_name)
            if msg:
                messages.append(msg)

    write_markdown(messages, out_md)
    write_json(messages, out_json)

    print(f"[done] messages={len(messages)} md={out_md} json={out_json}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


