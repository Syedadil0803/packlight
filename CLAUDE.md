# packlight - rules

## Start of every session
1. Read docs/STATUS.md.
2. Read docs/features/README.md, then only the page for the feature you were given.
3. Read the code that page points to. Code and tests are the truth; fix a page that is wrong.

## End of every feature
- Update the feature page (what changed, decisions and why, tests) in the same commit as the code.
- Update docs/STATUS.md: replace lines, never append history.

## What this is
Open-source Claude Code skill (MIT, github.com/Syedadil0803/packlight) that cuts token use: sets up a
rules-only CLAUDE.md, a one-screen STATUS.md and one page per feature, plus a token usage report.
Users: Claude Code users. Local folder name (`lean-sessions`) differs from the repo name.

## Folders
| Folder | What | Branch now |
|---|---|---|
| `packlight/` | The skill: `SKILL.md` menu, one file per command, `scripts/` | always-on-mode (main is protected) |
| `commands/` | 3 shortcut commands copied to `~/.claude/commands/` | same |
| `docs/` | STATUS.md and feature pages | same |

Installed copy lives in `~/.claude/skills/packlight` and `~/.claude/commands/`. After a change, copy again
and check `diff -rq packlight ~/.claude/skills/packlight` is empty.

## Gates (run before saying done)
- `python3 packlight/scripts/usage_report.py --selftest` prints `selftest ok`
- `bash packlight/scripts/mode.sh --selftest` prints `selftest ok`

## Sessions and tokens
- Small work (a question, a read, one edit) stays in the current session or a subagent.
- One feature = one session. Group small fixes of the same area into it.
- At most 3 sessions at once, one per lane. Reuse a session by clearing it, don't open new ones.
- Clear at feature end. ~150k context is a checkpoint, not a wall: finish the current step, write one hand-over
  line in STATUS.md (done, half-done with file, next), then clear. Deep in a hard bug: finish it first.
- Model per task: strongest (e.g. Opus) for design, security, hard bugs; mid (e.g. Sonnet) for feature work;
  fastest (e.g. Haiku) for bulk reading and searching, as a subagent (it keeps big output out of the chat).
  Commits and small edits stay inline: a subagent's startup costs more than they do.
- Keep tool output small: tail logs, `git log -10`, read big files by section, grep before reading.
- No sessions that poll or loop waiting on something.
- Turn off MCP connectors this project does not use.

## Project rules
- `main` is protected: changes go through a PR. No force-push. No commit, push or release without Adil's yes.
- No Claude/AI co-author or attribution in commits, PRs, releases or docs.
- `usage_report.py` never prints message content and stays stdlib-only Python.
- Keep SKILL.md a short menu; command steps load only from their own file.
