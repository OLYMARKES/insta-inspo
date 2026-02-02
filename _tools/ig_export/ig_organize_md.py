#!/usr/bin/env python3
"""
Organize Instagram per-post Markdown exports:

- Copies posts with caption length >= min_chars into a separate folder.
- Builds a topic rubricator (keyword-based, multi-label) as Markdown + JSON.

Input format (per file, as produced by ig_texts_to_md.py):
Line 1: URL
Line 2: blank
Rest : caption text (may contain newlines)
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


URL_RE = re.compile(r"^https?://")
DATE_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})(?:__(?P<ord>\d+))?\.md$")


@dataclass(frozen=True)
class Post:
    src_path: Path
    fname: str
    date: str
    ordinal: int
    url: str
    caption: str
    caption_len: int


def load_topics(topics_json_path: Optional[Path]) -> List[Dict[str, Any]]:
    """
    Topic schema:
    [
      {"id": "family", "title": "Семья", "keywords": ["сын", "мама", "папа"]},
      ...
    ]
    """
    if topics_json_path:
        data = json.loads(topics_json_path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("topics JSON must be a list")
        for t in data:
            if not isinstance(t, dict) or "id" not in t or "title" not in t or "keywords" not in t:
                raise ValueError("each topic must be an object with id/title/keywords")
            if not isinstance(t["keywords"], list):
                raise ValueError("topic.keywords must be a list")
        return data

    # Reasonable default rubricator (Russian-first; can be replaced by --topics-json).
    return [
        {"id": "kids_family", "title": "Семья / дети", "keywords": ["сын", "дочка", "дети", "ребен", "муж", "семь", "мама", "папа"]},
        {"id": "relationships", "title": "Отношения / любовь", "keywords": ["любов", "отношен", "ревную", "мужчина", "женщина", "секс", "расстав", "влюб"]},
        {"id": "work_projects", "title": "Работа / проекты", "keywords": ["работ", "проект", "клиент", "бренд", "съемк", "монтаж", "дедлайн", "команд"]},
        {"id": "creativity_writing", "title": "Творчество / письмо", "keywords": ["пишу", "текст", "книга", "стих", "музык", "песня", "сцен", "идея"]},
        {"id": "health_body", "title": "Здоровье / тело", "keywords": ["здоров", "бол", "врач", "сон", "спорт", "трен", "псих", "терап", "йог"]},
        {"id": "travel_places", "title": "Путешествия / места", "keywords": ["питер", "москва", "аэропорт", "самолет", "поезд", "отель", "город", "море", "путеше"]},
        {"id": "beauty_style", "title": "Красота / стиль", "keywords": ["космет", "крем", "волос", "макияж", "уход", "плать", "лук", "стиль"]},
        {"id": "friends_social", "title": "Друзья / тусовки", "keywords": ["друз", "тусов", "вечерин", "бар", "концерт", "вписк", "мы с"]},
        {"id": "mindset_reflection", "title": "Рефлексия / смыслы", "keywords": ["думаю", "понимаю", "страх", "стыд", "смысл", "важно", "внутри", "чувств"]},
    ]


def parse_md_post(path: Path) -> Optional[Tuple[str, str]]:
    """
    Returns (url, caption) or None if format doesn't match.
    """
    raw = path.read_text(encoding="utf-8", errors="ignore")
    lines = raw.splitlines()
    if not lines:
        return None
    url = lines[0].strip()
    if not URL_RE.match(url):
        return None

    rest = lines[1:]
    # drop at most one blank line after URL
    if rest and rest[0].strip() == "":
        rest = rest[1:]
    caption = "\n".join(rest).strip()
    return (url, caption)


def iter_posts(in_dir: Path) -> List[Post]:
    posts: List[Post] = []
    for p in sorted(in_dir.glob("*.md")):
        m = DATE_RE.match(p.name)
        if not m:
            continue
        parsed = parse_md_post(p)
        if not parsed:
            continue
        url, caption = parsed
        date = m.group("date")
        ord_raw = m.group("ord")
        ordinal = int(ord_raw) if ord_raw else 1
        cap_len = len(caption)
        posts.append(
            Post(
                src_path=p,
                fname=p.name,
                date=date,
                ordinal=ordinal,
                url=url,
                caption=caption,
                caption_len=cap_len,
            )
        )
    return posts


def normalize_text(s: str) -> str:
    s = s.casefold()
    # Keep letters/digits; collapse others to space
    s = re.sub(r"[^0-9a-zа-яё]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def classify(post: Post, topics: List[Dict[str, Any]]) -> List[str]:
    """
    Multi-label keyword match.
    """
    txt = normalize_text(post.caption)
    matched: List[str] = []
    for t in topics:
        tid = str(t["id"])
        kws = [str(x).casefold().strip() for x in (t.get("keywords") or []) if str(x).strip()]
        for kw in kws:
            # word-ish substring match on normalized text
            if kw and kw in txt:
                matched.append(tid)
                break
    return matched


def safe_topic_filename(topic_id: str) -> str:
    s = re.sub(r"[^a-z0-9_]+", "_", topic_id.casefold()).strip("_")
    return s[:80] if s else "topic"


def write_rubricator(
    posts: List[Post],
    topics: List[Dict[str, Any]],
    out_dir: Path,
    min_chars: int,
) -> None:
    topic_by_id = {t["id"]: t for t in topics}
    topic_posts: Dict[str, List[Post]] = {t["id"]: [] for t in topics}
    uncategorized: List[Post] = []

    for p in posts:
        if p.caption_len < min_chars:
            continue
        matched = classify(p, topics)
        if not matched:
            uncategorized.append(p)
            continue
        for tid in matched:
            if tid in topic_posts:
                topic_posts[tid].append(p)

    out_dir.mkdir(parents=True, exist_ok=True)
    topics_dir = out_dir / "topics"
    topics_dir.mkdir(parents=True, exist_ok=True)

    # per-topic pages
    for tid, plist in topic_posts.items():
        plist = sorted(plist, key=lambda x: (x.date, x.ordinal))
        t = topic_by_id.get(tid) or {"title": tid}
        title = t.get("title") or tid
        lines: List[str] = [f"# {title}", ""]
        for p in plist:
            snippet = p.caption.replace("\n", " ").strip()
            snippet = (snippet[:140] + "…") if len(snippet) > 141 else snippet
            lines.append(f"- **{p.date}** — [{p.url}]({p.url}) — {snippet}")
        (topics_dir / f"{safe_topic_filename(str(tid))}.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    # main rubricator.md
    rub_lines: List[str] = []
    rub_lines.append("# IG рубрикатор по темам (посты ≥ {} символов)".format(min_chars))
    rub_lines.append("")
    rub_lines.append(f"Источник: `{posts[0].src_path.parent}`" if posts else "")
    rub_lines.append("")

    # summary table-ish
    rub_lines.append("## Сводка")
    rub_lines.append("")
    rub_lines.append(f"- **Всего .md файлов**: {len(posts)}")
    rub_lines.append(f"- **Постов ≥ {min_chars}**: {sum(1 for p in posts if p.caption_len >= min_chars)}")
    rub_lines.append("")

    # topics sorted by count desc
    topic_counts: List[Tuple[str, int]] = [(tid, len(plist)) for tid, plist in topic_posts.items()]
    topic_counts.sort(key=lambda x: x[1], reverse=True)
    rub_lines.append("## Темы")
    rub_lines.append("")
    for tid, cnt in topic_counts:
        title = (topic_by_id.get(tid) or {}).get("title") or tid
        file_name = f"topics/{safe_topic_filename(str(tid))}.md"
        rub_lines.append(f"- **{title}** ({cnt}) — `{file_name}`")
    if uncategorized:
        rub_lines.append(f"- **Без темы / прочее** ({len(uncategorized)})")
    rub_lines.append("")

    (out_dir / "rubricator.md").write_text("\n".join([l for l in rub_lines if l is not None]).rstrip() + "\n", encoding="utf-8")

    # rubricator.json (machine-friendly)
    data = {
        "min_chars": min_chars,
        "total_files": len(posts),
        "total_long": sum(1 for p in posts if p.caption_len >= min_chars),
        "topics": [
            {
                "id": tid,
                "title": (topic_by_id.get(tid) or {}).get("title") or tid,
                "count": len(topic_posts.get(tid) or []),
                "posts": [
                    {"date": p.date, "ordinal": p.ordinal, "url": p.url, "file": p.fname, "caption_len": p.caption_len}
                    for p in sorted((topic_posts.get(tid) or []), key=lambda x: (x.date, x.ordinal))
                ],
            }
            for tid, _cnt in topic_counts
        ],
        "uncategorized": [
            {"date": p.date, "ordinal": p.ordinal, "url": p.url, "file": p.fname, "caption_len": p.caption_len}
            for p in sorted(uncategorized, key=lambda x: (x.date, x.ordinal))
        ],
    }
    (out_dir / "rubricator.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_long_posts(posts: List[Post], out_dir: Path, min_chars: int, overwrite: bool) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for p in posts:
        if p.caption_len < min_chars:
            continue
        dst = out_dir / p.fname
        if dst.exists() and not overwrite:
            continue
        shutil.copy2(p.src_path, dst)
        copied += 1
    return copied


def main() -> int:
    ap = argparse.ArgumentParser(description="Organize IG per-post Markdown exports by length and topics.")
    ap.add_argument("--in-md-dir", required=True, help="Directory with per-post .md files (URL + caption).")
    ap.add_argument("--out-dir", required=True, help="Base output directory.")
    ap.add_argument("--min-chars", type=int, default=200, help="Minimum caption length (characters) to include.")
    ap.add_argument("--topics-json", default="", help="Path to topics JSON config (optional).")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")
    args = ap.parse_args()

    in_dir = Path(args.in_md_dir)
    out_dir = Path(args.out_dir)
    min_chars = int(args.min_chars)
    overwrite = bool(args.overwrite)

    topics_path = Path(args.topics_json) if args.topics_json else None
    topics = load_topics(topics_path)

    posts = iter_posts(in_dir)
    if not posts:
        print("[warn] no posts found in input dir")
        out_dir.mkdir(parents=True, exist_ok=True)
        return 0

    long_dir = out_dir / f"long_{min_chars}_md"
    copied = copy_long_posts(posts, long_dir, min_chars=min_chars, overwrite=overwrite)

    rubric_dir = out_dir / "rubricator"
    write_rubricator(posts, topics, rubric_dir, min_chars=min_chars)

    print(f"[done] input_files={len(posts)} long_copied={copied} out={out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


