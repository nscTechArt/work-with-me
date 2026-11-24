"""PreToolUse guard template for zero-exception command and path write bans.

Invoked by .agents/hooks.json. Antigravity runs hook commands with the
directory containing hooks.json (.agents/) as the working directory, so
`python -B ./scripts/pre_tool_guard.py` resolves relative to .agents/.

Supports both PreToolUse stdin JSON payload formats:
- Antigravity: {"toolCall": {"name": "...", "args": {...}}, "cwd": "..."}
  (denies with {"decision": "deny", "reason": "..."}).
- Claude Code: {"tool_name": "...", "tool_input": {...}, "cwd": "..."}
  (denies with hookSpecificOutput permissionDecision="deny").
"""

from __future__ import annotations

import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Project-specific banned command patterns: tuple of (compiled_regex, denial_reason).
# Example:
#   (re.compile(r"\bdotnet(?:\.exe)?\s+(?:build|test)\b", re.IGNORECASE), "Builds are owned by the maintainer.")
BANNED_COMMAND_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = ()

# Project-specific top-level generated directories that agents must not edit directly.
# Example: ("dist", "build", "node_modules")
BANNED_EDIT_TOP_DIRS: tuple[str, ...] = ()

_BANNED_EDIT_MAP: dict[str, str] = {
    d.strip("/\\").lower(): d.strip("/\\")
    for d in BANNED_EDIT_TOP_DIRS
    if d.strip("/\\")
}

BANNED_RULE_FILENAMES = frozenset({
    "claude.md",
    "gemini.md",
})

COMMAND_TOOLS = frozenset({
    "run_command",
    "bash",
})

WRITE_TOOLS = frozenset({
    "edit_file",
    "write_file",
    "write_to_file",
    "replace_file_content",
    "multi_replace_file_content",
    "edit",
    "write",
    "multiedit",
    "notebookedit",
})


def deny(reason: str, harness: str) -> int:
    if harness == "claude":
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }))
    else:
        print(json.dumps({"decision": "deny", "reason": reason}))
    return 0


def check_command(args: dict) -> str | None:
    cmd = args.get("CommandLine") or args.get("command")
    if not isinstance(cmd, str) or not cmd:
        return None
    for pattern, reason in BANNED_COMMAND_PATTERNS:
        if pattern.search(cmd):
            return reason
    return None


def resolve_git_common_dir(checkout_dir: str) -> str | None:
    dot_git = os.path.join(checkout_dir, ".git")
    if os.path.isdir(dot_git):
        gitdir = dot_git
    elif os.path.isfile(dot_git):
        try:
            with open(dot_git, "r", encoding="utf-8-sig", errors="replace") as f:
                first_line = f.readline().strip()
        except OSError:
            return None
        if not first_line.lower().startswith("gitdir:"):
            return None
        raw_gitdir = first_line.split(":", 1)[1].strip()
        if not raw_gitdir:
            return None
        gitdir = os.path.join(checkout_dir, raw_gitdir)
        if not os.path.isdir(gitdir):
            return None
    else:
        return None

    commondir_file = os.path.join(gitdir, "commondir")
    if os.path.isfile(commondir_file):
        try:
            with open(commondir_file, "r", encoding="utf-8-sig", errors="replace") as f:
                raw_common = f.readline().strip()
        except OSError:
            return None
        if raw_common:
            return os.path.normcase(os.path.realpath(os.path.join(gitdir, raw_common)))
    return os.path.normcase(os.path.realpath(gitdir))


def resolve_repo_relpath(raw_path: str, payload: dict) -> str | None:
    cwd = payload.get("cwd") or REPO_ROOT
    target_real = os.path.realpath(os.path.join(cwd, raw_path))
    repo_common = resolve_git_common_dir(REPO_ROOT)

    if repo_common is not None:
        cur = os.path.dirname(target_real)
        while cur:
            candidate_common = resolve_git_common_dir(cur)
            if candidate_common is not None:
                if candidate_common == repo_common:
                    return os.path.relpath(target_real, cur).replace("\\", "/")
                return None
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
        return None

    root_real = os.path.realpath(REPO_ROOT)
    try:
        rel_norm = os.path.relpath(os.path.normcase(target_real), os.path.normcase(root_real))
    except ValueError:
        return None
    if rel_norm == ".." or rel_norm.startswith(".." + os.sep):
        return None
    return os.path.relpath(target_real, root_real).replace("\\", "/")


def check_write(args: dict, payload: dict) -> str | None:
    raw_path = (
        args.get("Path")
        or args.get("TargetFile")
        or args.get("file_path")
        or args.get("notebook_path")
    )
    if not isinstance(raw_path, str) or not raw_path:
        return None

    rel = resolve_repo_relpath(raw_path, payload)
    if rel is None:
        return None

    rel_lower = rel.lower()
    parts = rel_lower.split("/")
    top_dir = parts[0]
    basename = parts[-1]

    canonical = _BANNED_EDIT_MAP.get(top_dir)
    if canonical is not None:
        return f"Editing generated directory {canonical}/ is denied."

    if top_dir == ".claude":
        return "Do not create .claude/ configs; keep repository rules in root AGENTS.md and .agents/."

    if basename in BANNED_RULE_FILENAMES:
        return f"Do not create tool-specific rule file {basename}; keep standing rules in root AGENTS.md."

    if basename == "agents.md" and rel_lower != "agents.md":
        return "Do not create subdirectory AGENTS.md files; keep standing rules in root AGENTS.md."

    return None


def extract_tool_call(payload: dict) -> tuple[str, dict, str]:
    tool_call = payload.get("toolCall")
    if isinstance(tool_call, dict):
        name = tool_call.get("name")
        args = tool_call.get("args")
        return (
            name.lower() if isinstance(name, str) else "",
            args if isinstance(args, dict) else {},
            "antigravity",
        )
    tool_name = payload.get("tool_name")
    if isinstance(tool_name, str):
        args = payload.get("tool_input")
        return (
            tool_name.lower(),
            args if isinstance(args, dict) else {},
            "claude",
        )
    return "", {}, "antigravity"


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return 0
    if not isinstance(payload, dict):
        return 0

    tool_name, args, harness = extract_tool_call(payload)
    if not tool_name or not args:
        return 0

    reason: str | None = None
    if tool_name in COMMAND_TOOLS:
        reason = check_command(args)
    elif tool_name in WRITE_TOOLS:
        reason = check_write(args, payload)
    if reason is not None:
        return deny(reason, harness)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
