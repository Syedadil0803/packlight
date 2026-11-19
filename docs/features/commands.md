# Commands

## What it does
- `/packlight`: no code in the folder → new-project flow; code → setup (rules-only CLAUDE.md, STATUS.md, feature pages).
- `/packlight-new-project`: interview, stack, hosting and monthly cost, then the docs.
- `/packlight-unpack`: tidy drifted docs (line limits, history out of STATUS.md, path drift, old-doc candidates).

## Rules
- CLAUDE.md < 80 lines, STATUS.md < 60 lines. Never overwrite existing docs without a yes (`docs/packlight-proposed-<name>`).
- Never commit. Never open secret-looking files.

## Where the code is
- `packlight/SKILL.md` (menu), `packlight/setup.md`, `packlight/new-project.md`, `packlight/unpack.md`
- `commands/packlight-new-project.md`, `commands/packlight-unpack.md`, `commands/packlight-weigh.md`

## Decisions (why)
- One file per command so only the needed steps load (fewer tokens per run).
- Shortcut commands live in `~/.claude/commands/`, hidden from the skill list, so they cost no per-session tokens.

## Tests
- Scripted runs only: setup on Krisha website and K-Connect, unpack on copies of Dalal, OfferTag, Any-buddy, new-project on 2 made-up products.
- Unpack run for real on OfferTag 19 Nov (archive moves + STATUS rewrite).

## Open
- Not tested with a person answering the interviews.
- `/packlight-unpack` and `/packlight-new-project` not typed in a real session; check the 3 shortcuts show in the / menu.
