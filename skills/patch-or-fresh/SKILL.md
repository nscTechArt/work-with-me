---
name: patch-or-fresh
description: Compare patching existing code against building fresh before editing, and settle the path and scope.
disable-model-invocation: true
---

# Patch or Fresh

Decide before editing whether an upcoming change belongs on the **patch path** (extending the existing shape in place) or the **fresh path** (reshaping to the design you would author from zero for current requirements), and lock the resulting scope. Stay strictly read-only until the user confirms. Cite inspected files for every mismatch, constraint, caller, sibling, and scope item, and mark anything not read as `uninspected`.

## 1. Frame the requirement and locked boundaries

State the upcoming change in one plain sentence describing the behavior and invariants the system needs now, independent of the current code layout. If the requirement is missing or too vague to design from zero, ask one focused question and wait.

Read the enclosing `AGENTS.md` (or `CLAUDE.md`), `docs/product-scope.md`, and directly relevant architecture docs (when present), plus any declared compatibility boundaries (public APIs, wire formats, persisted schemas). Separate **locked boundaries** (confirmed product rules and compatibility contracts) from internal legacy assumptions that are free to change.

## 2. Sketch the fresh shape against reality

When this session has already proposed a plan, fix, or implementation anchored to existing code, dispatch this step to a read-only sub-agent with a **fresh context window** (never a fork inheriting parent context), passing only this step's instructions, the one-sentence requirement, the locked boundaries, and the target area (omitting prior design or implementation reasoning). Verify returned file claims before Step 3.

Read the target files in full, their direct callers, owning tests, architecture docs, and sibling modules of the same kind. Test recorded rationale in inline comments and docs against current code to separate constraints that still hold from expired assumptions.

Sketch the **fresh shape**: the cleanest data model, interface, and control flow you would author from zero for the current requirement within locked boundaries. Compare it against current code to identify concrete structural mismatches (expired assumptions, forced special cases, split responsibilities, or mismatched tests and docs).

## 3. Price both paths

If the current code already fits the fresh shape with no material structural mismatch, proceed directly to Step 4 with the planned file scope.

Otherwise, base both paths on code facts, leaving future roadmap, experimental risk, and schedule for the user to weigh:

- **Patch path**: exact landing seam and touched files (including callers, tests, and docs), concrete structural friction added (extra flags, branching, coupling, or awkward abstractions), and whether keeping the existing shape preserves **sibling consistency** across untouched peers or keeps an unvalidated experiment cheap.
- **Fresh path**: concrete end-state gain (correctness, runtime quality or cost, or long-term simplicity) and full **blast radius** (every file, caller, interface, test, doc, and sibling module that must move together to keep conventions unified).

## 4. Hand off the decision

Reply concisely in the user's language.

When the current shape already fits, state that plainly alongside the one-sentence requirement, any locked boundaries, and the planned file scope.

When forked, present:

- **Requirement**: the one-sentence current-state requirement and any locked boundaries.
- **Fresh shape vs current shape**: brief summary of the proposed fresh shape (data model, interface, or control flow) and the concrete structural mismatches with current code.
- **Patch path**: landing seam, touched files, structural cost, and consistency or experiment upsides.
- **Fresh path**: concrete gain and full file-level blast radius (including siblings to align).
- **Lean**: your evidence-based lean (**Patch** or **Fresh**), the code fact it hinges on, and which user-side factor (future plans, experimental risk, or schedule) flips the choice.

Wait for the user to choose **Patch** or **Fresh** (when forked) and confirm the scope before modifying any file.
