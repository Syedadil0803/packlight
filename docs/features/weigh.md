# Token report (weigh)

## What it does
`/packlight-weigh` reads Claude Code transcripts for the project and reports tokens per session, per call
and per model, with tips. `--since YYYY-MM-DD` splits before/after.

## Rules
- Never prints message content. Stdlib-only Python.
- Pass `--project=` with "=".

## Where the code is
- `packlight/scripts/usage_report.py`

## Decisions (why)
- No STATUS.md yet → run without `--since`; that is the baseline.
- `--since` date: user's date, else setup's date in STATUS.md, else first git commit of docs/STATUS.md (file dates are unreliable).

## Tests
- `python3 packlight/scripts/usage_report.py --selftest`
- Run on 6 real projects.

## Open
- Windows and Linux transcript paths untested.
