#!/usr/bin/env python3
"""Summarize the Claude Code transcripts of the last N days into a compact JSON.

Usage: python3 extract.py [days=7] > summary.json
Reads ~/.claude/projects/*/*.jsonl (main sessions) and counts each session's subagents.
Only records within the time window are counted, so long sessions are trimmed.
"""
import collections
import glob
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 7
PROJECTS_DIR = os.path.expanduser("~/.claude/projects")
CUTOFF_EPOCH = time.time() - DAYS * 86400
CUTOFF_ISO = datetime.fromtimestamp(CUTOFF_EPOCH, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
MAX_PROMPT_CHARS = 300
# Programs whose subcommand is worth keeping (e.g. "git diff" instead of just "git").
PROGRAMS_WITH_SUBCOMMAND = ("git", "docker", "npm", "composer", "drush", "ddev", "npx", "php", "lando",
                            "gh", "glab", "pnpm", "yarn", "ng", "nx")
SHELL_PREFIXES = ("do", "then", "else", "time", "sudo", "(", "{")
SHELL_NOISE = ("cd", "done", "fi", "for", "while", "if", "echo", "export", "}", ")", "true")
# The user writes in Spanish, so corrections are detected with Spanish phrases.
CORRECTION_PATTERN = re.compile(
    r"^\s*(no[ ,.!]|eso no|mal|te he dicho|otra vez|de nuevo|sigue sin|sigue fallando|no funciona|vuelve a)", re.I)


def user_text(content):
    """Return the plain text of a user message, whatever its content format."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def bash_programs(command):
    """Return the real program of each segment (&&, ;, |), ignoring cd, assignments, heredocs and flow control."""
    programs = []
    command = re.sub(r"<<-?\s*['\"]?(\w+)['\"]?.*?\n.*?\n\s*\1\s*(\n|$)", "\n", command, flags=re.S)
    command = re.sub(r"'[^']*'|\"[^\"]*\"", "''", command)
    for segment in re.split(r"&&|\|\||;|\||\n", command):
        words = [w for w in segment.strip().split() if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", w)]
        while words and words[0] in SHELL_PREFIXES:
            words = words[1:]
        if not words or words[0] in SHELL_NOISE:
            continue
        program = os.path.basename(words[0])
        if not re.match(r"^[A-Za-z][\w.+-]*$", program):
            continue
        has_subcommand = program in PROGRAMS_WITH_SUBCOMMAND and len(words) > 1
        programs.append(f"{program} {words[1]}" if has_subcommand else program)
    return set(programs)


def project_root(cwd, transcript_dir):
    """Return the project path for a session.

    The cwd may be a subfolder the session moved into, so walk up its ancestors until one
    encodes to the transcript folder name (Claude Code replaces every non-alphanumeric char with '-').
    """
    if not cwd:
        return None
    candidate = cwd
    while True:
        if re.sub(r"[^A-Za-z0-9]", "-", candidate) == transcript_dir:
            return candidate
        parent = os.path.dirname(candidate)
        if parent == candidate:
            return cwd
        candidate = parent


def summarize_session(path):
    """Build the summary of one session transcript."""
    session = {
        "project": None, "start": None, "end": None, "models": collections.Counter(),
        "prompts": [], "slash_commands": collections.Counter(), "skills": collections.Counter(),
        "tools": collections.Counter(), "bash": collections.Counter(), "mcp": collections.Counter(),
        "tool_errors": 0, "permission_denials": [], "interruptions": 0, "compactions": 0,
        "turn_duration_ms": 0, "edited_files": collections.Counter(), "corrections": 0,
        "pasted_images": 0,
    }
    for line in open(path, errors="ignore"):
        try:
            record = json.loads(line)
        except ValueError:
            continue
        record_type, timestamp = record.get("type"), record.get("timestamp")
        # Take the cwd even from records outside the window: it is only used to locate the project.
        if record.get("cwd") and not session["project"]:
            session["project"] = record["cwd"]
        if timestamp and timestamp < CUTOFF_ISO:
            continue
        if timestamp:
            session["start"] = session["start"] or timestamp
            session["end"] = timestamp

        if record_type == "system":
            subtype = record.get("subtype")
            if subtype == "compact_boundary":
                session["compactions"] += 1
            elif subtype == "turn_duration":
                session["turn_duration_ms"] += int(record.get("durationMs") or 0)

        elif record_type == "assistant":
            message = record.get("message", {})
            if message.get("model"):
                session["models"][message["model"]] += 1
            for block in message.get("content") or []:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                tool, tool_input = block.get("name", "?"), block.get("input") or {}
                if tool.startswith("mcp__"):
                    session["mcp"][tool.split("__")[1]] += 1
                    tool = "mcp"
                session["tools"][tool] += 1
                if tool == "Bash":
                    for program in bash_programs(tool_input.get("command") or ""):
                        session["bash"][program] += 1
                elif tool == "Skill":
                    session["skills"][tool_input.get("skill", "?")] += 1
                elif tool in ("Edit", "Write", "MultiEdit"):
                    session["edited_files"][tool_input.get("file_path", "?")] += 1

        elif record_type == "user":
            content = record.get("message", {}).get("content")
            if isinstance(content, list):
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "tool_result" and block.get("is_error"):
                        session["tool_errors"] += 1
                        error_text = str(block.get("content"))
                        if "denied" in error_text or "rejected" in error_text or record.get("toolDenialKind"):
                            session["permission_denials"].append(error_text[:160])
                    elif block.get("type") == "image":
                        session["pasted_images"] += 1
            text = user_text(content)
            if "[Request interrupted by user" in text:
                session["interruptions"] += 1
                continue
            slash_command = re.search(r"<command-name>(/[^<]+)</command-name>", text)
            if slash_command:
                session["slash_commands"][slash_command.group(1)] += 1
                continue
            is_human = (record.get("origin") or {}).get("kind") == "human" or record.get("promptSource") == "typed"
            if is_human and text and not record.get("isMeta") and not record.get("isCompactSummary"):
                if CORRECTION_PATTERN.match(text):
                    session["corrections"] += 1
                session["prompts"].append(re.sub(r"\s+", " ", text)[:MAX_PROMPT_CHARS])

    session["project"] = project_root(session["project"], os.path.basename(os.path.dirname(path)))
    session["permission_denials"] = session["permission_denials"][:10]
    # Only files edited 3+ times are interesting: they hint at rework.
    frequently_edited = {f: n for f, n in session["edited_files"].items() if n >= 3}
    session["edited_files"] = dict(collections.Counter(frequently_edited).most_common(10))
    for key in ("models", "slash_commands", "skills", "tools", "mcp"):
        session[key] = dict(session[key])
    session["bash"] = dict(session["bash"].most_common(15))
    session["turn_duration_min"] = round(session.pop("turn_duration_ms") / 60000, 1)
    return session


def main():
    sessions = []
    for path in glob.glob(os.path.join(PROJECTS_DIR, "*", "*.jsonl")):
        if os.path.getmtime(path) < CUTOFF_EPOCH:
            continue
        session = summarize_session(path)
        if not session["prompts"] and not session["tools"]:
            continue
        session_id = os.path.splitext(os.path.basename(path))[0]
        session["session_id"] = session_id
        session["subagents"] = len(glob.glob(os.path.join(os.path.dirname(path), session_id, "subagents", "*.jsonl")))
        sessions.append(session)
    sessions.sort(key=lambda s: s["start"] or "")

    totals = collections.Counter()
    bash_totals = collections.Counter()
    for session in sessions:
        totals.update({k: session[k] for k in ("tool_errors", "interruptions", "compactions", "corrections", "subagents")})
        totals["prompts"] += len(session["prompts"])
        totals["permission_denials"] += len(session["permission_denials"])
        bash_totals.update(session["bash"])

    json.dump({
        "generated_at": datetime.now().isoformat(timespec="minutes"), "days": DAYS, "session_count": len(sessions),
        "totals": dict(totals), "top_bash_programs": dict(bash_totals.most_common(25)), "sessions": sessions,
    }, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
