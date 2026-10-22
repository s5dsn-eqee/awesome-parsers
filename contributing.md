# Contributing

Thanks for helping keep this list useful. One entry per pull request keeps review fast.

## What qualifies

Before proposing a project, check that it:

1. Has had a commit or release in the last 24 months.
2. Has documentation beyond a README stub (an API reference, a guide, or a genuinely thorough README).
3. Is used by at least one notable downstream project, or is clearly the best option in its niche.

Projects that fail the first test can still be worth knowing about. They go in [graveyard.md](graveyard.md) with a one-line note on what replaced them, not in the readme.

Scope: things that parse. Parser combinators, parser generators, lexer generators, and libraries whose job is to turn a specific format or language into a tree or events. Full compilers, linters, and serialization frameworks are only listed when their parser is usable on its own.

## Entry format

```markdown
- [name](url) `Language` - One sentence that ends with a period.
```

- Use the name the project uses for itself. If two projects share a name, disambiguate with the owner (`BurntSushi/toml`, `goccy/go-yaml`).
- Link to the canonical source repository. GitHub is preferred because the monthly activity check only understands GitHub links; projects hosted elsewhere are listed for manual review in the report. Link to documentation only when there is no public repository.
- Tag the implementation language in backticks, main language first. If a project targets many languages (ANTLR, Kaitai Struct), tag the main ones and say "bindings for ..." in the description.
- Start the description with a capital letter, not with the project's own name, and end it with a period. Say what the project is and what sets it apart, without ranking it against other entries.
- Keep each repository to a single entry. The linter rejects duplicate links.
- Order within a section is by language, then by how widely used the project is. Put a new entry next to the ones it competes with.

## Where it goes

- The technique sections (combinators, PEG, LL and Earley, LR, incremental, lexers) are for general-purpose tools you build your own parser with.
- *Format Parsers* is for libraries that parse one data format. *Language Parsers* is for programming languages.
- A tool that supports several techniques goes under its primary one; mention the rest in the description.

## Graveyard policy

A workflow runs on the first of every month and opens an issue listing every GitHub-hosted entry whose repository is archived, gone, or has not been pushed to in two years. A maintainer then:

- moves confirmed entries to [graveyard.md](graveyard.md) with a note on the successor, or
- fixes the link if the project simply moved (to Codeberg, GitLab, a new organization), or
- leaves it alone if the quiet period is explained (for example, a project whose development happens on another branch).

Nothing is removed automatically. Graveyard entries keep their link so readers can still find them.

## Checks to run locally

```sh
# Formatting and structure rules for awesome lists
npx awesome-lint

# Parse the README and report repositories listed twice
python3 scripts/check_activity.py --list

# Activity report; set GITHUB_TOKEN to use the API instead of scraping
python3 scripts/check_activity.py --report report.md
```

The same checks run in CI on every pull request, together with a link checker that verifies every GitHub repository in the list still exists. Links to other hosts are not checked automatically.
