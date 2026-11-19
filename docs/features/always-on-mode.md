# Always-on mode

## What it does
A SessionStart hook prints one nudge to run `/packlight` when the project has no `docs/STATUS.md`, and
nothing in a set-up project. Typing exactly `stop packlight` turns it off, `start packlight` back on.

## Rules
- On by default. Off = the file `${CLAUDE_CONFIG_DIR:-~/.claude}/.packlight-off`.
- Only the whole message toggles it (case and a trailing . or ! ignored). Quoting the phrase never does.
- Applies to new chats; an open chat keeps what it loaded.
- Optional for users: they add the two hooks to `~/.claude/settings.json` (README "Always-on mode").

## Where the code is
- `packlight/scripts/mode.sh` (`start`, `prompt`, `--selftest`)
- README section "Always-on mode (optional)"

## Decisions (why)
- 19 Nov: hook prints only the not-set-up nudge. The rules already load from global and project CLAUDE.md;
  printing them again was a third copy every session (Fable review).
- 19 Nov: exact-message toggle. Substring matching turned packlight off when a review report quoted the phrase.
- Plain bash + grep/sed, no python3 or jq: runs on every prompt, so no extra startup and no missing-tool failure.
- Hooks in settings, not a plugin: packlight installs by copying a folder.
- One global flag (not per chat): simplest.

## Tests
- `bash packlight/scripts/mode.sh --selftest`: nudge when not set up, silent when set up (from a subfolder),
  phrase inside a longer or quoted message ignored, exact stop/start, flag written/removed, silent when off.

## Open
- No shipped status line; Adil's own `~/.claude/statusline.sh` shows `[PACKLIGHT]`.
