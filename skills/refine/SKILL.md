---
name: refine
description: Simplify selected scope while preserving intended behavior, reusing repository patterns, and fixing verified in-scope bugs directly.
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

When the target spans multiple files or was authored or edited in this session, dispatch Step 2 to a read-only sub-agent with a **fresh context window** (never a fork inheriting parent context), passing only Step 2's instructions, the scope, the factual baseline (never implementation reasoning or conclusions), and the target files or diff. Verify its returned candidates against the current files before editing. If no sub-agent is available, run Step 2 here and note that the review ran without fresh-context isolation.

## 2. Find simplifications

Examine the target with two passes:

- **Inward**: cut redundant state, indirection, branching, dead paths, obsolete comments, and obvious repeated work or allocations. Keep meaningful domain wrappers intact.
- **Outward**: search beyond changed lines by concept and operation, not just symbol name, for existing helpers, sibling implementations, and repository conventions. Reuse only when preconditions, early exits, errors, and lifecycle semantics match; keep distinct domain concepts separate.

Also note any incidental correctness bug verified while reading, with location and evidence. Return each candidate with location, proposed change, and any behavior uncertainty or decision risk.

**Done when**: every file or symbol in scope has been examined in context, and every new helper or repeated logic block has been checked against the repository with at least one concept-level search.

## 3. Apply safe edits

For review-only requests, skip editing and report the validated findings. Otherwise, keep every edit strictly in scope (preserving unrelated local edits and never spilling into adjacent files or nearby debt) and decision-safe (no unresolved product, design, contract, compatibility, or public API choice):

- **Simplifications**: apply when both behavior-preserving and net simpler. Behavior preservation requires code-path reasoning plus available local checks or tests to support equivalence across inputs, error paths, ordering, and lifecycles; defer on real uncertainty (reflection, serialization, ABI constraints, hidden external callers, or unclear edge-case intent). Net simpler means the smallest change removes more complexity than it adds, rather than relocating it or adding indirection for a few duplicate lines.
- **Verified correctness bugs**: fix directly when both the bug and its intended fix are verified without ambiguity; defer uncertain bugs.

## 4. Verify and report

When edits were made, run the smallest meaningful checks permitted by repository instructions, and re-inspect the final diff against the selected scope and unrelated local changes.

- **Applied changes** (when edits were made): what was simplified, why, any in-scope correctness bug fixes listed separately with their behavior change, and what checks ran with their outcomes.
- **Remaining findings**: simplifications or correctness bugs deferred for scope, uncertainty, or decision reasons (with location and evidence). If all candidates were ruled out, note any key reason to keep the existing implementation.
