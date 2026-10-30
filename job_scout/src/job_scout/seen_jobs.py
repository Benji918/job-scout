"""Persistent ledger of job listings already shown to the candidate.

The crew has no memory of past *runs* (the memory system only spans a single
kickoff), so "never show me the same job twice" cannot be enforced by wording
alone. This module stores every listing that reached a final dossier in
``seen_jobs.json`` and renders it for injection into the prompts.

Override the ledger location with ``JOB_SCOUT_SEEN_JOBS=/path/to/file.json``.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

_LEDGER_PATH = Path(__file__).resolve().parents[2] / "seen_jobs.json"
_URL_RE = re.compile(r"https?://[^\s<>\"')\]]+")
_TRAILING = ".,;:!?)]}>'\""
_POSTED_RE = re.compile(
    r"Posted:\s*("
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
    r"|[0-9]{1,2}\s+\w+\s+[0-9]{4}"
    r"|\w+\s+[0-9]{1,2},\s*[0-9]{4}"
    r")",
    re.IGNORECASE,
)


def ledger_path() -> Path:
    """Location of the ledger file (env override wins)."""
    override = os.getenv("JOB_SCOUT_SEEN_JOBS")
    return Path(override).expanduser().resolve() if override else _LEDGER_PATH


def normalize_url(url: str) -> str:
    """Reduce a URL to a stable identity (no scheme, www, query, fragment)."""
    url = (url or "").strip().rstrip(_TRAILING)
    if not url:
        return ""
    url = re.sub(r"^https?://", "", url, flags=re.IGNORECASE)
    url = re.sub(r"^www\.", "", url, flags=re.IGNORECASE)
    url = url.split("#", 1)[0].split("?", 1)[0]
    return url.rstrip("/").lower()


def entry_key(entry: dict) -> str:
    """Identity of a listing: normalized URL, else company + title."""
    url = normalize_url(entry.get("url", ""))
    if url:
        return f"url:{url}"
    company = (entry.get("company") or "").strip().lower()
    title = (entry.get("title") or "").strip().lower()
    return f"role:{company}|{title}"


def load_ledger() -> list[dict]:
    path = ledger_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return data if isinstance(data, list) else []


def save_ledger(entries: list[dict]) -> None:
    path = ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def format_for_prompt(entries: Iterable[dict]) -> str:
    """Compact block injected into prompts as ``{previously_seen_jobs}``."""
    lines = []
    for entry in entries:
        title = entry.get("title") or "Untitled role"
        company = entry.get("company") or "Unknown company"
        posted = entry.get("posted") or "date unknown"
        url = entry.get("url") or "no url"
        lines.append(f"- {company} | {title} | {posted} | {url}")
    if not lines:
        return "(none yet - no listings have been shown to the candidate)"
    return "\n".join(lines)


def known_keys(entries: Iterable[dict] | None = None) -> set[str]:
    entries = load_ledger() if entries is None else entries
    return {entry_key(entry) for entry in entries}


def is_seen(url: str, title: str = "", company: str = "", entries: list[dict] | None = None) -> bool:
    """True when this listing was already presented on an earlier run."""
    keys = known_keys(entries)
    if normalize_url(url) and entry_key({"url": url}) in keys:
        return True
    return entry_key({"title": title, "company": company}) in keys


def _parse_line(line: str) -> dict | None:
    urls = _URL_RE.findall(line)
    if not urls:
        return None
    url = urls[0].rstrip(_TRAILING)
    parts = [part.strip() for part in line.split("|")]
    title = parts[0] if parts and not parts[0].lower().startswith("http") else ""
    company = ""
    if len(parts) > 1 and not parts[1].lower().startswith("http"):
        company = parts[1]
    posted_match = _POSTED_RE.search(line)
    return {
        "title": title.lstrip("-* ").strip(),
        "company": company,
        "posted": posted_match.group(1) if posted_match else "",
        "url": url,
    }


def record_from_report(report: str) -> int:
    """Append every listing URL found in a dossier to the ledger.

    Returns the number of newly recorded listings. Empty/failed runs add nothing.
    """
    entries = load_ledger()
    seen = known_keys(entries)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    added = 0
    for raw_line in (report or "").splitlines():
        item = _parse_line(raw_line)
        if not item:
            continue
        key = entry_key(item)
        if key in seen:
            continue
        item["first_seen"] = now
        entries.append(item)
        seen.add(key)
        added += 1
    if added:
        save_ledger(entries)
    return added


if __name__ == "__main__":  # manual seeding: python -m job_scout.seen_jobs <report.md>
    import sys

    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("report.md")
    text = source.read_text(encoding="utf-8")
    count = record_from_report(text)
    print(f"Recorded {count} listing(s) from {source} into {ledger_path()}")
