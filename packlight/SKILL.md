---
name: packlight
description: Keep Claude Code sessions short and cheap. Sets up a rules-only CLAUDE.md, a one-screen docs/STATUS.md and one docs/features page per area, guides the stack for a new project, tidies drifted docs, and reports token use per session. Use when the user types /packlight or says "pack light", "lighten the load", "set up packlight", or asks for a token usage report for this project.
argument-hint: "[new | weigh | unpack]"
---

# packlight

Most tokens in a long session are the chat being re-read on every step. Short sessions that start from
a small, current set of docs cost far less. Load only the file the command needs.

| Command | Do this |
|---|---|
| `/packlight` | No code in the folder: read `new-project.md`. Code: read `setup.md`. |
| `/packlight new` | Read `new-project.md`, even if a few files exist. |
| `/packlight weigh` | Run `python3 <this skill folder>/scripts/usage_report.py` from the project folder (no other file needed). For a before/after split add `--since YYYY-MM-DD`: the date the user gives, else the first git commit of docs/STATUS.md; with no git, ask the user (file dates are unreliable). Show the numbers and the script's tips. It never prints message content. |
| `/packlight unpack` | Read `unpack.md`. |

## Model per task
Use the cheapest model that does the job well. When this session runs on a stronger model than a step
needs, hand that step to a subagent on the cheaper model and keep only its summary.

| Work | Model tier (current example) |
|---|---|
| Stack choice, architecture, security, hard bugs | Strongest (Opus) |
| Interview, writing CLAUDE.md and feature pages, feature work, reviews | Mid (Sonnet) |
| Reading and searching code, drift checks, line counts, `weigh`, commits, small doc edits | Fastest (Haiku) |

## Keeping it lean afterwards
- Each session reads STATUS.md + one feature page, not the whole docs folder.
- STATUS.md is rewritten, not appended. Finished work leaves STATUS.md and lives in the feature page.
- If a page and the code disagree, the code wins; fix the page in the same change.
