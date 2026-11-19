# 🎒 packlight

**Travel light. Spend fewer tokens.**

A long chat is a heavy bag: Claude carries every earlier message on every step, and you pay for it
each time. About 98% of the tokens in a Claude Code session are that re-reading. packlight packs only
what the next job needs: one status page, one feature page, one job per session. Then it unpacks and
starts fresh.

```
                     before          after packlight
median per session   41.6M tokens →  8.8M tokens     (about 4.7x less)
tokens per call      368k         →  204k
```
*Measured on one real project over about 5 weeks so far: 56 sessions, before and after switching.
Measuring continues, and new optimizations keep coming. Run `/packlight-weigh` to get your own numbers.*

Built by **Mohammed Adil Syed**. Running the report across real client projects showed the same leaks every
time: the chat being re-read, 70-108k tokens spent before any work, and nearly all tokens on the most
expensive model. packlight is the set of habits that fixed it.

> **Works with:** Claude Code (tested). **Coming soon:** Codex and other coding agents. The docs it writes are
> plain Markdown, so any agent can read them; the commands and the token report are Claude Code only for now.

## Four commands

| Command | What you get |
|---|---|
| `/packlight` | Lean docs and session rules for the project in this folder. Records your "before" token cost. |
| `/packlight-new-project` | A new project, start to finish: interview → stack → hosting and monthly cost → docs → first feature. |
| `/packlight-weigh` | Token report: cost per session, setup cost, long sessions, model mix, plain tips. |
| `/packlight-unpack` | Tidies docs that drifted: trims, merges, splits, and checks every code path still exists. |

All four appear in the `/` menu. "pack light" or "lighten the load" works too.
packlight never commits: you review the files and commit them yourself.

## Which command when

| Where you are | Run | What happens |
|---|---|---|
| Starting fresh, empty folder | `/packlight-new-project` | Interview, stack, hosting and cost, then the docs. No report yet: no history. |
| Midway, code but no packlight docs | `/packlight` | Reads the code, writes the docs, records today's token cost as your "before". |
| Late, big project with old docs | `/packlight`, then `/packlight-unpack` | Same, but never overwrites: it writes its version beside yours for you to approve, then flags stale docs. Biggest visible saving. |
| Already on packlight, docs drifting | `/packlight-unpack` | Trims STATUS back to one screen, merges or splits pages, checks every path still exists. |
| Any time | `/packlight-weigh` | Token report. No switch date yet: a baseline. With one: before vs after. |

Plain `/packlight` picks for you: an empty folder goes the new-project way, code goes the setup way.

## What it writes

```
CLAUDE.md                  rules only, under 80 lines
docs/STATUS.md             one screen: Live · Uncommitted · Open follow-ups · Waiting on owner · Next · Later
docs/features/README.md    the register of feature pages
docs/features/<area>.md    What it does · Rules · Where the code is · Decisions (why) · Tests · Open
```

A session reads STATUS.md plus one feature page, not the whole repo history. STATUS.md lines are
replaced, never appended, so it stays one screen forever.

**Session rules** it puts in `CLAUDE.md`:
- One feature = one session; small work stays in the current one.
- At most 3 sessions at once, reused by clearing. (Running 30+ at once raised the daily total.)
- Clear at feature end. ~150k context is a checkpoint, not a wall: finish the step, write one hand-over
  line in STATUS.md, clear, and the fresh session carries on from it.
- The cheapest model that does the job: strongest for stack, architecture and security; mid for features
  and docs; fastest for reading code, drift checks and reports.
- Small tool output, no polling sessions, unused connectors off.

## New project, end to end

1. **Interview**, three short rounds: what you're building, who uses it, platforms, users at launch and in
   a year, logins / payments / uploads / AI, budget, free plans or paid, region and data rules, deadline, team skills.
2. **Stack** with a one-line reason per choice and one alternative, decided by data rules and region first,
   then team skills, then managed over self-run, then cost.
3. **Hosting and cost**: for each piece (web, API, database, files, email, AI, jobs) the vendor and plan,
   region, minimum size, free plan limits and when you outgrow them, and monthly cost at launch and at
   year one. Prices are looked up live when the agent can browse, otherwise marked as estimates.
4. **Docs**: `DECISIONS.md`, a hosting page, one page per day-one feature, and a STATUS "Next" that walks
   you from opening accounts to the first feature, one session each.

## The report

`/packlight-weigh` runs `scripts/usage_report.py` (Python 3.8+, standard library only) over your local
transcripts in `~/.claude/projects/`. It never prints message content.

```
All sessions
  sessions            42
  total tokens        610.3M
  median per session  8.4M
  setup per session   61.2k  (median first-call context)
  past 150.0k context  9 of 42 sessions
  cache_read           597.1M  97.8%

Tips
  - Each session starts at 61.2k before any work: trim CLAUDE.md, turn off unused connectors.
```
*(numbers made up)*

Run it directly with a before / after split:

```bash
python3 ~/.claude/skills/packlight/scripts/usage_report.py --since 2026-11-01
```

Options: `--project=<folder or path>` (keep the `=`, folder names start with `-`), `--since YYYY-MM-DD`, `--top N`, `--selftest`.

## Install

```bash
git clone https://github.com/Syedadil0803/packlight.git packlight-repo
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r packlight-repo/packlight ~/.claude/skills/
cp packlight-repo/commands/*.md ~/.claude/commands/
```

Check: `python3 ~/.claude/skills/packlight/scripts/usage_report.py --selftest` prints `selftest ok`.
Update: `git -C packlight-repo pull`, then run the two `cp` lines again.
For one project only, copy into `<project>/.claude/skills/` instead.

### Always-on mode (optional)

Nudges you to run `/packlight` in any project that isn't set up yet. Type `stop packlight` to turn it off, `start packlight` to turn it back on (applies to new chats). Add to `~/.claude/settings.json`:

```json
"hooks": {
  "SessionStart": [{ "matcher": "startup|resume|clear|compact",
    "hooks": [{ "type": "command", "command": "bash \"$HOME/.claude/skills/packlight/scripts/mode.sh\" start", "timeout": 5 }] }],
  "UserPromptSubmit": [{
    "hooks": [{ "type": "command", "command": "bash \"$HOME/.claude/skills/packlight/scripts/mode.sh\" prompt", "timeout": 5 }] }]
}
```

Check: `bash ~/.claude/skills/packlight/scripts/mode.sh --selftest` prints `selftest ok`. It prints nothing in a project that is set up (CLAUDE.md already holds the rules) and one nudge to run `/packlight` where there is no `docs/STATUS.md`. Only the whole message `stop packlight` or `start packlight` counts.

**Light on itself:** SKILL.md is a short menu; each command's steps live in their own file and load only when it runs.

## Coming soon

- Codex and other coding agents.
- A warning when a session passes ~150k context.

## Licence

MIT
