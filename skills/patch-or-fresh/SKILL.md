---
name: patch-or-fresh
description: Check whether changes read as written fresh or layered patches, and reshape safe in-scope seams directly.
disable-model-invocation: true
---

# Patch or Fresh

Evaluate whether touched code, tests, comments, and docs read as **written fresh** for current requirements rather than patches layered onto legacy shape, and reshape safe in-scope patch seams directly.

## 1. Resolve target and isolate context

Resolve the review target from the caller (staged diff, uncommitted diff against `HEAD`, commit range, or explicit file paths). When omitted, review staged changes (`git diff --cached`) if non-empty; otherwise review uncommitted changes against `HEAD` (`git diff HEAD`) plus untracked files (`git ls-files -o --exclude-standard`). If the resolved target is empty, ask what to review and wait.

Note the enclosing `AGENTS.md` or `CLAUDE.md` path if present, plus the task goal and explicit user constraints (either an originating spec/ticket path or a brief factual summary, never implementation reasoning or conclusions).

If this session authored or discussed the target change, dispatch Step 2 to a read-only sub-agent with a **fresh context window** (never a fork inheriting parent context), passing only Step 2's instructions, the resolved target, the repo guidance path, and the task goal or spec path. Verify its returned candidates against the current files before editing. If no sub-agent is available, run Step 2 here and note that the review ran without fresh-context isolation.

## 2. Inspect whole files and filter

Read the enclosing `AGENTS.md` or `CLAUDE.md`, any originating spec or ticket, every touched file in full (not just diff hunks), and directly implicated architecture/design docs or owning test files. From those sources, establish the repo's standards, scope rules, and declared compatibility boundaries (public APIs, wire formats, persisted schemas). Then ask of each touched area: *if authored from zero for current requirements, would it take this shape?*

Check all four artifact types for patch seams:

- **Code:** bolt-on flags or special-case branches, thin wrappers routing around legacy interfaces, unnecessary internal backward compatibility, or leftover dead or duplicate code in scope.
- **Tests:** tacked-on cases or branches inside legacy fixtures instead of tests shaped around the current contract.
- **Comments and docs:** appended clauses, spliced sentences, or delta narration ("formerly", "now also", migration notes) instead of direct current-state prose.

Filter every candidate before keeping it:

- **Verify reasons and boundaries:** verify recorded reasons in inline comments and architecture/design docs against current code, and check declared compatibility boundaries. Drop anything protecting a constraint that still holds or an external compatibility boundary (unless the user explicitly asked to revisit it).
- **Require real end-state gain:** keep a finding only when the fresh alternative wins clearly on correctness, runtime quality or cost, or long-term simplicity (or the repo's explicit axes). Drop equivalent shapes and style preferences.
- **Classify scope honestly:** label each kept finding **In scope** (local to this change) or **Beyond task scope** (wider refactor outside this task). Exclude unrelated pre-existing issues outside the touched area.

Return each kept finding with `file:line`, the patch seam, the concrete fresh alternative and end-state gain, and its scope label (plus any trade-off or pause trigger); if none remain, state that the change reads as written fresh.

## 3. Apply safe reshapes and reply

For review-only requests or committed-history targets (such as a commit range), skip editing and report the kept findings. Otherwise, reshape verified **In scope** findings directly while preserving unrelated local edits. Hold any finding that is **Beyond task scope**, requires a user decision (such as a product or contract trade-off, a locked constraint, revisiting a declared compatibility boundary, or an unauthorized destructive action), or triggers a pause rule in `AGENTS.md` or `CLAUDE.md`. When edits are made, run the smallest meaningful checks permitted by repository instructions and re-inspect the final diff against scope and unrelated local changes.

Reply directly and plainly without a formal report template. If the change already reads as written fresh, say so plainly. Otherwise, when edits were made, list each applied reshape (`file:line`, patch seam removed, fresh shape and end-state gain) and the checks run with their outcomes; list any held or review-only findings (`file:line`, patch seam, concrete fresh alternative and gain, scope label, and for held findings, the decision needed or pause trigger).
