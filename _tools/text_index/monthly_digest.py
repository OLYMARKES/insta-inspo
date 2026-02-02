#!/usr/bin/env python3
"""
Build a monthly digest from index_with_ig.jsonl (and original source files for richer metadata).

Output: Markdown + JSON summary.

Usage:
  python3 tools/text_index/monthly_digest.py \
    --index data/text_index/index_with_ig.jsonl \
    --month 2025-01 \
    --sources ig,tg_daily,tg_daily2025 \
    --out-md data/digests/2025-01_digest_ig_tg.md \
    --out-json data/digests/2025-01_digest_ig_tg.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)


def ensure_dir(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


STOP_RU = set(
    "и а но что это в во на по к ко у о об про за для из от до как я мы ты вы он она они оно мне меня моя мой мои тут там вот ну да нет уже еще ещё с со без чтобы если то ли же бы быть есть были будет буду очень просто потом когда потому тоже только уже вообще".split()
)
STOP_EN = set("the a an and or but to of in on at for with is are was were be been i you we they he she it my your our".split())
STOP = STOP_RU | STOP_EN


def tokenize(text: str) -> list[str]:
    toks = [t.lower() for t in re.findall(r"[A-Za-zА-Яа-яЁё0-9]+(?:[-'][A-Za-zА-Яа-яЁё0-9]+)?", text)]
    toks = [t for t in toks if t not in STOP and len(t) >= 3]
    return toks


def sentences(text: str) -> list[str]:
    t = re.sub(r"\s+", " ", text).strip()
    if not t:
        return []
    # rough splitter; keeps punctuation
    parts = re.split(r"(?<=[.!?…])\s+", t)
    return [p.strip() for p in parts if p.strip()]


def parse_tg_reactions_from_md(md_path: Path) -> dict[str, int]:
    # our per-post tg md ends with line: "Reactions: ❤10 🔥2"
    try:
        txt = md_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {}
    m = re.search(r"^Reactions:\s*(.+)$", txt, flags=re.M)
    if not m:
        return {}
    rx = m.group(1).strip()
    out: dict[str, int] = {}
    for emo, cnt in re.findall(r"(\S+?)(\d+)", rx):
        try:
            out[emo] = int(cnt)
        except ValueError:
            continue
    return out


@dataclass
class Item:
    source: str
    date: str
    path: str
    url: str | None
    title: str | None
    text: str
    reactions: dict[str, int]

    @property
    def reactions_total(self) -> int:
        return sum(self.reactions.values()) if self.reactions else 0


def load_items(index_path: Path, month: str, sources: set[str]) -> list[Item]:
    items: list[Item] = []
    with index_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue

            src = rec.get("source")
            if src not in sources:
                continue
            date = rec.get("date")
            if not isinstance(date, str) or not date.startswith(month + "-"):
                continue

            path = rec.get("path") or ""
            text = rec.get("text") or ""
            if not isinstance(text, str) or not text.strip():
                continue

            url = rec.get("url")
            url = url if isinstance(url, str) and url.strip() else None
            title = rec.get("title")
            title = title if isinstance(title, str) and title.strip() else None

            reactions: dict[str, int] = {}
            # for tg sources, read reactions from original md file (not from index)
            if src.startswith("tg_") and path.endswith(".md"):
                md_path = ROOT / path
                reactions = parse_tg_reactions_from_md(md_path)

            items.append(Item(source=src, date=date, path=path, url=url, title=title, text=text.strip(), reactions=reactions))
    return sorted(items, key=lambda i: (i.date, i.source, i.path))


def pick_quotes(items: list[Item], limit: int = 10) -> list[dict[str, Any]]:
    # pick best sentences by length + presence of punctuation; de-dupe
    candidates: list[tuple[int, dict[str, Any]]] = []
    seen: set[str] = set()
    for it in items:
        for s in sentences(it.text):
            if len(s) < 90 or len(s) > 240:
                continue
            key = s.lower()
            if key in seen:
                continue
            seen.add(key)
            score = len(s)
            if it.reactions_total:
                score += min(4000, it.reactions_total) // 20
            candidates.append(
                (
                    score,
                    {
                        "quote": s,
                        "source": it.source,
                        "date": it.date,
                        "path": it.path,
                        "url": it.url,
                        "reactions_total": it.reactions_total,
                    },
                )
            )
    candidates.sort(key=lambda x: x[0], reverse=True)
    return [c[1] for c in candidates[:limit]]


def summarize(items: list[Item]) -> dict[str, Any]:
    by_source: dict[str, list[Item]] = defaultdict(list)
    for it in items:
        by_source[it.source].append(it)

    kw_all = Counter()
    kw_by_source: dict[str, Counter] = {}
    for src, lst in by_source.items():
        c = Counter()
        for it in lst:
            c.update(tokenize(it.text))
        kw_by_source[src] = c
        kw_all.update(c)

    # highlights: top by reactions (tg) and top by length (ig)
    tg = [it for it in items if it.source.startswith("tg_")]
    ig = [it for it in items if it.source == "ig"]

    top_tg = sorted(tg, key=lambda i: (i.reactions_total, len(i.text)), reverse=True)[:8]
    top_ig = sorted(ig, key=lambda i: len(i.text), reverse=True)[:8]

    return {
        "counts": {
            "total": len(items),
            "by_source": {k: len(v) for k, v in sorted(by_source.items())},
        },
        "keywords": {
            "all": kw_all.most_common(40),
            "by_source": {k: v.most_common(30) for k, v in sorted(kw_by_source.items())},
        },
        "highlights": {
            "top_tg": [
                {
                    "date": it.date,
                    "source": it.source,
                    "path": it.path,
                    "reactions_total": it.reactions_total,
                    "preview": " ".join(it.text.split())[:320] + ("…" if len(it.text) > 320 else ""),
                }
                for it in top_tg
            ],
            "top_ig": [
                {
                    "date": it.date,
                    "source": it.source,
                    "path": it.path,
                    "url": it.url,
                    "preview": " ".join(it.text.split())[:320] + ("…" if len(it.text) > 320 else ""),
                }
                for it in top_ig
            ],
        },
        "quotes": pick_quotes(items, limit=10),
    }


def write_md(month: str, sources: list[str], items: list[Item], summary: dict[str, Any], out_path: Path) -> None:
    ensure_dir(out_path)
    parts: list[str] = []
    parts.append(f"# Дайджест месяца — {month}")
    parts.append("")
    parts.append(f"Источники: {', '.join(sources)}")
    parts.append("")
    parts.append(f"Всего текстов: **{summary['counts']['total']}**")
    parts.append("")
    parts.append("## Количество по источникам")
    for src, n in summary["counts"]["by_source"].items():
        parts.append(f"- **{src}**: {n}")

    parts.append("")
    parts.append("## Ключевые слова месяца (приблизительно)")
    parts.append(", ".join([w for w, _ in summary["keywords"]["all"][:25]]))

    parts.append("")
    parts.append("## Хайлайты (по весу/длине)")
    parts.append("")
    if summary["highlights"]["top_tg"]:
        parts.append("### Telegram (топ по реакциям)")
        for h in summary["highlights"]["top_tg"]:
            parts.append(f"- **{h['date']}** (`{h['source']}`) — реакции≈{h['reactions_total']}: {h['preview']}")
        parts.append("")
    if summary["highlights"]["top_ig"]:
        parts.append("### Instagram (топ по длине)")
        for h in summary["highlights"]["top_ig"]:
            url = h.get("url") or ""
            url_part = f" — {url}" if url else ""
            parts.append(f"- **{h['date']}** (`{h['source']}`){url_part}: {h['preview']}")
        parts.append("")

    parts.append("## Цитаты месяца (черновая выборка)")
    for q in summary["quotes"]:
        meta = f"{q['date']} / {q['source']}"
        if q.get("url"):
            meta += f" / {q['url']}"
        parts.append(f"- “{q['quote']}”  \n  _{meta}_")

    parts.append("")
    parts.append("## Список источников (для проверки)")
    for it in items:
        url = f" — {it.url}" if it.url else ""
        parts.append(f"- {it.date} (`{it.source}`): `{it.path}`{url}")

    out_path.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build monthly digest from unified index.")
    ap.add_argument("--index", required=True, help="Path to index_with_ig.jsonl")
    ap.add_argument("--month", required=True, help="Month in YYYY-MM format (e.g., 2025-01)")
    ap.add_argument("--sources", required=True, help="Comma-separated sources, e.g. ig,tg_daily,tg_daily2025")
    ap.add_argument("--out-md", required=True, help="Output markdown path")
    ap.add_argument("--out-json", required=True, help="Output json path")
    args = ap.parse_args()

    index_path = Path(args.index)
    month = args.month.strip()
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    src_set = set(sources)

    items = load_items(index_path, month, src_set)
    summary = summarize(items)

    out_md = Path(args.out_md)
    out_json = Path(args.out_json)
    ensure_dir(out_md)
    ensure_dir(out_json)

    write_md(month, sources, items, summary, out_md)
    out_json.write_text(json.dumps({"month": month, "sources": sources, "summary": summary}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[done] month={month} items={len(items)} md={rel(out_md)} json={rel(out_json)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



