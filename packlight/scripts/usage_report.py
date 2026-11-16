#!/usr/bin/env python3
"""Token usage per Claude Code session, read from local transcripts.

Reads ~/.claude/projects/<folder>/**/*.jsonl and prints totals only.
It never prints message content.

  python3 usage_report.py                      # project for the current folder
  python3 usage_report.py --project=DIR        # a folder under ~/.claude/projects, or a full path
                                               # (use "=": those folder names start with "-")
  python3 usage_report.py --since 2026-11-01   # split sessions before / after a date
  python3 usage_report.py --selftest
"""
import argparse
import json
import os
import re
import statistics
import sys
from pathlib import Path

KINDS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
SHORT = ("input", "output", "cache_write", "cache_read")
LONG = 150_000  # context size at which a session should be cleared


def read_lines(paths):
    for path in paths:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    yield path, json.loads(line)
                except ValueError:
                    continue


def collect(paths):
    """Return {session_id: {"start": ts, "calls": {msg_id: usage}}}."""
    sessions = {}
    for path, d in read_lines(paths):
        if not isinstance(d, dict) or d.get("type") != "assistant":
            continue
        msg = d.get("message") or {}
        usage = msg.get("usage")
        if not usage or not msg.get("id"):
            continue
        # Subagent files carry the parent's sessionId, so they count toward the parent.
        sid = d.get("sessionId") or Path(path).stem
        s = sessions.setdefault(sid, {"start": None, "calls": {}})
        ts = d.get("timestamp")
        if ts and (s["start"] is None or ts < s["start"]):
            s["start"] = ts
        # A streamed reply is logged several times under one id; keep the last copy.
        c = {k: int(usage.get(k) or 0) for k in KINDS}
        c.update(ts=ts or "", model=msg.get("model") or "?", side=bool(d.get("isSidechain")))
        s["calls"][msg["id"]] = c
    return sessions


def summarize(sessions):
    rows = []
    for sid, s in sessions.items():
        calls = s["calls"].values()
        sums = {k: sum(c[k] for c in calls) for k in KINDS}
        # Context size of a call = everything it read; output is excluded.
        main = sorted((c for c in calls if not c["side"]), key=lambda c: c["ts"]) or list(calls)
        ctx = [c["input_tokens"] + c["cache_creation_input_tokens"] + c["cache_read_input_tokens"] for c in main]
        models = {}
        for c in calls:
            models[c["model"]] = models.get(c["model"], 0) + sum(c[k] for k in KINDS)
        rows.append({"id": sid, "start": (s["start"] or "")[:10], "calls": len(s["calls"]),
                     "total": sum(sums.values()), "setup": ctx[0], "peak": max(ctx), "models": models, **sums})
    return rows


def fmt(n):
    for unit, size in (("B", 1e9), ("M", 1e6), ("k", 1e3)):
        if abs(n) >= size:
            return f"{n / size:.1f}{unit}"
    return str(int(n))


def block(title, rows):
    if not rows:
        print(f"\n{title}: no sessions")
        return
    total = sum(r["total"] for r in rows)
    calls = sum(r["calls"] for r in rows)
    print(f"\n{title}")
    print(f"  sessions            {len(rows)}")
    print(f"  model calls         {calls}")
    print(f"  total tokens        {fmt(total)}")
    print(f"  median per session  {fmt(statistics.median(r['total'] for r in rows))}")
    print(f"  per model call      {fmt(total / calls) if calls else 0}")
    print(f"  setup per session   {fmt(statistics.median(r['setup'] for r in rows))}  (median first-call context)")
    long_ = [r for r in rows if r["peak"] > LONG]
    print(f"  past {fmt(LONG)} context  {len(long_)} of {len(rows)} sessions")
    for k, name in zip(KINDS, SHORT):
        part = sum(r[k] for r in rows)
        print(f"  {name:<19} {fmt(part):>7}  {100 * part / total if total else 0:.1f}%")


def model_mix(rows):
    mix = {}
    for r in rows:
        for m, n in r["models"].items():
            mix[m] = mix.get(m, 0) + n
    return {m: n for m, n in sorted(mix.items(), key=lambda x: -x[1]) if m != "<synthetic>"}


def tips(rows):
    """Plain-language hints from the numbers."""
    out = []
    setup = statistics.median(r["setup"] for r in rows)
    if setup > 50_000:
        out.append(f"Each session starts at {fmt(setup)} before any work: trim CLAUDE.md, turn off unused connectors.")
    long_ = sum(r["peak"] > LONG for r in rows)
    if long_ > len(rows) / 4:
        out.append(f"{long_} of {len(rows)} sessions ran past {fmt(LONG)} context: clear at feature end or ~150k.")
    total = sum(r["total"] for r in rows)
    mix = model_mix(rows)
    top = sum(n for m, n in mix.items() if "opus" in m.lower())
    if total and top / total > 0.8:
        out.append(f"{100 * top / total:.0f}% of tokens on the strongest model: route routine work to a cheaper one.")
    reads = sum(r["cache_read_input_tokens"] for r in rows)
    if total and reads / total > 0.95 and statistics.median(r["total"] for r in rows) > 20_000_000:
        out.append("Most tokens are the chat being re-read: shorter sessions save the most.")
    return out or ["Nothing stands out. Sessions look lean."]


def report(rows, since=None, top=10):
    block("All sessions", rows)
    if since:
        block(f"Before {since}", [r for r in rows if r["start"] < since])
        block(f"From {since}", [r for r in rows if r["start"] >= since])
    total = sum(r["total"] for r in rows)
    print("\nBy model (all sessions)")
    for m, n in model_mix(rows).items():
        print(f"  {m[:28]:<28} {fmt(n):>7}  {100 * n / total if total else 0:.1f}%")
    print(f"\nTop {top} sessions")
    print(f"  {'session':<10} {'started':<10} {'calls':>6} {'total':>8} {'per call':>9} {'peak':>7}")
    for r in sorted(rows, key=lambda r: -r["total"])[:top]:
        per = fmt(r["total"] / r["calls"]) if r["calls"] else "0"
        print(f"  {r['id'][:8]:<10} {r['start']:<10} {r['calls']:>6} {fmt(r['total']):>8} {per:>9} {fmt(r['peak']):>7}")
    recent = [r for r in rows if r["start"] >= since] if since else rows
    print("\nTips" + (f" (from {since})" if since else ""))
    for t in tips(recent or rows):
        print(f"  - {t}")


def project_dirs(arg):
    """The project's transcript folder plus those of its subfolders and worktrees."""
    root = Path.home() / ".claude" / "projects"
    if arg:
        p = Path(arg).expanduser()
        base = p if p.is_dir() else root / arg
    else:
        # Claude Code names the folder after the working directory, non-alphanumerics as "-".
        base = root / re.sub(r"[^A-Za-z0-9]", "-", os.getcwd())
    # ponytail: name-prefix match, so a sibling folder like "app-old" next to "app" is counted too.
    return [base] + sorted(d for d in base.parent.glob(base.name + "-*") if d.is_dir())


def selftest():
    import tempfile

    def line(sid, mid, ts, out, read):
        u = {"input_tokens": 10, "output_tokens": out, "cache_creation_input_tokens": 100,
             "cache_read_input_tokens": read}
        return json.dumps({"type": "assistant", "sessionId": sid, "timestamp": ts,
                           "message": {"id": mid, "usage": u, "content": "SECRET"}})

    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "a.jsonl").write_text("\n".join([
            line("a", "m1", "2026-01-01T00:00:00Z", 5, 1000),
            line("a", "m1", "2026-01-01T00:00:01Z", 50, 1000),  # same call, streamed again
            line("a", "m2", "2026-01-01T00:01:00Z", 20, 2000),
            json.dumps({"type": "user", "message": {"content": "SECRET"}}),
            "not json",
        ]))
        sub = Path(tmp, "a", "subagents")
        sub.mkdir(parents=True)
        (sub / "x.jsonl").write_text(line("a", "m3", "2026-01-01T00:02:00Z", 1, 500))
        Path(tmp, "b.jsonl").write_text(line("b", "m9", "2026-02-01T00:00:00Z", 1, 1))
        rows = {r["id"]: r for r in summarize(collect(sorted(Path(tmp).rglob("*.jsonl"))))}
    assert set(rows) == {"a", "b"}, rows
    a = rows["a"]
    assert a["calls"] == 3, a
    assert a["output_tokens"] == 71, a  # 50 (last copy of m1) + 20 + 1
    assert a["cache_read_input_tokens"] == 3500, a
    assert a["total"] == 30 + 71 + 300 + 3500, a
    assert a["start"] == "2026-01-01", a
    assert a["setup"] == 10 + 100 + 1000 and a["peak"] == 10 + 100 + 2000, a
    assert fmt(1_234_567) == "1.2M" and fmt(999) == "999"
    assert tips([a]) == ["Nothing stands out. Sessions look lean."]
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", help="folder name under ~/.claude/projects, or a full path")
    ap.add_argument("--since", help="YYYY-MM-DD; split sessions by start date")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.since and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.since):
        sys.exit("--since must be YYYY-MM-DD")
    dirs = [d for d in project_dirs(args.project) if d.is_dir()]
    paths = sorted(p for d in dirs for p in d.rglob("*.jsonl"))
    if not paths:
        sys.exit("No transcripts found for this folder. Pass --project.")
    print(f"Read {len(dirs)} transcript folder(s): the project, its subfolders and worktrees")
    report(summarize(collect(paths)), args.since, args.top)


if __name__ == "__main__":
    main()
