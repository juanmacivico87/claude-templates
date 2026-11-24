#!/usr/bin/env bash
# SessionStart hook: once a day, tell Claude when this week's (Monday) report is still pending.
set -u
REPORTS_DIR="$HOME/.claude/reports"
mkdir -p "$REPORTS_DIR"
today=$(date +%F)
# Monday of the current week (today if it is Monday).
monday=$(date -d "$today -$(( $(date +%u) - 1 )) days" +%F)
last_report=$(cat "$REPORTS_DIR/.last-report" 2>/dev/null || echo "0000-00-00")
last_notice=$(cat "$REPORTS_DIR/.last-notice" 2>/dev/null || echo "0000-00-00")

# Pending when the last report is older than this week's Monday; notify at most once per day.
if [[ "$last_report" < "$monday" && "$last_notice" != "$today" ]]; then
  echo "$today" > "$REPORTS_DIR/.last-notice"
  message="Weekly report pending (last one: $last_report). The user asked to receive every Monday a report with recommendations to work better with Claude Code. In your first reply of this session, tell them in one line (in Spanish). If their first message has no task (e.g. a greeting) or asks for the report, generate it right away with the weekly-report skill. If it brings another task, handle it first and then offer to generate the report."
  json_message=$(printf '%s' "$message" | python3 -c 'import json, sys; print(json.dumps(sys.stdin.read()))')
  printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' "$json_message"
fi
exit 0
