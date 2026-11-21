"""Refresh the auto-updated sections of the profile README.

Standard library only. Run locally or from the GitHub Action:
    python scripts/update_readme.py
Sections are replaced between <!-- name:start --> and <!-- name:end --> markers.
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

USER = "sametbesni"
SKIP_REPOS = {USER}
LIMIT = 5
MAX_AGE_DAYS = 365
README = Path(__file__).resolve().parent.parent / "README.md"


def fetch(url: str, accept: str = "application/json") -> bytes:
    headers = {"User-Agent": f"{USER}-profile-readme", "Accept": accept}
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com"):
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return r.read()


def latest_repos() -> str:
    url = f"https://api.github.com/users/{USER}/repos?type=owner&sort=pushed&per_page=30"
    repos = json.loads(fetch(url))
    cutoff = (datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)).strftime("%Y-%m-%d")
    rows = []
    for repo in repos:
        if repo["fork"] or repo["archived"] or repo["name"] in SKIP_REPOS:
            continue
        if repo["pushed_at"][:10] < cutoff:  # old practice repos stay off the front page
            continue
        desc = (repo.get("description") or "").strip()
        line = f"[{repo['name']}]({repo['html_url']}) - {repo['pushed_at'][:10]}"
        if desc:
            short = desc if len(desc) <= 70 else desc[:67].rstrip() + "..."
            line += f"<br><sub>{short}</sub>"
        rows.append(line)
        if len(rows) == LIMIT:
            break
    return "\n\n".join(rows)


def replace_section(text: str, name: str, body: str) -> str:
    pattern = re.compile(rf"(<!-- {name}:start -->).*?(<!-- {name}:end -->)", re.DOTALL)
    if not pattern.search(text):
        raise SystemExit(f"marker '{name}' not found in README")
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(2)}", text)


def main() -> int:
    text = README.read_text(encoding="utf-8")
    updated = text
    for name, builder in (("repos", latest_repos),):
        try:
            updated = replace_section(updated, name, builder())
        except SystemExit:
            raise
        except Exception as exc:  # keep the old section if one source is down
            print(f"warning: {name} not refreshed: {exc}", file=sys.stderr)
    if updated != text:
        README.write_text(updated, encoding="utf-8", newline="\n")
        print("README updated")
    else:
        print("README unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
