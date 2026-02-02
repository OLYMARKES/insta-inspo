#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import dataclasses
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateutil_parser


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


MONTH_RE = re.compile(r"/(\d{4})/(\d{2})/?$")
DAY_RE = re.compile(r"/(\d{4})/(\d{2})/(\d{2})/?$")
POST_HTML_RE = re.compile(r"/(\d+)\.html(?:[?#].*)?$")


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_url(url: str) -> str:
    """
    Normalize by removing fragments and trimming trailing slash for non-root.
    """
    u = urlparse(url)
    u = u._replace(fragment="")
    cleaned = urlunparse(u)
    if cleaned.endswith("/") and u.path not in ("", "/"):
        cleaned = cleaned[:-1]
    return cleaned


def canonicalize_entry_url(url: str) -> str:
    """
    Canonicalize a post permalink by stripping query + fragment.
    Keeps only scheme/netloc/path. (LJ often adds ?thread=..., ?mode=reply, #t123)
    """
    u = urlparse(url)
    u = u._replace(query="", fragment="")
    cleaned = urlunparse(u)
    if cleaned.endswith("/") and u.path not in ("", "/"):
        cleaned = cleaned[:-1]
    return cleaned


def same_site(url: str, base_url: str) -> bool:
    return urlparse(url).netloc.lower() == urlparse(base_url).netloc.lower()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_text_if_exists(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def polite_sleep(delay_s: float) -> None:
    if delay_s > 0:
        time.sleep(delay_s)


@dataclass
class DiscoveredUrls:
    month_urls: set[str] = dataclasses.field(default_factory=set)
    day_urls: set[str] = dataclasses.field(default_factory=set)
    post_urls: set[str] = dataclasses.field(default_factory=set)


def fetch_html(session: requests.Session, url: str, timeout_s: float = 30.0) -> str:
    r = session.get(url, timeout=timeout_s)
    r.raise_for_status()
    r.encoding = r.encoding or "utf-8"
    return r.text


def extract_links(soup: BeautifulSoup, base_url: str) -> set[str]:
    links: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a.get("href")
        if not href:
            continue
        # skip javascript/mailto
        if href.startswith("javascript:") or href.startswith("mailto:"):
            continue
        abs_url = normalize_url(urljoin(base_url, href))
        links.add(abs_url)
    return links


def discover_post_urls(
    session: requests.Session,
    base_url: str,
    out_urls_path: Path,
    delay_s: float,
    max_posts: Optional[int] = None,
) -> list[str]:
    """
    Best-effort discovery:
    - Primary: paginate journal front page via ?skip=N and collect post permalinks (*.html).
    - Secondary fallback: calendar/month/day archives (YYYY/MM[/DD]).
    """
    base_url = normalize_url(base_url)
    discovered = DiscoveredUrls()

    seed_urls = [
        base_url,
        urljoin(base_url + "/", "calendar"),
        urljoin(base_url + "/", "calendar/"),
        urljoin(base_url + "/", "?skip=0"),
        urljoin(base_url + "/", "archive/"),
    ]

    def add_archive_urls(from_links: Iterable[str]) -> None:
        for link in from_links:
            if not same_site(link, base_url):
                continue
            if MONTH_RE.search(urlparse(link).path):
                discovered.month_urls.add(link)
            if DAY_RE.search(urlparse(link).path):
                discovered.day_urls.add(link)

    # Step 1: paginate main journal pages (?skip=N) to discover post permalinks
    post_urls: set[str] = set()
    stable_pages = 0
    prev_page_urls: set[str] = set()

    def extract_post_permalinks_from_html(html: str, page_url: str) -> set[str]:
        soup = BeautifulSoup(html, "lxml")
        links = extract_links(soup, base_url=page_url)
        found: set[str] = set()
        for link in links:
            if not same_site(link, base_url):
                continue
            if POST_HTML_RE.search(urlparse(link).path):
                found.add(canonicalize_entry_url(link))
        return found

    # LJ typically shows 10 entries per page; we keep paging until results stabilize.
    for skip in range(0, 1000000, 10):
        page_url = f"{base_url}/?skip={skip}"
        try:
            html = fetch_html(session, page_url)
        except Exception:
            break

        found = extract_post_permalinks_from_html(html, page_url)
        new = found - post_urls
        post_urls |= found

        if found == prev_page_urls or not new:
            stable_pages += 1
        else:
            stable_pages = 0
        prev_page_urls = found

        polite_sleep(delay_s)

        if max_posts and len(post_urls) >= max_posts:
            break
        # stop after a few pages in a row add nothing new (end reached or repeats)
        if stable_pages >= 5:
            break

    discovered.post_urls |= post_urls

    # Step 2: get month/day links from seeds (fallback enrichment)
    for u in seed_urls:
        try:
            html = fetch_html(session, u)
        except Exception:
            continue
        soup = BeautifulSoup(html, "lxml")
        links = extract_links(soup, base_url=u)
        add_archive_urls(links)
        polite_sleep(delay_s)

    # Step 2: expand months -> days (and also handle month pagination if present)
    month_queue = list(sorted(discovered.month_urls))
    seen_month_pages: set[str] = set()
    while month_queue:
        month_url = month_queue.pop(0)
        if month_url in seen_month_pages:
            continue
        seen_month_pages.add(month_url)
        try:
            html = fetch_html(session, month_url)
        except Exception:
            continue
        soup = BeautifulSoup(html, "lxml")
        links = extract_links(soup, base_url=month_url)
        add_archive_urls(links)

        # pagination sometimes exists via ?skip=...
        for link in links:
            if not same_site(link, base_url):
                continue
            if urlparse(link).path == urlparse(month_url).path and "skip=" in urlparse(link).query:
                month_queue.append(link)

        polite_sleep(delay_s)

    # Step 3: day pages -> post permalinks (*.html)
    day_queue = list(sorted(discovered.day_urls))
    seen_day_pages: set[str] = set()
    for day_url in day_queue:
        if day_url in seen_day_pages:
            continue
        seen_day_pages.add(day_url)
        try:
            html = fetch_html(session, day_url)
        except Exception:
            continue
        soup = BeautifulSoup(html, "lxml")
        links = extract_links(soup, base_url=day_url)
        for link in links:
            if not same_site(link, base_url):
                continue
            if POST_HTML_RE.search(urlparse(link).path):
                discovered.post_urls.add(canonicalize_entry_url(link))
        polite_sleep(delay_s)
        if max_posts and len(discovered.post_urls) >= max_posts:
            break

    post_urls_sorted = sorted({canonicalize_entry_url(u) for u in discovered.post_urls})
    if max_posts:
        post_urls_sorted = post_urls_sorted[:max_posts]

    ensure_dir(out_urls_path.parent)
    out_urls_path.write_text("\n".join(post_urls_sorted) + ("\n" if post_urls_sorted else ""), encoding="utf-8")
    return post_urls_sorted


def extract_text_preserve_paragraphs(node) -> str:
    # Prefer paragraph-like separation
    text = node.get_text("\n", strip=True)
    # Collapse 3+ newlines -> 2 newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def slugify(text: str, max_len: int = 80) -> str:
    s = (text or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^a-z0-9а-яё _-]+", "", s, flags=re.IGNORECASE)
    s = s.replace(" ", "_")
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:max_len] if s else ""


def write_index_tsv(posts: list[dict], index_path: Path) -> None:
    """
    One line per post: URL<TAB>Title
    """
    ensure_dir(index_path.parent)
    lines: list[str] = []
    for p in posts:
        url = p.get("url") or ""
        title = (p.get("title") or "").replace("\t", " ").strip()
        if not url:
            continue
        lines.append(f"{url}\t{title}")
    index_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def write_per_post_markdown(posts: list[dict], md_dir: Path) -> None:
    ensure_dir(md_dir)
    for p in posts:
        write_one_post_markdown(p, md_dir)


def write_one_post_markdown(post: dict, md_dir: Path) -> Path:
    ensure_dir(md_dir)
    entry_id = post.get("entry_id") or ""
    title = post.get("title") or "(без заголовка)"
    dt = (post.get("published_at") or "").split("T", 1)[0] if post.get("published_at") else ""
    slug = slugify(title)
    name_parts = [part for part in [dt, entry_id, slug] if part]
    fname = "__".join(name_parts) if name_parts else (entry_id or "post")
    path = md_dir / f"{fname}.md"

    parts: list[str] = []
    parts.append(f"# {title}")
    if post.get("published_at") or post.get("published_at_raw"):
        parts.append(f"*Date*: {post.get('published_at') or post.get('published_at_raw')}")
    if post.get("url"):
        parts.append(f"*URL*: {post.get('url')}")
    if post.get("tags"):
        parts.append(f"*Tags*: {', '.join(post.get('tags') or [])}")
    parts.append("")
    parts.append(post.get("content_text") or "")
    parts.append("")
    path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    return path


def first_meta(soup: BeautifulSoup, *, prop: str | None = None, name: str | None = None) -> Optional[str]:
    if prop:
        tag = soup.find("meta", attrs={"property": prop})
        if tag and tag.get("content"):
            return str(tag.get("content")).strip()
    if name:
        tag = soup.find("meta", attrs={"name": name})
        if tag and tag.get("content"):
            return str(tag.get("content")).strip()
    return None


def parse_published_at(soup: BeautifulSoup) -> tuple[Optional[str], Optional[str]]:
    """
    Returns (published_at_iso, published_at_raw)
    """
    # best case: meta with ISO
    iso = first_meta(soup, prop="article:published_time") or first_meta(soup, prop="og:updated_time")
    if iso:
        try:
            dt = dateutil_parser.isoparse(iso)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat(), iso
        except Exception:
            return None, iso

    # time tag
    t = soup.find("time")
    if t:
        if t.get("datetime"):
            raw = str(t.get("datetime")).strip()
            try:
                dt = dateutil_parser.parse(raw)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat(), raw
            except Exception:
                return None, raw
        raw = t.get_text(" ", strip=True)
        if raw:
            try:
                dt = dateutil_parser.parse(raw, fuzzy=True)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat(), raw
            except Exception:
                return None, raw

    return None, None


def parse_post_page(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    canonical = first_meta(soup, prop="og:url") or url
    canonical = canonicalize_entry_url(canonical)

    title = first_meta(soup, prop="og:title")
    if not title:
        h1 = soup.find(["h1", "h2"], class_=re.compile(r"(entry-title|b-singlepost-title|subj)", re.I))
        title = h1.get_text(" ", strip=True) if h1 else None
    if not title:
        # fallback: HTML <title>
        title_tag = soup.find("title")
        title = title_tag.get_text(" ", strip=True) if title_tag else None

    published_at, published_at_raw = parse_published_at(soup)

    # tags
    tags: list[str] = []
    for a in soup.select('a[rel="tag"], a[rel="tag"]:visited'):
        txt = a.get_text(" ", strip=True)
        if txt and txt not in tags:
            tags.append(txt)
    # additional heuristics for tags block
    for a in soup.select('a[href*="/tag/"], a[href*="tag="]'):
        txt = a.get_text(" ", strip=True)
        if txt and txt not in tags and len(txt) <= 60:
            tags.append(txt)

    # content block heuristics
    selectors = [
        ".aentry-post__text",
        ".aentry-post__content .aentry-post__text",
        ".aentry-post__text--view",
        ".aentry-post__content .aentry-post__text--view",
        "article .entry-content",
        ".entry-content",
        ".b-singlepost-body",
        "article .e-content",
        ".e-content",
        ".entry-text",
        ".entry_text",
        ".entry .content",
        "article",
    ]
    content_node = None
    for sel in selectors:
        node = soup.select_one(sel)
        if node and node.get_text(strip=True):
            content_node = node
            break

    content_html = ""
    content_text = ""
    if content_node:
        # Remove obvious UI noise if we ended up with a large wrapper node
        for sel in [
            ".aentry-post__socials",
            "section.category-panel",
            ".aentry-post__slot",
            "script",
            "style",
        ]:
            for n in content_node.select(sel):
                try:
                    n.decompose()
                except Exception:
                    pass
        content_html = str(content_node)
        content_text = extract_text_preserve_paragraphs(content_node)

    m = POST_HTML_RE.search(urlparse(canonical).path)
    entry_id = m.group(1) if m else None

    return {
        "entry_id": entry_id,
        "url": canonical,
        "source_url": normalize_url(url),
        "title": title,
        "published_at": published_at,  # UTC ISO if parsed
        "published_at_raw": published_at_raw,
        "tags": tags,
        "content_text": content_text,
        "content_html": content_html,
    }


def iter_processed_urls(posts_jsonl_path: Path) -> set[str]:
    processed: set[str] = set()
    if not posts_jsonl_path.exists():
        return processed
    with posts_jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            url = obj.get("url") or obj.get("source_url")
            if isinstance(url, str):
                processed.add(canonicalize_entry_url(url))
    return processed


def write_csv(posts: list[dict], csv_path: Path) -> None:
    ensure_dir(csv_path.parent)
    fieldnames = [
        "entry_id",
        "url",
        "title",
        "published_at",
        "published_at_raw",
        "tags",
        "content_text",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for p in posts:
            w.writerow(
                {
                    "entry_id": p.get("entry_id"),
                    "url": p.get("url"),
                    "title": p.get("title"),
                    "published_at": p.get("published_at"),
                    "published_at_raw": p.get("published_at_raw"),
                    "tags": "; ".join(p.get("tags") or []),
                    "content_text": p.get("content_text"),
                }
            )


def write_markdown(posts: list[dict], md_path: Path) -> None:
    ensure_dir(md_path.parent)
    parts: list[str] = []
    for p in posts:
        title = p.get("title") or "(без заголовка)"
        parts.append(f"## {title}")
        if p.get("published_at") or p.get("published_at_raw"):
            parts.append(f"*Date*: {p.get('published_at') or p.get('published_at_raw')}")
        if p.get("url"):
            parts.append(f"*URL*: {p.get('url')}")
        if p.get("tags"):
            parts.append(f"*Tags*: {', '.join(p.get('tags') or [])}")
        parts.append("")
        parts.append(p.get("content_text") or "")
        parts.append("\n---\n")
    md_path.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Export public LiveJournal posts (text + basic metadata).")
    ap.add_argument("--base-url", required=True, help="Base journal URL, e.g. https://olymarkes.livejournal.com")
    ap.add_argument("--out-dir", required=True, help="Output directory, e.g. data/lj_export")
    ap.add_argument("--urls-file", default="", help="Optional: file with URLs to parse (one per line). Skips discovery.")
    ap.add_argument("--delay", type=float, default=0.7, help="Delay between HTTP requests (seconds).")
    ap.add_argument("--max-posts", type=int, default=0, help="Limit number of posts (0 = no limit).")
    ap.add_argument("--save-raw-html", action="store_true", help="Save raw HTML pages to out-dir/raw_html/")
    ap.add_argument("--per-post-md", action="store_true", help="Write one cleaned Markdown file per post.")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    ensure_dir(out_dir)
    raw_dir = out_dir / "raw_html"
    urls_path = out_dir / "urls.txt"
    posts_jsonl_path = out_dir / "posts.jsonl"
    posts_csv_path = out_dir / "posts.csv"
    posts_md_path = out_dir / "posts.md"
    index_tsv_path = out_dir / "index.tsv"
    md_posts_dir = out_dir / "posts_md"
    run_info_path = out_dir / "run_info.json"

    max_posts = args.max_posts if args.max_posts and args.max_posts > 0 else None

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "ru,en;q=0.8"})

    # 1) Discover URLs
    if args.urls_file:
        urls_file_path = Path(args.urls_file)
        raw = read_text_if_exists(urls_file_path) or ""
        post_urls = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            post_urls.append(canonicalize_entry_url(line))
        # dedupe while preserving order
        seen = set()
        post_urls = [u for u in post_urls if not (u in seen or seen.add(u))]
        if max_posts:
            post_urls = post_urls[:max_posts]
        ensure_dir(urls_path.parent)
        urls_path.write_text("\n".join(post_urls) + ("\n" if post_urls else ""), encoding="utf-8")
        print(f"[discover] loaded {len(post_urls)} post URLs from {urls_file_path} -> {urls_path}", flush=True)
    else:
        post_urls = discover_post_urls(
            session=session,
            base_url=args.base_url,
            out_urls_path=urls_path,
            delay_s=args.delay,
            max_posts=max_posts,
        )
        print(f"[discover] found {len(post_urls)} post URLs -> {urls_path}", flush=True)

    # 2) Parse posts (resume supported)
    processed = iter_processed_urls(posts_jsonl_path)
    print(f"[resume] already have {len(processed)} URLs in {posts_jsonl_path}", flush=True)

    if args.save_raw_html:
        ensure_dir(raw_dir)
    if args.per_post_md:
        ensure_dir(md_posts_dir)

    posts_by_url: dict[str, dict] = {}
    if posts_jsonl_path.exists():
        # load existing (dedupe by canonical URL)
        with posts_jsonl_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                u = obj.get("url") or obj.get("source_url")
                if isinstance(u, str) and u:
                    posts_by_url[canonicalize_entry_url(u)] = obj

    with posts_jsonl_path.open("a", encoding="utf-8") as out_jsonl:
        for i, url in enumerate(post_urls, start=1):
            nurl = canonicalize_entry_url(url)
            if nurl in processed:
                continue

            try:
                html = fetch_html(session, nurl)
                post = parse_post_page(html, nurl)
                post["fetched_at"] = now_utc_iso()
            except Exception as e:
                err = {"url": nurl, "error": repr(e), "fetched_at": now_utc_iso()}
                print(f"[error] {nurl}: {err['error']}", file=sys.stderr, flush=True)
                continue

            if args.save_raw_html:
                # filename by entry_id if available, else by slug-ish
                fname = post.get("entry_id") or re.sub(r"[^a-zA-Z0-9]+", "_", urlparse(nurl).path.strip("/"))[:80]
                if not fname:
                    fname = f"post_{i}"
                raw_path = raw_dir / f"{fname}.html"
                raw_path.write_text(html, encoding="utf-8")
                post["raw_html_path"] = str(raw_path.as_posix())

            out_jsonl.write(json.dumps(post, ensure_ascii=False) + "\n")
            out_jsonl.flush()
            os.fsync(out_jsonl.fileno())

            posts_by_url[canonicalize_entry_url(post.get("url") or nurl)] = post
            processed.add(nurl)

            if args.per_post_md:
                try:
                    write_one_post_markdown(post, md_posts_dir)
                except Exception as e:
                    print(f"[warn] md write failed for {nurl}: {repr(e)}", file=sys.stderr, flush=True)

            if i % 20 == 0:
                print(f"[parse] processed {i}/{len(post_urls)}", flush=True)
            polite_sleep(args.delay)

    # 3) Export formats from full parsed set (deduped)
    parsed_posts_sorted = sorted(
        posts_by_url.values(),
        key=lambda p: (p.get("published_at") or "", p.get("url") or ""),
    )
    # Rewrite JSONL to a clean deduped set (stable order)
    posts_jsonl_path.write_text(
        "".join(json.dumps(p, ensure_ascii=False) + "\n" for p in parsed_posts_sorted),
        encoding="utf-8",
    )
    write_csv(parsed_posts_sorted, posts_csv_path)
    write_markdown(parsed_posts_sorted, posts_md_path)
    write_index_tsv(parsed_posts_sorted, index_tsv_path)
    if args.per_post_md:
        write_per_post_markdown(parsed_posts_sorted, md_posts_dir)

    run_info = {
        "base_url": normalize_url(args.base_url),
        "generated_at": now_utc_iso(),
        "posts_count": len(parsed_posts_sorted),
        "urls_count": len(post_urls),
        "save_raw_html": bool(args.save_raw_html),
        "delay_s": args.delay,
        "per_post_md": bool(args.per_post_md),
    }
    run_info_path.write_text(json.dumps(run_info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[export] posts.jsonl: {posts_jsonl_path}")
    print(f"[export] posts.csv:   {posts_csv_path}")
    print(f"[export] posts.md:    {posts_md_path}")
    print(f"[export] index.tsv:   {index_tsv_path}")
    if args.per_post_md:
        print(f"[export] posts_md/:  {md_posts_dir}")
    print(f"[export] run_info:    {run_info_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


