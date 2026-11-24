---
name: refine
description: Behavior-preserving simplification within a selected scope, removing local excess and reusing existing repository patterns.
disable-model-invocation: true
---

# Refine

## 1. Pin scope and baseline

Inspect `git status` and resolve the target in order:

1. **Explicit scope**: requested files, symbols, staged or unstaged changes, commit or range, or named area. Whole-repository refinement requires an explicit request.
2. **Conversation target**: concrete files, symbols, or changes already under discussion.
3. **Local changes**: combined unstaged, staged, and relevant untracked changes.
4. **HEAD**: the latest commit.

Identify the behavior and contracts the target must preserve (for a diff or commit, its intended **post-change** behavior and fixes).

## 2. Find simplifications

Examine the target with two passes:

- **Inward**: cut redundant state, indirection, branching, dead paths, obsolete comments, and obvious repeated work or allocations. Keep meaningful domain wrappers intact.
- **Outward**: search beyond changed lines by concept and operation, not just symbol name, for existing helpers, sibling implementations, and repository conventions. Reuse only when preconditions, early exits, errors, and lifecycle semantics match; keep distinct domain concepts separate.

When the target spans multiple files or underwent multi-turn edits in this session, dispatch a read-only sub-agent with a **fresh context window** (never a fork inheriting parent context) to run both passes. Pass it the scope, baseline, and target files or diff, then verify its returned candidates against the current files before editing.

**Done when**: every file or symbol in scope has been examined in context, and every new helper or repeated logic block has been checked against the repository with at least one concept-level search.

## 3. Apply safe simplifications

For review-only requests, skip editing and report the validated findings. Otherwise, apply a simplification when all four hold:

1. **Strictly in scope**: edits stay inside the selected scope, preserve unrelated local edits, and never spill into adjacent files or nearby debt; report cross-scope opportunities instead.
2. **Behavior-preserving**: code-path reasoning (plus available local checks or tests) supports equivalence across inputs, error paths, ordering, and lifecycles. Defer when real uncertainty remains (reflection, serialization, ABI constraints, hidden external callers, or unclear edge-case intent).
3. **Net simpler**: the smallest change eliminates more complexity than it adds, rather than relocating it or adding indirection for a few duplicate lines.
4. **Decision-safe**: it makes no unresolved product, design, or public API choice.

Report any incidental correctness bug separately instead of mixing a behavior change into simplification.

## 4. Verify and report

Run the smallest meaningful checks permitted by repository instructions, and re-inspect the final diff against the selected scope and unrelated local changes.

- **Applied changes** (when edits were made): what was simplified, why, and what checks ran with their outcomes.
- **Remaining findings**: simplifications deferred for scope, uncertainty, or decision reasons, plus any incidental correctness bugs found (with location and evidence). If all candidates were ruled out, note any key reason to keep the existing implementation.
