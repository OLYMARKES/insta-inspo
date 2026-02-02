#!/usr/bin/env python3
"""
Year digest builder: "3 lines" + best-of scenes from IG+TG.

Lines:
  1) love_relationships
  2) body_nervous_system
  3) work_creativity

Scenes = multi-sentence fragments (not single quotes), chosen by relevance + (TG reactions).

Usage:
  python3 tools/text_index/year_digest.py \
    --index data/text_index/index_with_ig.jsonl \
    --year 2025 \
    --sources ig,tg_daily,tg_daily2025 \
    --out-md data/digests/2025_year_3lines_bestof_ig_tg.md \
    --out-json data/digests/2025_year_3lines_bestof_ig_tg.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


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


LINE_KEYWORDS: dict[str, dict[str, list[str]]] = {
    "love_relationships": {
        "name": "Любовь / отношения",
        "keywords": [
            "любов", "отношен", "партнер", "партнёр", "поли", "ревност", "выбра",
            "свидан", "краш", "расстав", "влюб", "семья", "близост", "секс", "тантр",
            "честност", "верност", "compersion",
            "дима", "вадим", "педро",
        ],
    },
    "body_nervous_system": {
        "name": "Тело / нервная система",
        "keywords": [
            "тело", "нерв", "сон", "устал", "тревог", "паник", "серф", "сёрф", "йога",
            "баня", "лед", "ice", "bath", "фридайв", "плав", "боль", "врач", "болел",
            "здоров", "питание", "тренир", "пмс", "гормон", "адреналин",
        ],
    },
    "work_creativity": {
        "name": "Работа / творчество",
        "keywords": [
            "работ", "проект", "запуск", "курс", "sekta", "секта", "програм",
            "альбом", "песн", "текст", "студ", "репет", "концерт", "сцена", "тур",
            "подкаст", "рилс", "контент", "публикац", "инста", "телеграм", "аудитор",
            "идея", "пишу", "писать",
        ],
    },
}


def tokenize(text: str) -> list[str]:
    toks = [t.lower() for t in re.findall(r"[A-Za-zА-Яа-яЁё0-9]+(?:[-'][A-Za-zА-Яа-яЁё0-9]+)?", text)]
    toks = [t for t in toks if t not in STOP and len(t) >= 3]
    return toks


def split_paragraphs(text: str) -> list[str]:
    # keep paragraphs; collapse extra whitespace inside
    parts = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    return parts


def parse_tg_reactions_from_md(md_path: Path) -> int:
    try:
        txt = md_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return 0
    m = re.search(r"^Reactions:\s*(.+)$", txt, flags=re.M)
    if not m:
        return 0
    rx = m.group(1).strip()
    total = 0
    for _, cnt in re.findall(r"(\S+?)(\d+)", rx):
        try:
            total += int(cnt)
        except ValueError:
            pass
    return total


@dataclass
class Item:
    source: str
    date: str
    year: str
    path: str
    url: str | None
    title: str | None
    text: str
    tg_reactions_total: int


def load_items(index_path: Path, year: str, sources: set[str]) -> list[Item]:
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
            d = rec.get("date")
            y = rec.get("year")
            if y != year:
                continue
            if not isinstance(d, str) or not isinstance(y, str):
                continue

            text = rec.get("text") or ""
            if not isinstance(text, str) or not text.strip():
                continue

            path = rec.get("path") or ""
            url = rec.get("url")
            url = url if isinstance(url, str) and url.strip() else None
            title = rec.get("title")
            title = title if isinstance(title, str) and title.strip() else None

            tg_rx = 0
            if src.startswith("tg_") and path.endswith(".md"):
                tg_rx = parse_tg_reactions_from_md(ROOT / path)

            items.append(Item(src, d, y, path, url, title, text.strip(), tg_rx))
    return sorted(items, key=lambda i: (i.date, i.source, i.path))


def keyword_score(text: str, keywords: list[str]) -> int:
    t = text.lower()
    score = 0
    for k in keywords:
        if k in t:
            score += 1
    return score


def choose_scenes(items: list[Item], line_key: str, limit: int = 8) -> list[dict[str, Any]]:
    kw = LINE_KEYWORDS[line_key]["keywords"]
    candidates: list[tuple[int, dict[str, Any]]] = []
    seen: set[str] = set()

    for it in items:
        # paragraphs are better "scenes" than single sentences
        for p in split_paragraphs(it.text):
            # skip tiny fragments
            if len(p) < 280 or len(p) > 1200:
                continue
            # require multi-sentence-ish
            if len(re.findall(r"[.!?…]", p)) < 2:
                continue
            # relevance
            kscore = keyword_score(p, kw)
            if kscore == 0:
                continue

            norm = re.sub(r"\s+", " ", p).strip().lower()
            # de-dupe by start
            sig = norm[:220]
            if sig in seen:
                continue
            seen.add(sig)

            score = kscore * 10 + min(5000, it.tg_reactions_total) // 25 + min(1200, len(p)) // 40

            candidates.append(
                (
                    score,
                    {
                        "scene": p.strip(),
                        "date": it.date,
                        "source": it.source,
                        "path": it.path,
                        "url": it.url,
                        "tg_reactions_total": it.tg_reactions_total,
                    },
                )
            )

    candidates.sort(key=lambda x: x[0], reverse=True)
    return [c[1] for c in candidates[:limit]]


def best_of_scenes(items: list[Item], limit: int = 25) -> list[dict[str, Any]]:
    # pick top scenes across all lines by "scene quality"
    candidates: list[tuple[int, dict[str, Any]]] = []
    seen: set[str] = set()

    all_kw = []
    for lk in LINE_KEYWORDS.values():
        all_kw.extend(lk["keywords"])

    for it in items:
        for p in split_paragraphs(it.text):
            if len(p) < 280 or len(p) > 1200:
                continue
            if len(re.findall(r"[.!?…]", p)) < 2:
                continue

            # must have at least 1 thematic hit in any line
            kscore = keyword_score(p, all_kw)
            if kscore == 0:
                continue

            norm = re.sub(r"\s+", " ", p).strip().lower()
            sig = norm[:220]
            if sig in seen:
                continue
            seen.add(sig)

            score = kscore * 6 + min(5000, it.tg_reactions_total) // 20 + min(1200, len(p)) // 35

            candidates.append(
                (
                    score,
                    {
                        "scene": p.strip(),
                        "date": it.date,
                        "source": it.source,
                        "path": it.path,
                        "url": it.url,
                        "tg_reactions_total": it.tg_reactions_total,
                    },
                )
            )

    candidates.sort(key=lambda x: x[0], reverse=True)
    return [c[1] for c in candidates[:limit]]


def summarize_months(items: list[Item]) -> dict[str, int]:
    c = Counter(i.date[:7] for i in items if i.date and len(i.date) >= 7)
    return dict(sorted(c.items()))


def build_digest(items: list[Item]) -> dict[str, Any]:
    by_source = Counter(i.source for i in items)
    months = summarize_months(items)

    lines_out: dict[str, Any] = {}
    for lk in LINE_KEYWORDS.keys():
        lines_out[lk] = {
            "name": LINE_KEYWORDS[lk]["name"],
            "scenes": choose_scenes(items, lk, limit=8),
        }

    digest = {
        "counts": {"total": len(items), "by_source": dict(by_source), "months": months},
        "lines": lines_out,
        "best_of_scenes": best_of_scenes(items, limit=25),
    }
    return digest


def write_md(year: str, sources: list[str], digest: dict[str, Any], out_path: Path) -> None:
    ensure_dir(out_path)
    parts: list[str] = []
    parts.append(f"# Итоги {year} — 3 линии + best‑of сцены (IG+TG)")
    parts.append("")
    parts.append(f"Источники: {', '.join(sources)}")
    parts.append("")
    parts.append(f"Текстов в выборке: **{digest['counts']['total']}**")
    parts.append("")

    parts.append("## Покрытие по месяцам (по тем текстам, что есть в базе)")
    for m, n in digest["counts"]["months"].items():
        parts.append(f"- **{m}**: {n}")

    parts.append("")
    parts.append("## 3 линии года")
    for lk, info in digest["lines"].items():
        parts.append("")
        parts.append(f"### {info['name']}")
        for s in info["scenes"]:
            meta = f"{s['date']} / {s['source']}"
            if s.get("tg_reactions_total"):
                meta += f" / реакции≈{s['tg_reactions_total']}"
            if s.get("url"):
                meta += f" / {s['url']}"
            parts.append(f"- **{meta}**")
            parts.append(f"  {s['scene']}")
            parts.append("")

    parts.append("## Best‑of сцены года (смешанный список)")
    for s in digest["best_of_scenes"]:
        meta = f"{s['date']} / {s['source']}"
        if s.get("tg_reactions_total"):
            meta += f" / реакции≈{s['tg_reactions_total']}"
        if s.get("url"):
            meta += f" / {s['url']}"
        parts.append(f"- **{meta}**")
        parts.append(f"  {s['scene']}")
        parts.append("")

    out_path.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build year digest (3 lines + best-of scenes).")
    ap.add_argument("--index", required=True, help="Path to index_with_ig.jsonl")
    ap.add_argument("--year", required=True, help="Year YYYY")
    ap.add_argument("--sources", required=True, help="Comma-separated sources (e.g. ig,tg_daily,tg_daily2025)")
    ap.add_argument("--out-md", required=True, help="Output markdown path")
    ap.add_argument("--out-json", required=True, help="Output json path")
    args = ap.parse_args()

    year = args.year.strip()
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    src_set = set(sources)

    items = load_items(Path(args.index), year, src_set)
    digest = build_digest(items)

    out_md = Path(args.out_md)
    out_json = Path(args.out_json)
    ensure_dir(out_md)
    ensure_dir(out_json)

    write_md(year, sources, digest, out_md)
    out_json.write_text(json.dumps({"year": year, "sources": sources, "digest": digest}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[done] year={year} items={len(items)} md={rel(out_md)} json={rel(out_json)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



