---
name: code-review
description: Review uncommitted changes, commits, or branches for correctness, standards, and spec compliance.
---

# Code Review

Read-only review of a diff against a fixed point. Never edit repository files.

Follow `docs/evidence-model.md` when present. Otherwise grade load-bearing claims against the reviewed target (`Confirmed` / `Inferred` / `Unresolved`), report statically decidable claims whose source cannot be inspected as `Uninspected gap`, and grade surviving findings as `Blocking` (produces a wrong result, contract/order/lifetime defect, regression, or product-scope violation) or `Non-blocking` (concrete performance, maintainability, extensibility, or misreading risk).

## 1. Prepare inputs

Resolve the fixed point from the caller (`HEAD`, commit SHA, branch, or tag). If omitted and the working tree has changes, default to `HEAD`; otherwise ask. Confirm the fixed point resolves and the diff is non-empty.

- **Uncommitted changes (`HEAD`)**: diff with `git diff HEAD` plus every untracked file from `git ls-files -o --exclude-standard` read in full. The **reviewed target** is `HEAD`, the working tree, and those untracked files.
- **Committed range**: diff with `git diff <fixed-point>...HEAD` and commit log `git log <fixed-point>..HEAD --oneline`. The **reviewed target** is `HEAD`; for any file with unrelated local edits, read `git show HEAD:<path>`.
- **Spec / ticket**: use the caller's path, or any `.scratch/<feature>/` spec or ticket touched by the diff. When reviewing a ticket, include every spec section it cites and judge completeness strictly within that ticket's scope. If no spec exists, skip the Spec axis and note "no spec provided".
- **Standards & contracts**: collect root `AGENTS.md` / `CLAUDE.md`, `docs/product-scope.md`, `docs/evidence-model.md`, touched module files under `docs/architecture/`, `GLOSSARY.md`, and coding-style docs (when present).

## 2. Enter a clean context

- If the current context authored or discussed this diff, dispatch Steps 3 and 4 to a read-only sub-agent with a **fresh context window** (never a fork inheriting parent context), handing it this skill, the diff command, the reviewed target rule, and the collected input paths.
- Otherwise run Steps 3 and 4 here. If no sub-agent is available for a self-authored diff, run here and state explicitly in the report that the author reviewed its own work.

## 3. Review

Run two separate passes:

1. **Correctness & Standards**: check every changed hunk and affected call site for logic bugs, edge and error states, resource lifetime or ordering defects, caller regressions, living architecture contract violations, and breaches of documented repository standards. Skip linter-enforced formatting and behavior-preserving refactoring. Consult the spec or ticket (when present) to recognize intentional departures.
2. **Spec** (when present): walk every requirement, contract, edge-state, and persistent-state rule in scope. Report what is missing or partial, unrequested, or divergent, quoting the relevant spec or ticket line.

Falsify every candidate finding against the **reviewed target** (drop if disproved; narrow scope or lower severity if partially countered).

## 4. Report

Present `## Correctness & Standards` and `## Spec` as separate sections without merging or reranking across axes. Within each section, order findings `Blocking`, `Non-blocking`, and any `Unresolved` claim or `Uninspected gap`, citing `file:line` and supporting evidence (or what is unknown, what was inspected, its impact, and the cheapest check).

End with a one-line summary giving the count per axis and whether any `Blocking` finding remains.
