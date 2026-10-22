#!/usr/bin/env python3
"""Report README entries whose upstream GitHub repository is stale or archived.

Every list item of the form ``- [name](https://github.com/owner/repo) ...`` in
the README is checked. Items under the sections named in ``--skip-section``
(Graveyard, Learning Resources, and so on by default) are ignored.

Two data sources are supported:

* ``api`` - the GitHub REST API. Set ``GITHUB_TOKEN`` (or ``GH_TOKEN``) for a
  usable rate limit. Reports ``pushed_at`` (last push to any branch), the
  archived flag, and the star count. This is what the monthly workflow uses.
* ``web`` - no token needed. Reads the repository's commit Atom feed for the
  latest default-branch commit date and the repository page for the archived
  flag. Slower, and the date is "last commit on the default branch" rather
  than "last push to any branch".

``--mode auto`` (the default) picks ``api`` when a token is present and ``web``
otherwise.

Examples::

    python3 scripts/check_activity.py
    python3 scripts/check_activity.py --max-age-days 730 --report report.md --json report.json
    GITHUB_TOKEN=... python3 scripts/check_activity.py --fail-on-stale

Exit status is 0 unless ``--fail-on-stale`` is given and stale, archived, or
missing entries were found.
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

USER_AGENT = "awesome-parsers-activity-check (+https://github.com/s5dsn-eqee/awesome-parsers)"

LIST_ITEM_RE = re.compile(r"^\s*[-*]\s+\[([^\]]+)\]\((https?://[^)\s]+)\)")
GITHUB_REPO_RE = re.compile(
    r"^https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?(?:[/#?].*)?$"
)
HEADING_RE = re.compile(r"^(#{2,6})\s+(.*?)\s*$")

DEFAULT_SKIP_SECTIONS = (
    "Contents",
    "Learning Resources",
    "Graveyard",
    "Contributing",
    "License",
)


# --------------------------------------------------------------------------- #
# README parsing
# --------------------------------------------------------------------------- #


def parse_readme(path: str, skip_sections: set[str]) -> list[dict]:
    """Return one dict per list item that links to a GitHub repository."""
    entries: list[dict] = []
    top: str | None = None
    section: str | None = None
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            heading = HEADING_RE.match(line)
            if heading:
                level = len(heading.group(1))
                title = heading.group(2)
                if level == 2:
                    top = title
                    section = title
                else:
                    section = f"{top} / {title}" if top else title
                continue
            if top in skip_sections:
                continue
            item = LIST_ITEM_RE.match(line)
            if not item:
                continue
            name, url = item.group(1), item.group(2)
            repo_match = GITHUB_REPO_RE.match(url)
            entries.append(
                {
                    "name": name,
                    "url": url,
                    "section": section,
                    "line": lineno,
                    "repo": f"{repo_match.group(1)}/{repo_match.group(2)}" if repo_match else None,
                }
            )
    return entries


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #


class RateLimited(Exception):
    def __init__(self, reset_epoch: int | None):
        super().__init__("rate limited")
        self.reset_epoch = reset_epoch


class TransientError(Exception):
    """A network hiccup worth retrying."""


def fetch(url: str, headers: dict | None = None, timeout: int = 30) -> tuple[int, bytes, dict, str]:
    """GET ``url``; return (status, body, headers, final_url)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
            try:
                body = resp.read()
            except http.client.IncompleteRead as err:
                # GitHub sometimes closes large chunked responses early. The
                # fields we look for are near the top of the page, so a
                # non-empty partial body is good enough; an empty one is retried.
                if not err.partial:
                    raise TransientError(str(err)) from err
                body = err.partial
            return resp.status, body, hdrs, resp.geturl()
    except urllib.error.HTTPError as err:
        hdrs = {k.lower(): v for k, v in err.headers.items()}
        if err.code in (403, 429) and hdrs.get("x-ratelimit-remaining") == "0":
            reset = hdrs.get("x-ratelimit-reset")
            raise RateLimited(int(reset) if reset else None) from err
        if err.code == 429:
            raise RateLimited(None) from err
        return err.code, err.read(), hdrs, url


def fetch_with_retry(url: str, headers: dict | None = None, attempts: int = 3) -> tuple[int, bytes, dict, str]:
    delay = 15
    for attempt in range(1, attempts + 1):
        try:
            return fetch(url, headers)
        except RateLimited as rl:
            if rl.reset_epoch:
                wait = max(1, rl.reset_epoch - int(time.time()) + 2)
            else:
                wait = delay
            if attempt == attempts or wait > 900:
                raise
            print(f"  rate limited, sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)
            delay *= 2
        except (urllib.error.URLError, TimeoutError, TransientError, http.client.HTTPException, ConnectionError) as err:
            if attempt == attempts:
                raise
            print(f"  network error ({err}), retrying", file=sys.stderr)
            time.sleep(min(delay, 5))
    raise RuntimeError("unreachable")


# --------------------------------------------------------------------------- #
# Checkers
# --------------------------------------------------------------------------- #


def check_api(repo: str, token: str | None) -> dict:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    status, body, _, _ = fetch_with_retry(f"https://api.github.com/repos/{repo}", headers)
    if status == 404:
        return {"status": "missing", "source": "api"}
    if status != 200:
        return {"status": "error", "source": "api", "http_status": status}
    data = json.loads(body)
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
    status, feed, _, final_url = fetch_with_retry(f"https://github.com/{repo}/commits.atom")
    if status == 404:
        return {"status": "missing", "source": "web"}
    if status != 200:
        return {"status": "error", "source": "web", "http_status": status}
    updated = re.search(rb"<updated>([^<]+)</updated>", feed)
    last_activity = updated.group(1).decode() if updated else None

    resolved = re.match(r"^https?://github\.com/([^/]+/[^/]+)", final_url)
    resolved_repo = resolved.group(1) if resolved else repo

    status, page, _, _ = fetch_with_retry(f"https://github.com/{repo}")
    archived_match = re.search(rb'"isArchived":(true|false)', page) if status == 200 else None
    archived = archived_match.group(1) == b"true" if archived_match else None

    return {
        "status": "ok",
        "source": "web",
        "last_activity": last_activity,
        "archived": archived,
        "stars": None,
        "resolved_repo": resolved_repo,
    }


# --------------------------------------------------------------------------- #
# Evaluation and reporting
# --------------------------------------------------------------------------- #


def parse_iso(ts: str | None) -> dt.datetime | None:
    if not ts:
        return None
    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))


def evaluate(entry: dict, result: dict, now: dt.datetime, max_age_days: int) -> dict:
    row = {**entry, **result}
    reasons: list[str] = []
    last = parse_iso(result.get("last_activity"))
    row["age_days"] = (now - last).days if last else None

    if result.get("status") == "missing":
        reasons.append("repository not found (404)")
    elif result.get("status") == "error":
        reasons.append(f"could not check (HTTP {result.get('http_status')})")
    else:
        if result.get("archived"):
            reasons.append("archived")
        if result.get("disabled"):
            reasons.append("disabled")
        if row["age_days"] is not None and row["age_days"] > max_age_days:
            reasons.append(f"no activity for {row['age_days']} days")
        resolved = result.get("resolved_repo")
        if resolved and entry["repo"] and resolved.lower() != entry["repo"].lower():
            reasons.append(f"moved to {resolved}")

    row["reasons"] = reasons
    row["flagged"] = bool(reasons)
    return row


def md_table(rows: list[dict]) -> str:
    lines = [
        "| Entry | Section | Last activity | Age (days) | Why |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        last = (r.get("last_activity") or "")[:10]
        age = "" if r.get("age_days") is None else str(r["age_days"])
        lines.append(
            f"| [{r['name']}]({r['url']}) | {r['section']} | {last} | {age} | {'; '.join(r['reasons'])} |"
        )
    return "\n".join(lines)


def build_report(rows: list[dict], unchecked: list[dict], max_age_days: int, now: dt.datetime, source: str) -> str:
    flagged = [r for r in rows if r["flagged"]]
    healthy = [r for r in rows if not r["flagged"]]
    out = [
        f"# Activity report ({now:%Y-%m-%d})",
        "",
        f"Checked {len(rows)} GitHub-hosted entries via `{source}`; threshold {max_age_days} days.",
        "",
        f"## Flagged ({len(flagged)})",
        "",
    ]
    if flagged:
        out.append(md_table(sorted(flagged, key=lambda r: (r.get('age_days') or 0), reverse=True)))
    else:
        out.append("Nothing to report.")
    out += ["", f"## Healthy ({len(healthy)})", ""]
    out.append("<details><summary>Show</summary>\n")
    out.append(md_table(sorted(healthy, key=lambda r: r["name"].lower())) if healthy else "None.")
    out.append("\n</details>")
    if unchecked:
        out += ["", f"## Not on GitHub, check by hand ({len(unchecked)})", ""]
        out += [f"- [{e['name']}]({e['url']}) ({e['section']})" for e in unchecked]
    return "\n".join(out) + "\n"


def list_entries(readme: str, skip: set[str]) -> int:
    """Print parsed entries and fail if any repository appears more than once."""
    entries = parse_readme(readme, skip)
    by_repo: dict[str, list[dict]] = {}
    for entry in entries:
        print(f"{entry['line']:4d}  {entry['section']:<45} {entry['name']:<28} {entry['repo'] or entry['url']}")
        if entry["repo"]:
            by_repo.setdefault(entry["repo"].lower(), []).append(entry)
    duplicates = {repo: items for repo, items in by_repo.items() if len(items) > 1}
    github_count = sum(1 for e in entries if e["repo"])
    print(f"\n{len(entries)} entries, {github_count} on GitHub, {len(entries) - github_count} elsewhere", file=sys.stderr)
    if duplicates:
        for repo, items in duplicates.items():
            lines = ", ".join(str(i["line"]) for i in items)
            print(f"duplicate: {repo} listed on lines {lines}", file=sys.stderr)
        return 1
    return 0


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main(argv: list[str] | None = None) -> int:
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
    ap.add_argument("--list", action="store_true",
                    help="only parse the README: print entries, fail on repositories listed twice (no network)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    if args.list:
        return list_entries(args.readme, set(args.skip_section) if args.skip_section else set(DEFAULT_SKIP_SECTIONS))

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    mode = args.mode
    if mode == "auto":
        mode = "api" if token else "web"
    delay = args.delay if args.delay is not None else (0.0 if mode == "api" else 0.5)
    skip = set(args.skip_section) if args.skip_section else set(DEFAULT_SKIP_SECTIONS)

    entries = parse_readme(args.readme, skip)
    github_entries = [e for e in entries if e["repo"]]
    unchecked = [e for e in entries if not e["repo"]]
    now = dt.datetime.now(dt.timezone.utc)

    if not args.quiet:
        print(f"{len(github_entries)} GitHub entries to check ({mode} mode), {len(unchecked)} non-GitHub entries skipped",
              file=sys.stderr)

    rows: list[dict] = []
    seen: dict[str, dict] = {}
    for i, entry in enumerate(github_entries, 1):
        repo = entry["repo"]
        if repo.lower() in seen:
            result = seen[repo.lower()]
        else:
            if not args.quiet:
                print(f"[{i}/{len(github_entries)}] {repo}", file=sys.stderr)
            try:
                result = check_api(repo, token) if mode == "api" else check_web(repo)
            except RateLimited:
                print("Rate limit exhausted; aborting. Set GITHUB_TOKEN or try again later.", file=sys.stderr)
                return 2
            except Exception as err:  # noqa: BLE001 - we want to keep going
                result = {"status": "error", "source": mode, "http_status": None, "error": str(err)}
            seen[repo.lower()] = result
            if delay:
                time.sleep(delay)
        rows.append(evaluate(entry, result, now, args.max_age_days))

    flagged = [r for r in rows if r["flagged"]]
    report = build_report(rows, unchecked, args.max_age_days, now, mode)

    if args.report_path:
        with open(args.report_path, "w", encoding="utf-8") as fh:
            fh.write(report)
    if args.json_path:
        with open(args.json_path, "w", encoding="utf-8") as fh:
            json.dump({"generated": now.isoformat(), "mode": mode, "max_age_days": args.max_age_days,
                       "entries": rows, "unchecked": unchecked}, fh, indent=2)
    if not args.report_path and not args.quiet:
        print(report)
    else:
        print(f"flagged: {len(flagged)} of {len(rows)}", file=sys.stderr)

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as fh:
            fh.write(f"stale_count={len(flagged)}\n")

    if args.fail_on_stale and flagged:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
