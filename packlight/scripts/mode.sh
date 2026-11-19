#!/usr/bin/env bash
# Packlight always-on mode. On by default. Plain bash, no python or jq.
# The whole message "stop packlight" turns it off (flag file); "start packlight" turns it back on.
# The rules themselves live in CLAUDE.md; this hook only nudges when a project is not set up yet.
# Usage: mode.sh start (SessionStart hook) | mode.sh prompt (UserPromptSubmit hook) | mode.sh --selftest
off="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/.packlight-off"

if [ "$1" = "--selftest" ]; then
  t=$(mktemp -d); s="$0"; fail=0; mkdir -p "$t/setup/docs" "$t/setup/sub" "$t/bare"; touch "$t/setup/docs/STATUS.md"
  run() { CLAUDE_CONFIG_DIR="$t" bash "$s" "$@"; }
  chk() { [ "$1" = 1 ] || { echo "FAIL: $2"; fail=1; }; }
  echo "{\"cwd\":\"$t/bare\"}" | run start | grep -q "/packlight"; chk $(( ! $? )) "nudge in a project not set up"
  [ -z "$(echo "{\"cwd\":\"$t/setup/sub\"}" | run start)" ]; chk $(( ! $? )) "silent in a set-up project (from a subfolder)"
  [ -z "$(echo '{"prompt":"pls stop packlight now"}' | run prompt)" ]; chk $(( ! $? )) "phrase inside a longer message ignored"
  [ -z "$(echo '{"prompt":"the hook said \"stop packlight\""}' | run prompt)" ]; chk $(( ! $? )) "quoted phrase ignored"
  echo '{"session_id":"x","prompt":" Stop Packlight. "}' | run prompt | grep -q OFF; chk $(( ! $? )) "exact stop"
  [ -f "$t/.packlight-off" ]; chk $(( ! $? )) "flag written"
  [ -z "$(echo "{\"cwd\":\"$t/bare\"}" | run start)" ]; chk $(( ! $? )) "silent when off"
  echo '{"prompt":"start packlight"}' | run prompt | grep -q ON; chk $(( ! $? )) "exact start"
  [ ! -f "$t/.packlight-off" ]; chk $(( ! $? )) "flag removed"
  rm -rf "$t"; [ $fail = 0 ] && echo "selftest ok"; exit $fail
fi

input=$(cat)

if [ "$1" = "prompt" ]; then
  # Only the whole message counts, so quoting the phrase or pasting docs never flips it.
  ws='[[:space:]]*'
  if printf '%s' "$input" | grep -Eiq "\"prompt\"$ws:$ws\"$ws(stop) packlight$ws[.!]?$ws\""; then
    touch "$off"; echo "Packlight mode is now OFF for new chats. Say \"start packlight\" to turn it back on."
  elif printf '%s' "$input" | grep -Eiq "\"prompt\"$ws:$ws\"$ws(start) packlight$ws[.!]?$ws\""; then
    rm -f "$off"; echo "Packlight mode is now ON for new chats."
  fi
  exit 0
fi

[ -f "$off" ] && exit 0
d=$(printf '%s' "$input" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
[ -n "$d" ] || d=$PWD
while [ -n "$d" ] && [ "$d" != "/" ]; do
  [ -f "$d/docs/STATUS.md" ] && exit 0
  d=$(dirname "$d")
done
echo "PACKLIGHT: this project has no docs/STATUS.md yet. Suggest /packlight once if the user starts real work here; don't push. (Turn off: \"stop packlight\".)"
