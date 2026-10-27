#!/usr/bin/env python3
"""Check generated asset URLs, including their case on case-insensitive systems."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"img", "script", "source"} and attrs.get("src"):
            self.urls.append(attrs["src"])
        if tag in {"img", "source"} and attrs.get("srcset"):
            self.urls.extend(item.strip().split()[0] for item in attrs["srcset"].split(","))
        if tag == "link" and set(attrs.get("rel", "").split()) & {
            "stylesheet", "icon", "apple-touch-icon", "mask-icon", "preload"
        } and attrs.get("href"):
            self.urls.append(attrs["href"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", default="public")
    parser.add_argument("--base-url", default="https://likipiki.github.io/")
    args = parser.parse_args()
    root = Path(args.directory)
    if not root.is_dir():
        parser.error(f"Build output does not exist: {root}")
    files = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    errors = set()
    checked = 0
    for name in sorted(files):
        if not name.endswith(".html"):
            continue
        assets = AssetParser()
        assets.feed((root / name).read_text(encoding="utf-8"))
        page_url = urljoin(args.base_url, name)
        for asset in assets.urls:
            url = urlsplit(urljoin(page_url, asset))
            if url.netloc != urlsplit(args.base_url).netloc or url.scheme not in {"http", "https"}:
                continue
            checked += 1
            target = unquote(url.path).lstrip("/")
            if target not in files:
                errors.add(f"{name}: missing asset {url.path}")
    if errors:
        raise SystemExit("\n".join(sorted(errors)))
    print(f"Checked {checked} local asset references; all paths match exactly.")


if __name__ == "__main__":
    main()
