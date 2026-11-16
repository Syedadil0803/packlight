# Setup

For a project that already has code. (No code yet: use `new-project.md`.)

## 1. Ask (one message, short)
1. What is being built: web, mobile, backend, or a mix?
2. Who uses it?
3. The main features (a few words each).
4. Repos and folders, and which branch each uses (skip if it is one repo).

Skip any answer the code makes obvious. Don't ask anything else unless only the user can know it.
No one to ask (scripted run): answer from the code and put what only the owner knows under STATUS "Waiting on owner".
If an answer and the code disagree (say, branch names), write what the code shows and add the mismatch to STATUS.md "Open follow-ups".

## 2. Read the code, cheaply
- Read package manifests, README, top-level folders, CI config, existing CLAUDE.md and docs.
- List folders; open only entry files and route/screen indexes. Read big files by section.
- Find the real gate commands: build, lint, type check, test. Copy them exactly. A gate that can't run
  (tool missing, no config) still goes in, marked "broken", with a line in STATUS.md "Open follow-ups".
- Existing CLAUDE.md or docs: keep what is true, move state out of CLAUDE.md into STATUS.md,
  move feature detail into feature pages. Never overwrite without the user's yes: write your version
  as `docs/packlight-proposed-<name>` and show the difference.
- Several repos under one folder: the root CLAUDE.md holds shared rules; each repo's own CLAUDE.md keeps
  only repo rules (its gates, conventions). List repeats, conflicts and stale lines in the repo files under
  STATUS "Open follow-ups" and propose edits; don't edit them without a yes.
- Where the docs live: one repo - inside it, so they are committed with the code. Repo in a subfolder or
  several repos under a plain folder - at that folder; note in CLAUDE.md that docs/ is not in git and ask
  the user whether to move it into a repo.
- Generated files committed to the repo (sitemaps, lockfiles, API clients): note "don't hand-edit".
- Secret-looking files or folders (`secrets/`, `keys/`, `.env*`): never open them; add a project rule
  that sessions don't either, and ask the user to confirm they are gitignored.

## 3. Write the files

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
| Folder | What | Branch now |      (one row per top-level folder; mark folders that are not part of the project)

## Gates (run before saying done)
<exact commands, grouped per repo>


## Sessions and tokens
- Small work (a question, a read, one edit) stays in the current session or a subagent.
- One feature = one session. Group small fixes of the same area into it.
- At most 3 sessions at once, one per lane. Reuse a session by clearing it, don't open new ones.
- Clear at feature end. ~150k context is a checkpoint, not a wall: finish the current step, write one hand-over
  line in STATUS.md (done, half-done with file, next), then clear. Deep in a hard bug: finish it first.
- Model per task: strongest (e.g. Opus) for design, security, hard bugs; mid (e.g. Sonnet) for feature work;
  fastest (e.g. Haiku) for reading, searching, docs, commits. Hand bulk reading to a subagent on a cheaper model.
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
One page per area that has code; a small project may have only 2-3, don't pad. In an existing project,
planned features with no code get a line in STATUS.md "Next" or "Later", and a page when work starts
(a new project gets a page per day-one feature, see `new-project.md`). Merge tiny areas; split a page past ~150 lines.

## 4. Optional docs - only when the project needs them now
- `docs/DECISIONS.md` - decisions that span areas.
- `docs/change-requests.md` - client asks with date and status.
- `docs/meetings/` - one file per meeting.
- `docs/RUNBOOK.md` - deploy and ops steps.
- `docs/security/<YYYY-MM-DD>/` - review reports.
- `docs/reference/` - specs, API docs from others.
- `docs/manual-tasks.md` - things only a person can do.
- `docs/HANDOVER.md` - when someone else takes over.
- `docs/archive/` - old docs that no longer match the code.

## 5. Finish
- Print a short list of files written and line counts. Check CLAUDE.md < 80 and STATUS.md < 60 lines.
- Don't commit. Tell the user what to review, plus any open questions (project rules, mismatches).
- Record the baseline: run `/packlight-weigh` now and show the numbers (the "without packlight" cost).
  Add to STATUS.md "Next": `<today + 7 days>: /packlight-weigh --since <today>` to see the saving.
