#!/usr/bin/env python3
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "contest_analysis.html"
RAW_PATH = ROOT / "logs" / "latest_instagram_comments.json"


def run(cmd, *, capture=True):
    return subprocess.run(cmd, cwd=str(ROOT), check=True, capture_output=capture, text=True)


def extract_current_data(html):
    match = re.search(r"const DATA = (\[.*?\]);\nconst STORE_KEY", html, flags=re.S)
    if not match:
        raise RuntimeError("Could not find embedded DATA array in contest_analysis.html")
    return json.loads(match.group(1), strict=False)


def classify(item):
    text = item.get("text", "") or ""
    lower = text.lower()
    length = len(text)
    username = item.get("username", "")
    is_author = username == "olymarkes"
    pain_words = ["вес", "спин", "бол", "после род", "родов", "стресс", "устал", "устала", "развал", "рпп", "депресс", "не вывожу", "не могу", "финанс", "денег", "ипотек", "развод", "миграц", "переезд", "выгор", "живот", "отек"]
    finance_words = ["финанс", "денег", "деньги", "ипотек", "счет", "счёт", "не тяну", "не могу позволить", "не могу себе позволить", "нет возможности", "не в бюджете", "бесплатн", "дорого"]
    loyal_words = ["секта", "sekta", "буткемп", "буткэмп", "курс", "сезонк", "давно с", "проходила", "проходил", "лагер", "куратор", "волонтер"]
    promise_words = ["обещ", "готова", "готов", "дойду", "не соль", "отчет", "отчёт", "каждый день"]
    goal_words = ["хочу", "мечта", "цель", "форма", "тело", "спорт", "трен", "энерг", "сила", "привыч"]

    tags = []
    if any(w in lower for w in pain_words):
        tags.append("боль")
    if any(w in lower for w in finance_words):
        tags.append("финансы")
    if any(w in lower for w in promise_words):
        tags.append("обещание")
    if any(w in lower for w in loyal_words):
        tags.append("лояльный")
    if any(w in lower for w in goal_words):
        tags.append("цель")
    if not tags:
        tags.append("нейтрально")

    score = min(length / 55, 8.0)
    score += 3.0 if "боль" in tags else 0
    score += 2.0 if "финансы" in tags else 0
    score += 2.5 if "лояльный" in tags else 0
    score += 1.5 if "обещание" in tags else 0
    score += 1.0 if "цель" in tags else 0
    score += 0.8 if re.search(r"\b(мне|я)\s+\d{2}\b|\d{2}\s*(год|лет)", lower) else 0
    score += 0.8 if any(w in lower for w in ["мама", "дет", "ребен", "ребён"]) else 0
    if is_author:
        score = min(score, 1.0)

    if length < 10:
        level = "spam"
    elif score >= 11:
        level = "high"
    elif score >= 5:
        level = "medium"
    else:
        level = "low"

    if length >= 420:
        concrete = "high"
    elif length >= 150:
        concrete = "medium"
    elif length >= 70:
        concrete = "low"
    else:
        concrete = "none"

    return {"lvl": level, "cn": concrete, "ts": tags, "L": length, "sc": round(score, 1), "au": is_author}


def normalize(raw_item, existing_by_id):
    item_id = raw_item.get("id", "")
    if item_id in existing_by_id:
        current = existing_by_id[item_id].copy()
        current["lk"] = raw_item.get("like_count", current.get("lk", 0)) or 0
        return current

    username = raw_item.get("username", "")
    created = raw_item.get("created_at", "")
    row = {
        "u": username,
        "n": raw_item.get("full_name", ""),
        "c": raw_item.get("text", "") or "",
        "d": created[:10] if created else datetime.now(timezone.utc).date().isoformat(),
        "lk": raw_item.get("like_count", 0) or 0,
        "id": item_id,
        "pid": raw_item.get("parent_comment_id", ""),
        "url": f"https://www.instagram.com/{username}/" if username else "",
    }
    row.update(classify(raw_item))
    return row


def main():
    payload = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    html = HTML_PATH.read_text(encoding="utf-8")
    existing = {row["id"]: row for row in extract_current_data(html)}
    data = [normalize(item, existing) for item in payload.get("comments", [])]
    unique_authors = len({row["u"] for row in data if row["u"] and not row.get("au")})

    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    html = re.sub(
        r"const DATA = \[.*?\];\nconst STORE_KEY",
        lambda _: f"const DATA = {data_json};\nconst STORE_KEY",
        html,
        flags=re.S,
    )
    html = re.sub(
        r"Пост DXtJd3aEc69 · \d+ комментар(?:ий|ия|иев), \d+ уникальн(?:ый|ых|ая|ые) автор(?:а|ов)? · отметки сохраняются локально в браузере",
        f"Пост DXtJd3aEc69 · {len(data)} комментариев, {unique_authors} уникальных авторов · отметки сохраняются локально в браузере",
        html,
    )
    HTML_PATH.write_text(html, encoding="utf-8")

    changed = bool(run(["git", "status", "--short", "contest_analysis.html"]).stdout.strip())
    if not changed:
        print(f"No changes; {len(data)} comments already deployed.")
        return

    run(["git", "add", "contest_analysis.html"], capture=False)
    run(["git", "commit", "-m", f"Refresh contest comments ({len(data)})"], capture=False)
    run(["git", "push", "origin", "main"], capture=False)
    print(f"Updated and pushed {len(data)} comments.")


if __name__ == "__main__":
    main()
