# packlight

A Claude Code skill that cuts token use and speeds up sessions. Pack light: every session starts from
a small, current set of docs (one status page and one feature page) instead of a long chat history.

## Why

About 98% of the tokens in a Claude Code session are cache reads: the chat is re-read on every step.
So a long chat gets more expensive with every message. The fix is short sessions that start from a small, up-to-date set of docs
instead of a long chat history.

Measured on one real project (several months, one developer), before and after switching:

| | Long chat sessions | One feature per session |
|---|---|---|
| Median tokens per session | ~40M | ~7M |
| Tokens per model call | ~338k | ~200k |
| Fixed setup per session | ~60k | ~60k |

The other lesson: running 30+ sessions at once still raised the daily total. So the rules also cap
open sessions at 3 and reuse them by clearing.

## What it does

**New project.** In an empty folder it runs a short guided interview (what you're building, who uses it,
platforms, expected users, logins / payments / uploads / AI, budget, region and data rules, deadline, team
skills), suggests a stack with a one-line reason per choice and one alternative, and records your pick in
`docs/DECISIONS.md`. Then it writes the docs below.

**Existing project.** Asks four short questions (web / mobile / backend, who the users are, main features, repos and folders), reads
the code, then writes:

- `CLAUDE.md` - rules only, under 80 lines, including the session rules below.
- `docs/STATUS.md` - state only, one screen: Live · Uncommitted · Open follow-ups · Waiting on owner · Next · Later. Lines are replaced, never appended.
- `docs/features/README.md` - a register of feature pages.
- `docs/features/<area>.md` - one per feature or cross-cutting area: What it does · Rules · Where the code is · Decisions (why) · Tests · Open.
- Optional docs (runbook, decisions, meetings...) only when the project needs them.

**Session rules** written into `CLAUDE.md`:
- Small work stays in the current session; one feature = one session.
- At most 3 sessions at once, reused by clearing.
- Clear at feature end or ~150k context, with a hand-over line in STATUS.md.
- Cheaper model for routine work.
- Small tool output: tail logs, read big files by section.
- No polling sessions; turn off unused connectors.

**Report.** `scripts/usage_report.py` (Python 3.8+, standard library only) reads your local transcripts in
`~/.claude/projects/` and prints sessions, total tokens, median per session, tokens per model call,
the input / output / cache split, setup cost per session (context before any work), how many sessions
ran past 150k context, tokens by model, top sessions, a before / after split for a date, and plain tips
("turn off unused connectors", "clear earlier", "route routine work to a cheaper model"). It never
prints message content.

**Model per task.** The skill tells Claude which model tier each job needs: strongest for stack choice,
architecture and security; mid for writing docs and features; fastest for reading code, drift checks and
reports. Bulk reading goes to a subagent on a cheaper model.

**Light on itself.** SKILL.md is a short menu; setup, new-project and unpack steps live in their own files and
load only when that command runs.

## Install

```bash
git clone https://github.com/Syedadil0803/packlight.git packlight-repo
mkdir -p ~/.claude/skills
cp -r packlight-repo/packlight ~/.claude/skills/
mkdir -p ~/.claude/commands
cp packlight-repo/commands/*.md ~/.claude/commands/   # optional: /packlight-weigh, -new, -unpack in the menu
```

For one project only, copy it to `<project>/.claude/skills/` instead.

To update later: `git -C packlight-repo pull`, then run the `cp` line again.

Check it works: `python3 ~/.claude/skills/packlight/scripts/usage_report.py --selftest` prints `selftest ok`.

## Use

| Command | What it does |
|---|---|
| `/packlight` | Sets up the docs. Spots by itself whether the project is new or existing. |
| `/packlight new` | New project: guided interview, stack suggestion, then the docs. |
| `/packlight weigh` | Weighs your bag: token report for this project. |
| `/packlight unpack` | Tidies an existing setup: trims STATUS.md, merges tiny pages, fixes pages that drifted from the code. |

The shortcuts `/packlight-weigh`, `/packlight-new` and `/packlight-unpack` do the same and show up in the `/` menu.
Saying "pack light" or "lighten the load" works too. Packlight never commits; review the files and commit them yourself.

The report can also be run directly, from the project folder:

```bash
python3 ~/.claude/skills/packlight/scripts/usage_report.py --since 2026-11-01
```

Example output (numbers made up):

```
All sessions
  sessions            42
  model calls         9120
  total tokens        610.3M
  median per session  8.4M
  per model call      66.9k
  input                  0.3M  0.1%
  output                 2.1M  0.3%
  cache_write           10.8M  1.8%
  cache_read           597.1M  97.8%

Top 10 sessions
  session    started     calls    total  per call
  3f2a91c0   2026-10-12   1204    96.0M     79.7k
```

Options: `--project=<folder or path>` (keep the `=`, folder names start with `-`), `--since YYYY-MM-DD`, `--top N`, `--selftest`.

## Licence

MIT
