#!/usr/bin/env python3
"""Post a vault note to Qiita as a private (draft) item.

Usage:
    python scripts/publish-qiita.py <path-to-note.md>

Reads token from ~/.config/qiita/token. Posts with private=true so the item
is never publicly visible from this script — user must promote to public on
qiita.com manually. Prints the returned item URL to stdout.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

QIITA_API = "https://qiita.com/api/v2/items"
TOKEN_PATH = Path.home() / ".config" / "qiita" / "token"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def die(msg: str, code: int = 1) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def load_token() -> str:
    if not TOKEN_PATH.exists():
        die(f"token file not found: {TOKEN_PATH} (create it with chmod 600)")
    mode = TOKEN_PATH.stat().st_mode & 0o777
    if mode & 0o077:
        die(f"token file {TOKEN_PATH} is world/group readable (mode {oct(mode)}). chmod 600 first.")
    token = TOKEN_PATH.read_text().strip()
    if not token:
        die(f"token file {TOKEN_PATH} is empty")
    return token


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse minimal YAML frontmatter. Supports: scalar, [a, b] list."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        die("note has no frontmatter (must start with ---\\n...\\n---\\n)")
    raw, body = m.group(1), m.group(2)
    fm: dict = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            items = [s.strip().strip("\"'") for s in val[1:-1].split(",")]
            fm[key] = [s for s in items if s]
        else:
            fm[key] = val.strip("\"'")
    return fm, body.lstrip("\n")


def derive_title(fm: dict, body: str, path: Path) -> str:
    """Title priority: first H1 in body → filename stem."""
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def pick_tags(fm: dict) -> list[dict]:
    tags = fm.get("qiita_tags") or fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    tags = [t for t in tags if t]
    if not tags:
        die("no tags found in frontmatter (need at least 1)")
    if len(tags) > 5:
        die(f"too many tags ({len(tags)}); Qiita limit is 5. Use qiita_tags in frontmatter to narrow.")
    return [{"name": t, "versions": []} for t in tags]


def post_to_qiita(token: str, title: str, body: str, tags: list[dict]) -> dict:
    payload = {
        "title": title,
        "body": body,
        "tags": tags,
        "private": True,           # NEVER set to False from this script
        "coediting": False,
        "tweet": False,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        QIITA_API,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        die(f"Qiita API HTTP {e.code}: {body_text}")
    except urllib.error.URLError as e:
        die(f"Qiita API network error: {e.reason}")


def main() -> None:
    if len(sys.argv) != 2:
        die("usage: publish-qiita.py <note.md>")
    path = Path(sys.argv[1])
    if not path.is_file():
        die(f"not a file: {path}")

    token = load_token()
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    if fm.get("status") != "draft":
        die(f"status must be 'draft' (got {fm.get('status')!r}). Run /draft-qiita first.")
    if fm.get("qiita_url"):
        die(f"qiita_url already set ({fm['qiita_url']}). Refusing to re-post.")

    title = derive_title(fm, body, path)
    tags = pick_tags(fm)

    result = post_to_qiita(token, title, body, tags)
    url = result.get("url")
    if not url:
        die(f"unexpected response (no url): {result}")
    print(url)


if __name__ == "__main__":
    main()
