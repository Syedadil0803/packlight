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

**Setup.** Asks four short questions (web / mobile / backend, who the users are, main features, repos and folders), reads
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
the input / output / cache split, top sessions, and a before / after split for a date. It never
prints message content.

## Install

```bash
git clone <this repo> packlight-repo
mkdir -p ~/.claude/skills
cp -r packlight-repo/packlight ~/.claude/skills/
```

For one project only, copy it to `<project>/.claude/skills/` instead.

## Use

In a project, ask Claude Code: "set up packlight" (or type `/packlight`). Review the files, then commit them yourself.

Token report, from the project folder:

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
