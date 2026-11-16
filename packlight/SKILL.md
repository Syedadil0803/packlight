---
name: packlight
description: Set up a project's docs so Claude Code sessions stay short and cheap - a rules-only CLAUDE.md, a one-screen docs/STATUS.md, and one docs/features page per area - plus session rules (one feature per session, clear early, small tool output) and a token usage report. Use when the user says "set up packlight", "set up project docs", "make sessions cheaper", "cut token use", or "how many tokens did this project use".
---

# packlight

Most tokens in a long Claude Code session are cache reads: the whole chat is re-read on every step.
Short sessions that start from a small, current set of docs cost far less. This skill writes those docs
and the rules that keep sessions short.

Two jobs:
- **Setup** - write the docs for a project (below).
- **Report** - show token use: `python3 <this skill folder>/scripts/usage_report.py [--since YYYY-MM-DD]`.
  Run it from the project folder. It prints totals only, never message content.

## Setup

### 1. Ask (one message, short)
1. What is being built: web, mobile, backend, or a mix?
2. Who uses it?
3. The main features (a few words each).
4. Repos and folders, and which branch each uses (skip if it is one repo).

Skip any answer the code makes obvious. Don't ask anything else unless only the user can know it.
If an answer and the code disagree (say, branch names), write what the code shows and add the mismatch to STATUS.md "Open follow-ups".

### 2. Read the code, cheaply
- Read package manifests, README, top-level folders, CI config, existing CLAUDE.md and docs.
- List folders; open only entry files and route/screen indexes. Read big files by section.
- Find the real gate commands: build, lint, type check, test. Copy them exactly. A gate that can't run
  (tool missing, no config) still goes in, marked "broken", with a line in STATUS.md "Open follow-ups".
- Existing CLAUDE.md or docs: keep what is true, move state out of CLAUDE.md into STATUS.md,
  move feature detail into feature pages. Show the user what will change before overwriting.

### 3. Write the files

**`CLAUDE.md`** - rules only, under 80 lines. No state, no history, no feature detail.
```
# <Project> - rules

## Start of every session
1. Read docs/STATUS.md.
2. Read docs/features/README.md, then only the page for the feature you were given.
3. Read the code that page points to. Code and tests are the truth; fix a page that is wrong.

## End of every feature
- Update the feature page (what changed, decisions and why, tests) in the same commit as the code.
- Update docs/STATUS.md: replace lines, never append history.

## What this is
<2-3 lines: product, users, platforms.>

## Folders
| Folder | What | Branch |      (one row per top-level folder that holds code or docs)

## Gates (run before saying done)
<exact commands per repo>

## Sessions and tokens
- Small work (a question, a read, one edit) stays in the current session or a subagent.
- One feature = one session. Group small fixes of the same area into it.
- At most 3 sessions at once, one per lane. Reuse a session by clearing it, don't open new ones.
- Clear at feature end or at ~150k context. Before a mid-feature clear, write one hand-over line in STATUS.md.
- Use a cheaper model for routine work (commits, docs, small fixes, forms); the strongest for design, security, hard bugs.
- Keep tool output small: tail logs, `git log -10`, read big files by section, grep before reading.
- No sessions that poll or loop waiting on something.
- Turn off MCP connectors this project does not use.

## Project rules
<only rules the code can't show: what never to do, who approves deploys, data rules>
```
Don't invent project rules. Write only ones the user stated or the code/docs already enforce; if none, leave
`- (none yet)` and ask the user in step 5.

**`docs/STATUS.md`** - state only, under 60 lines, one screen. Replace lines; never append history.
```
# Status
## Live
## Uncommitted
## Open follow-ups
## Waiting on owner
## Next
## Later
```
Fill a heading only from evidence (git status, TODOs, open branches, deploy config, the user's answers).
No evidence: leave it empty. "Waiting on owner" means waiting on the person who runs the project.

**`docs/features/README.md`** - the register: one row per page.
```
| Area | Page | One line |
```

**`docs/features/<area>.md`** - one per product feature or cross-cutting area (auth, payments, api,
deploy, design...). Kebab-case names. Newest first inside each section.
```
# <Area>
## What it does
## Rules
## Where the code is      (paths, main functions; no code pasted)
## Decisions (why)
## Tests                  (file paths and the command to run them)
## Open
```
One page per area that has code; a small project may have only 2-3, don't pad. Planned features with no
code get a line in STATUS.md "Next" or "Later", and a page when work starts. Merge tiny areas; split a page past ~150 lines.

### 4. Optional docs - only when the project needs them now
- `docs/DECISIONS.md` - decisions that span areas.
- `docs/change-requests.md` - client asks with date and status.
- `docs/meetings/` - one file per meeting.
- `docs/RUNBOOK.md` - deploy and ops steps.
- `docs/security/<YYYY-MM-DD>/` - review reports.
- `docs/reference/` - specs, API docs from others.
- `docs/manual-tasks.md` - things only a person can do.
- `docs/HANDOVER.md` - when someone else takes over.
- `docs/archive/` - old docs that no longer match the code.

### 5. Finish
- Print a short list of files written and line counts. Check CLAUDE.md < 80 and STATUS.md < 60 lines.
- Don't commit. Tell the user what to review, plus any open questions (project rules, mismatches).
- Suggest running the report now and again in a week with `--since <today>` to see the change.

## Keeping it lean afterwards
- Each session reads STATUS.md + one feature page, not the whole docs folder.
- STATUS.md is rewritten, not appended. Finished work leaves STATUS.md and lives in the feature page.
- If a page and the code disagree, the code wins; fix the page in the same change.
