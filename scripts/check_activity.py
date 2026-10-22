#!/usr/bin/env python3
"""Flag README entries whose GitHub repository is missing, archived, moved, or inactive.

Modes: api (GitHub REST, needs GITHUB_TOKEN or GH_TOKEN), web (commit feed, no token),
auto (api when a token is set). Exit 1 with --fail-on-stale if anything is flagged.
"""

from __future__ import annotations

import argparse
import datetime as dt
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from functools import reduce
from typing import Callable, Iterable, Mapping, NamedTuple

USER_AGENT = "awesome-parsers-activity-check (+https://github.com/s5dsn-eqee/awesome-parsers)"
API_HEADERS = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
LIST_ITEM_RE = re.compile(r"^\s*[-*]\s+\[([^\]]+)\]\((https?://[^)\s]+)\)")
GITHUB_REPO_RE = re.compile(
    r"^https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?(?:[/#?].*)?$"
)
HEADING_RE = re.compile(r"^(#{2,6})\s+(.*?)\s*$")
DEFAULT_SKIP_SECTIONS = ("Contents", "Learning Resources", "Graveyard", "Contributing", "License")
NETWORK_ERRORS = (urllib.error.URLError, TimeoutError, http.client.HTTPException, ConnectionError)


class Entry(NamedTuple):
    name: str
    url: str
    section: str | None
    line: int
    repo: str | None


class Response(NamedTuple):
    status: int
    body: bytes
    headers: Mapping[str, str]
    url: str


class RateLimited(Exception):
    def __init__(self, reset_epoch: int | None):
        super().__init__("rate limited")
        self.reset_epoch = reset_epoch


class TransientError(Exception):
    pass


def log(message: str) -> None:
    print(message, file=sys.stderr)


def repo_of(url: str) -> str | None:
    match = GITHUB_REPO_RE.match(url)
    return f"{match.group(1)}/{match.group(2)}" if match else None


def parse_readme(path: str, skip: frozenset[str]) -> tuple[Entry, ...]:
    def step(state: tuple, numbered: tuple[int, str]) -> tuple:
        top, section, entries = state
        lineno, line = numbered
        heading = HEADING_RE.match(line)
        if heading:
            level, title = len(heading.group(1)), heading.group(2)
            return (title, title, entries) if level == 2 else (top, f"{top} / {title}" if top else title, entries)
        item = LIST_ITEM_RE.match(line)
        if top in skip or not item:
            return state
        entry = Entry(item.group(1), item.group(2), section, lineno, repo_of(item.group(2)))
        return top, section, entries + (entry,)

    with open(path, encoding="utf-8") as fh:
        return reduce(step, enumerate(fh, 1), (None, None, ()))[2]


def lower_keys(headers: Iterable[tuple[str, str]]) -> Mapping[str, str]:
    return {k.lower(): v for k, v in headers}


def read_body(resp) -> bytes:
    try:
        return resp.read()
    except http.client.IncompleteRead as err:
        if not err.partial:
            raise TransientError(str(err)) from err
        return err.partial


def fetch(url: str, headers: Mapping[str, str] | None = None, timeout: int = 30) -> Response:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return Response(resp.status, read_body(resp), lower_keys(resp.headers.items()), resp.geturl())
    except urllib.error.HTTPError as err:
        hdrs = lower_keys(err.headers.items())
        reset = hdrs.get("x-ratelimit-reset")
        if err.code == 429 or (err.code == 403 and hdrs.get("x-ratelimit-remaining") == "0"):
            raise RateLimited(int(reset) if reset else None) from err
        return Response(err.code, err.read(), hdrs, url)


def fetch_with_retry(url: str, headers: Mapping[str, str] | None = None, attempts: int = 3, delay: int = 15) -> Response:
    try:
        return fetch(url, headers)
    except RateLimited as rl:
        wait = max(1, rl.reset_epoch - int(time.time()) + 2) if rl.reset_epoch else delay
        if attempts == 1 or wait > 900:
            raise
        log(f"  rate limited, sleeping {wait}s")
        time.sleep(wait)
        return fetch_with_retry(url, headers, attempts - 1, delay * 2)
    except (*NETWORK_ERRORS, TransientError) as err:
        if attempts == 1:
            raise
        log(f"  network error ({err}), retrying")
        time.sleep(min(delay, 5))
        return fetch_with_retry(url, headers, attempts - 1, delay)


def failure(source: str, status: int) -> dict:
    return {"status": "missing", "source": source} if status == 404 else {"status": "error", "source": source, "http_status": status}


def check_api(repo: str, token: str | None) -> dict:
    auth = {"Authorization": f"Bearer {token}"} if token else {}
    resp = fetch_with_retry(f"https://api.github.com/repos/{repo}", {**API_HEADERS, **auth})
    if resp.status != 200:
        return failure("api", resp.status)
    data = json.loads(resp.body)
    return {
        "status": "ok",
        "source": "api",
        "last_activity": data.get("pushed_at"),
        "archived": bool(data.get("archived")),
        "stars": data.get("stargazers_count"),
        "resolved_repo": data.get("full_name"),
        "disabled": bool(data.get("disabled")),
    }


def check_web(repo: str) -> dict:
    feed = fetch_with_retry(f"https://github.com/{repo}/commits.atom")
    if feed.status != 200:
        return failure("web", feed.status)
    page = fetch_with_retry(f"https://github.com/{repo}")
    updated = re.search(rb"<updated>([^<]+)</updated>", feed.body)
    resolved = re.match(r"^https?://github\.com/([^/]+/[^/]+)", feed.url)
    archived = re.search(rb'"isArchived":(true|false)', page.body) if page.status == 200 else None
    return {
        "status": "ok",
        "source": "web",
        "last_activity": updated.group(1).decode() if updated else None,
        "archived": archived.group(1) == b"true" if archived else None,
        "stars": None,
        "resolved_repo": resolved.group(1) if resolved else repo,
    }


def parse_iso(ts: str | None) -> dt.datetime | None:
    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00")) if ts else None


def evaluate(entry: Entry, result: dict, now: dt.datetime, max_age_days: int) -> dict:
    last = parse_iso(result.get("last_activity"))
    age = (now - last).days if last else None
    resolved = result.get("resolved_repo")
    moved = bool(resolved and entry.repo and resolved.lower() != entry.repo.lower())
    checks = (
        (result.get("archived"), "archived"),
        (result.get("disabled"), "disabled"),
        (age is not None and age > max_age_days, f"no activity for {age} days"),
        (moved, f"moved to {resolved}"),
    )
    reasons = (
        ["repository not found (404)"] if result["status"] == "missing"
        else [f"could not check (HTTP {result.get('http_status')})"] if result["status"] == "error"
        else [text for hit, text in checks if hit]
    )
    return {**entry._asdict(), **result, "age_days": age, "reasons": reasons, "flagged": bool(reasons)}


def md_row(r: dict) -> str:
    last = (r.get("last_activity") or "")[:10]
    age = "" if r.get("age_days") is None else str(r["age_days"])
    return f"| [{r['name']}]({r['url']}) | {r['section']} | {last} | {age} | {'; '.join(r['reasons'])} |"


def md_table(rows: Iterable[dict]) -> str:
    header = ("| Entry | Section | Last activity | Age (days) | Why |", "| --- | --- | --- | --- | --- |")
    return "\n".join((*header, *map(md_row, rows)))


def build_report(rows: list[dict], unchecked: Iterable[Entry], max_age_days: int, now: dt.datetime, source: str) -> str:
    flagged = sorted((r for r in rows if r["flagged"]), key=lambda r: r.get("age_days") or 0, reverse=True)
    healthy = sorted((r for r in rows if not r["flagged"]), key=lambda r: r["name"].lower())
    unchecked = tuple(unchecked)
    lines = (
        f"# Activity report ({now:%Y-%m-%d})",
        "",
        f"Checked {len(rows)} GitHub-hosted entries via `{source}`; threshold {max_age_days} days.",
        "",
        f"## Flagged ({len(flagged)})",
        "",
        md_table(flagged) if flagged else "Nothing to report.",
        "",
        f"## Healthy ({len(healthy)})",
        "",
        "<details><summary>Show</summary>\n",
        md_table(healthy) if healthy else "None.",
        "\n</details>",
        *(("", f"## Not on GitHub, check by hand ({len(unchecked)})", "") if unchecked else ()),
        *(f"- [{e.name}]({e.url}) ({e.section})" for e in unchecked),
    )
    return "\n".join(lines) + "\n"


def list_entries(readme: str, skip: frozenset[str]) -> int:
    entries = parse_readme(readme, skip)
    github = [e for e in entries if e.repo]
    by_repo = {key: [e.line for e in github if e.repo.lower() == key] for key in {e.repo.lower() for e in github}}
    duplicates = {key: lines for key, lines in by_repo.items() if len(lines) > 1}
    print(*(f"{e.line:4d}  {e.section:<45} {e.name:<28} {e.repo or e.url}" for e in entries), sep="\n")
    log(f"\n{len(entries)} entries, {len(github)} on GitHub, {len(entries) - len(github)} elsewhere")
    tuple(log(f"duplicate: {key} listed on lines {', '.join(map(str, lines))}") for key, lines in duplicates.items())
    return 1 if duplicates else 0


def safe_check(check: Callable[[str], dict], repo: str, source: str) -> dict:
    try:
        return check(repo)
    except RateLimited:
        raise
    except Exception as err:  # noqa: BLE001
        return {"status": "error", "source": source, "http_status": None, "error": str(err)}


def check_all(repos: Mapping[str, str], check: Callable[[str], dict], source: str, delay: float, quiet: bool) -> dict:
    def one(i: int, key: str, repo: str) -> dict:
        quiet or log(f"[{i}/{len(repos)}] {repo}")
        result = safe_check(check, repo, source)
        delay and time.sleep(delay)
        return result

    return {key: one(i, key, repo) for i, (key, repo) in enumerate(repos.items(), 1)}


def write_text(path: str | None, text: str, mode: str = "w") -> None:
    if path:
        with open(path, mode, encoding="utf-8") as fh:
            fh.write(text)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--readme", default="README.md")
    ap.add_argument("--max-age-days", type=int, default=730)
    ap.add_argument("--mode", choices=("auto", "api", "web"), default="auto")
    ap.add_argument("--delay", type=float, default=None, help="seconds between requests (default 0 api / 0.5 web)")
    ap.add_argument("--skip-section", action="append", default=None,
                    help="top-level section to ignore (repeatable; default: %s)" % ", ".join(DEFAULT_SKIP_SECTIONS))
    ap.add_argument("--json", dest="json_path", help="write full results as JSON")
    ap.add_argument("--report", dest="report_path", help="write Markdown report")
    ap.add_argument("--fail-on-stale", action="store_true")
    ap.add_argument("--list", action="store_true", help="only parse the README and fail on duplicates (no network)")
    ap.add_argument("--quiet", action="store_true")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    skip = frozenset(args.skip_section or DEFAULT_SKIP_SECTIONS)
    if args.list:
        return list_entries(args.readme, skip)

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    mode = args.mode if args.mode != "auto" else ("api" if token else "web")
    delay = args.delay if args.delay is not None else (0.0 if mode == "api" else 0.5)
    check = (lambda repo: check_api(repo, token)) if mode == "api" else check_web
    now = dt.datetime.now(dt.timezone.utc)

    entries = parse_readme(args.readme, skip)
    github_entries = [e for e in entries if e.repo]
    unchecked = [e for e in entries if not e.repo]
    repos = {e.repo.lower(): e.repo for e in github_entries}
    args.quiet or log(f"{len(github_entries)} GitHub entries to check ({mode} mode), {len(unchecked)} non-GitHub entries skipped")

    try:
        results = check_all(repos, check, mode, delay, args.quiet)
    except RateLimited:
        log("Rate limit exhausted; aborting. Set GITHUB_TOKEN or try again later.")
        return 2

    rows = [evaluate(e, results[e.repo.lower()], now, args.max_age_days) for e in github_entries]
    flagged = [r for r in rows if r["flagged"]]
    report = build_report(rows, unchecked, args.max_age_days, now, mode)
    payload = {"generated": now.isoformat(), "mode": mode, "max_age_days": args.max_age_days,
               "entries": rows, "unchecked": [e._asdict() for e in unchecked]}

    write_text(args.report_path, report)
    write_text(args.json_path, json.dumps(payload, indent=2))
    write_text(os.environ.get("GITHUB_OUTPUT"), f"stale_count={len(flagged)}\n", mode="a")
    print(report) if not args.report_path and not args.quiet else log(f"flagged: {len(flagged)} of {len(rows)}")
    return 1 if args.fail_on_stale and flagged else 0


if __name__ == "__main__":
    sys.exit(main())
