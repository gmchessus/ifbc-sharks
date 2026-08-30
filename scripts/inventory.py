#!/usr/bin/env python3
"""Build a same-origin inventory of the legacy site without modifying it.

Usage:
    python3 scripts/inventory.py --output archive-inventory.csv

The script intentionally inventories first. Downloading/importing media is a
separate reviewed step so no legacy asset is silently overwritten.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import deque
from html.parser import HTMLParser
from pathlib import PurePosixPath
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen
import ssl

DEFAULT_START = "https://ifbc-sharks.ru/"
USER_AGENT = "IFBC-Sharks-Archive-Inventory/1.0 (read-only)"
MEDIA_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".svg", ".mp4", ".webm", ".mov", ".avi"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: set[str] = set()
        self.title: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "title":
            self._in_title = True
        for key in ("href", "src", "poster"):
            value = attributes.get(key)
            if value:
                self.links.add(value.strip())

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title.append(data.strip())


def normalize(raw: str, base: str, host: str) -> str | None:
    absolute = urljoin(base, raw)
    absolute, _ = urldefrag(absolute)
    parsed = urlparse(absolute)
    # Ignore query/action URLs during a read-only inventory. They can trigger
    # duplicate views or state-changing endpoints on legacy applications.
    if parsed.scheme not in {"http", "https"} or parsed.netloc != host or parsed.query:
        return None
    return absolute


def is_media(url: str) -> bool:
    return PurePosixPath(urlparse(url).path.lower()).suffix in MEDIA_EXTENSIONS


def fetch(url: str, host: str, insecure: bool) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    context = ssl._create_unverified_context() if insecure else None
    with urlopen(request, timeout=20, context=context) as response:
        final = urlparse(response.geturl())
        if final.netloc != host:
            raise RuntimeError(f"redirected outside allowed host: {response.geturl()}")
        return response.read()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default=DEFAULT_START)
    parser.add_argument("--output", default="archive-inventory.csv")
    parser.add_argument("--max-pages", type=int, default=5000)
    parser.add_argument("--insecure", action="store_true", help="trust a self-signed source certificate; use only for this public read-only source")
    args = parser.parse_args()

    host = urlparse(args.start).netloc
    queue: deque[str] = deque([args.start])
    visited: set[str] = set()
    rows: list[dict[str, str]] = []

    while queue and len(visited) < args.max_pages:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        try:
            raw = fetch(url, host, args.insecure)
        except Exception as error:  # keep the inventory going on broken legacy pages
            rows.append({"source_url": url, "content_type": "unavailable", "title": "", "event_date": "", "season": "", "team": "", "photo_count": "", "video_count": "", "target_url": "", "migration_status": "needs-review", "notes": str(error)})
            continue

        content_type = "media" if is_media(url) else "page"
        title = ""
        if content_type == "page":
            text = raw.decode("utf-8", errors="replace")
            parsed = PageParser()
            parsed.feed(text)
            title = re.sub(r"\s+", " ", " ".join(parsed.title)).strip()
            for raw_link in parsed.links:
                linked = normalize(raw_link, url, host)
                if linked and linked not in visited:
                    queue.append(linked)
                if linked and is_media(linked):
                    rows.append({"source_url": linked, "content_type": "media", "title": "", "event_date": "", "season": "", "team": "", "photo_count": "", "video_count": "", "target_url": "", "migration_status": "discovered", "notes": "found in " + url})

        rows.append({"source_url": url, "content_type": content_type, "title": title, "event_date": "", "season": "", "team": "", "photo_count": "", "video_count": "", "target_url": "", "migration_status": "discovered", "notes": ""})

    unique: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        unique[(row["source_url"], row["content_type"])] = row
    fieldnames = ["source_url", "content_type", "title", "event_date", "season", "team", "photo_count", "video_count", "target_url", "migration_status", "notes"]
    with open(args.output, "w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted(unique.values(), key=lambda row: row["source_url"]))
    print(f"Inventoried {len(unique)} unique records from {args.start} into {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
