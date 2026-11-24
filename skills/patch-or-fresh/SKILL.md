---
name: patch-or-fresh
description: Check whether changes read as written fresh or layered patches, and propose cleaner end states.
disable-model-invocation: true
---

# Patch or Fresh

Evaluate whether touched code, tests, comments, and docs read as **written fresh** for current requirements rather than patches layered onto legacy shape. Stay read-only until the user agrees to edit.

## 1. Resolve target and isolate context

Resolve the review target from the caller (staged diff, uncommitted diff against `HEAD`, commit range, or explicit file paths). When omitted, review staged changes (`git diff --cached`) if non-empty; otherwise review uncommitted changes against `HEAD` (`git diff HEAD`) plus untracked files (`git ls-files -o --exclude-standard`). If the resolved target is empty, ask what to review and wait.

Note the enclosing `AGENTS.md` or `CLAUDE.md` path if present, plus the task goal and explicit user constraints (either an originating spec/ticket path or a brief factual summary, never implementation reasoning or conclusions).

If this session authored or discussed the target change, dispatch Steps 2 and 3 to a read-only sub-agent with a **fresh context window** (never a fork inheriting parent context), passing only this skill, the resolved target, the repo guidance path, and the task goal or spec path. If no sub-agent is available, run Steps 2 and 3 here and note that the review ran without fresh-context isolation.

## 2. Inspect whole files and filter

Read the enclosing `AGENTS.md` or `CLAUDE.md`, any originating spec or ticket, every touched file in full (not just diff hunks), and directly implicated architecture/design docs or owning test files. From those sources, establish the repo's standards, scope rules, and declared compatibility boundaries (public APIs, wire formats, persisted schemas). Then ask of each touched area: *if authored from zero for current requirements, would it take this shape?*

Check all four artifact types for patch seams:

- **Code:** bolt-on flags or special-case branches, thin wrappers routing around legacy interfaces, unnecessary internal backward compatibility, or leftover dead or duplicate code in scope.
- **Tests:** tacked-on cases or branches inside legacy fixtures instead of tests shaped around the current contract.
- **Comments and docs:** appended clauses, spliced sentences, or delta narration ("formerly", "now also", migration notes) instead of direct current-state prose.

Filter every candidate before keeping it:

- **Verify reasons and boundaries:** verify recorded reasons in inline comments and architecture/design docs against current code, and check declared compatibility boundaries. Drop anything protecting a constraint that still holds or an external compatibility boundary (unless the user explicitly asked to revisit it).
- **Require real end-state gain:** keep a finding only when the fresh alternative wins clearly on correctness, runtime quality or cost, or long-term simplicity (or the repo's explicit axes). Drop equivalent shapes and style preferences.
- **Classify scope honestly:** label each kept finding **In scope** (reshape directly within this change) or **Beyond task scope** (wider refactor needing a user scope decision rather than a local patch). Exclude unrelated pre-existing issues outside the touched area.

## 3. Reply

Reply directly and plainly without a formal report template. If the change already reads as written fresh, say so plainly.

Otherwise, list each kept finding with its location (`file:line`), the patch seam observed, the concrete fresh alternative and its end-state gain, and its scope label (**In scope** or **Beyond task scope**).
