#!/usr/bin/env python3
"""
Extract Instagram posts about addiction / sobriety (and optionally a phrase like "длина с чего")
from the unified IG JSONL index.

Input:  data/text_index/index_with_ig.jsonl
Output: a single Markdown file with matched posts.

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def norm(s: str) -> str:
    # normalize a bit for Russian searches
    return (s or "").replace("Ё", "Е").replace("ё", "е")


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class Match:
    date: str | None
    path: str
    url: str | None
    text: str
    reasons: list[str]
    tier: str  # "primary" | "secondary"


def infer_date(rec: dict) -> str | None:
    d = rec.get("date")
    if isinstance(d, str) and DATE_RE.match(d):
        return d
    path = rec.get("path") or ""
    if isinstance(path, str) and len(path) >= 10 and DATE_RE.match(path[-14:-4]):
        # not expected, but keep safe
        return path[-14:-4]
    if isinstance(path, str) and len(path) >= 10 and DATE_RE.match(path.split("/")[-1][:10]):
        return path.split("/")[-1][:10]
    return None


def build_patterns() -> dict[str, re.Pattern]:
    # Core themes: addiction / sobriety / substance use (RU, best-effort)
    addiction = re.compile(
        r"("
        r"\bзависим\w*"
        r"|созавис\w*"
        r"|аддикц\w*"
        r")",
        flags=re.IGNORECASE,
    )

    sobriety = re.compile(
        r"("
        r"\bтрезв\w*"
        r"|\bвоздержан\w*"
        r"|не\s+пью\b"
        r"|без\s+алкогол\w*"
        r"|сух\w+\s+закон"
        r"|я\s+больше\s+не\s+пью\b"
        r"|год\s+трезвост\w*"
        r")",
        flags=re.IGNORECASE,
    )

    substances = re.compile(
        r"("
        r"\bалкогол\w*"
        r"|выпив\w*"
        r"|похмел\w*"
        r"|опьян\w*"
        r"|пьян\w*"
        r"|запо\w*"
        r"|перепил\w*"
        r"|бух\w*"
        r"|наркот\w*"
        r"|употребля\w*"  # ambiguous, but often used in this context
        r"|рехаб\w*"
        r"|реабилит\w*"
        r"|детокс\w*"
        r"|12\s*шаг\w*"
        r"|двенадцат\w+\s+шаг\w*"
        r"|\bа\.?\s?а\.?\b"  # АА / A.A.
        r"|срыв\w*"
        r"|чист\w+\s+(\d+|дн|дня|дней|мес|месяц|года|лет)\b"
        r"|марихуан\w*"
        r"|травк\w*"
        r"|гашиш\w*"
        r"|кокс\w*"
        r"|амфет\w*"
        r"|героин\w*"
        r"|опиат\w*"
        r"|спайс\w*"
        r"|сигарет\w*"
        r"|никотин\w*"
        r"|вейп\w*"
        r"|\bкурю\b|\bкурил\b|\bкурила\b|\bкурить\b"
        r")",
        flags=re.IGNORECASE,
    )

    # Special phrase bucket (user wording): "длина с чего"
    length_phrase = re.compile(
        r"(длинн?а\W{0,30}с\W*чего|с\W*чего\W{0,30}длинн?а)",
        flags=re.IGNORECASE,
    )

    return {
        "addiction": addiction,
        "sobriety": sobriety,
        "substances": substances,
        "length_phrase": length_phrase,
    }


def classify_tier(text_n: str, reasons: list[str]) -> str:
    """
    primary = clearly about addiction/sobriety/recovery
    secondary = casual mention / metaphor / joke (still kept, but separated)
    """
    if "addiction" in reasons or "sobriety" in reasons or "length_phrase" in reasons:
        return "primary"

    # Substances-only: separate heavy/clinical terms vs casual/metaphoric usage.
    strong_substance = re.search(
        r"("
        r"алкоголизм\w*"
        r"|запо\w*"
        r"|похмел\w*"
        r"|перепил\w*"
        r"|срыв\w*"
        r"|употребля\w*"
        r"|рехаб\w*"
        r"|реабилит\w*"
        r"|12\s*шаг\w*"
        r"|двенадцат\w+\s+шаг\w*"
        r"|\bа\.?\s?а\.?\b"
        r")",
        text_n,
        flags=re.IGNORECASE,
    )
    return "primary" if strong_substance else "secondary"


def is_false_positive(text_n: str, reasons: list[str]) -> bool:
    # Filter obvious non-theme usages to reduce noise.
    # If the only signal is "алкоголичка" as clothing ("майка-алкоголичка"), ignore.
    if any(r in reasons for r in ["substances", "sobriety", "addiction"]):
        # if we already have strong reasons, keep unless it's clearly only a clothing phrase
        pass
    only_substances = reasons == ["substances"]
    if only_substances:
        if re.search(r"майк\w*\W*алкоголичк\w*", text_n, flags=re.IGNORECASE):
            # keep only if there are other substance markers besides this phrase
            tmp = re.sub(r"майк\w*\W*алкоголичк\w*", "", text_n, flags=re.IGNORECASE)
            if not re.search(r"\bалкогол\w*|\bпьян\w*|\bпью\b|\bбух\w*", tmp, flags=re.IGNORECASE):
                return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract IG posts about addiction/sobriety into one Markdown file.")
    ap.add_argument("--index", default="data/text_index/index_with_ig.jsonl", help="Path to index_with_ig.jsonl")
    ap.add_argument(
        "--out",
        default="data/digests/ig_addiction_sobriety_posts.md",
        help="Output Markdown path",
    )
    ap.add_argument("--min-len", type=int, default=1, help="Minimum text length to include")
    args = ap.parse_args()

    idx = (ROOT / args.index).resolve()
    out = (ROOT / args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    patterns = build_patterns()

    matches: list[Match] = []
    total_ig = 0

    with idx.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("source") != "ig":
                continue
            total_ig += 1

            text = rec.get("text") or ""
            if not isinstance(text, str):
                continue
            if len(text.strip()) < args.min_len:
                continue

            text_n = norm(text)
            reasons: list[str] = []
            for key, pat in patterns.items():
                if pat.search(text_n):
                    reasons.append(key)

            if not reasons:
                continue

            # Keep posts that are about the core themes, or match the special phrase.
            core = any(r in reasons for r in ("addiction", "sobriety", "substances"))
            special = "length_phrase" in reasons
            if not (core or special):
                continue

            # Reduce obvious noise.
            filtered_reasons = [r for r in reasons if r != "length_phrase"] + (["length_phrase"] if "length_phrase" in reasons else [])
            if is_false_positive(text_n, [r for r in filtered_reasons if r != "length_phrase"]):
                # still keep if special phrase matched
                if not special:
                    continue

            path = rec.get("path") or ""
            if not isinstance(path, str):
                path = ""
            url = rec.get("url")
            if not isinstance(url, str) or not url.strip():
                url = None

            date = infer_date(rec)
            tier = classify_tier(text_n, reasons)
            matches.append(Match(date=date, path=path, url=url, text=text.strip(), reasons=reasons, tier=tier))

    # De-dup by (date, text) to avoid duplicates coming from the same content via multiple paths (rare but possible).
    seen: set[tuple[str | None, str]] = set()
    uniq: list[Match] = []
    for m in matches:
        key = (m.date, m.text)
        if key in seen:
            continue
        seen.add(key)
        uniq.append(m)

    # Sort chronologically (date, path)
    uniq.sort(key=lambda x: ((x.date or "9999-99-99"), x.path))

    # Write markdown
    def reason_label(rs: list[str]) -> str:
        labels = []
        if "sobriety" in rs:
            labels.append("трезвость")
        if "addiction" in rs:
            labels.append("зависимость")
        if "substances" in rs:
            labels.append("алко/употребление/вещества")
        if "length_phrase" in rs:
            labels.append("«длина с чего» (фраза)")
        return ", ".join(labels) if labels else "match"

    with out.open("w", encoding="utf-8") as w:
        w.write("# IG: посты про зависимость / трезвость\n\n")
        w.write(f"Источник: `{args.index}` (IG записей: {total_ig})\n\n")
        primary = [m for m in uniq if m.tier == "primary"]
        secondary = [m for m in uniq if m.tier == "secondary"]
        w.write(f"Отобрано постов: **{len(uniq)}** (после дедупликации)\n")
        w.write(f"- **primary (точно по теме)**: {len(primary)}\n")
        w.write(f"- **secondary (косвенно: шутки/метафоры/упоминания)**: {len(secondary)}\n\n")
        w.write("Критерии (best-effort): слова про зависимость/созависимость, трезвость/воздержание, алкоголь/наркотики/срыв/реабилитацию, плюс отдельная попытка поймать фразу «длина с чего».\n\n")
        w.write("---\n\n")

        def write_section(header: str, items: list[Match]) -> None:
            w.write(f"## {header}\n\n")
            for m in items:
                title = m.date or Path(m.path).stem
                w.write(f"### {title}\n\n")
                w.write(f"- source: `{m.path}`\n")
                if m.url:
                    w.write(f"- url: `{m.url}`\n")
                w.write(f"- tags: {reason_label(m.reasons)}\n\n")
                w.write(m.text.rstrip() + "\n\n")
                w.write("---\n\n")

        write_section("Primary: точно про зависимость/трезвость", primary)
        write_section("Secondary: косвенные упоминания (шутки/метафоры)", secondary)

    print(f"[done] total_ig={total_ig} matched={len(matches)} uniq={len(uniq)} out={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

