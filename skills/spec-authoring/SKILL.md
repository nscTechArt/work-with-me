---
name: spec-authoring
description: Disposable specs (spec.md) and multi-session tickets (issues/) under .scratch/<slug>/. Use when writing a multi-seam or high-risk spec, splitting it into local tickets, or updating in-flight contracts.
---

# Spec Authoring

`.scratch/<slug>/` holds disposable working drafts; cite only living docs or code from repository files and comments.

## Spec (`.scratch/<slug>/spec.md`)

Write a spec only when work spans multiple seams or carries high design or rework risk; skip it for local single-session work.

Ground every load-bearing claim against current code at `HEAD` (following `docs/evidence-model.md` if present, otherwise citing inspected `file:line` or marking unknowns explicitly). Define the goal, concrete contracts (inputs, outputs, formats, ownership, ordering), acceptance evidence (per `docs/testing.md` if present, otherwise choosing the cheapest reliable lock and requiring blind spot, independent oracle, and stable interface for permanent tests), out-of-scope exclusions, and any departed module-doc decisions with verified reasons. When `.scratch/<slug>/research.md` exists, resolve its unresolved claims, finalize departures from adopted references, and cite `research.md` or exact source locations directly instead of copying rationale. Keep each rule in one owning section and link to it elsewhere instead of restating it.

Explicitly specify three failure-prone boundaries whenever they apply:

- **Traced cross-seam values:** trace every introduced or changed value crossing a seam (e.g., config/serializer to runtime, CPU to GPU) through conversions to consumer use at `HEAD` (units, ranges, encodings, scale, packing, defaults).
- **Edge states:** define inputs and outputs for first use, reset, resize, retry, empty/missing/invalid/non-finite inputs, and out-of-range outputs.
- **Persistent state invalidation:** for each keyed/indexed store, cache, history, or pending commit, define behavior on overwrite, skip, failed or abandoned attempt, and implicit input changes (not reflected in its key) enumerated from the producer at `HEAD`.

Update `spec.md` during implementation only when a contract changes while open downstream tickets still depend on it.

## Tickets (`.scratch/<slug>/issues/<NN>-<ticket-slug>.md`)

Split into numbered self-contained vertical slices from `01` covering every spec contract only when implementation spans multiple sessions. Propose the slice breakdown briefly before writing ticket files if the split itself has meaningful ordering trade-offs.

Each ticket tracks:

- `Status: open | done` (use `done` once implementation and the repository's required verification pass: local checks when allowed, or static review with any pending manual runtime check noted).
- `Blocked by:` acyclic producer-to-consumer ticket dependencies, or `None`.
- Concrete code entry points at `HEAD` and pointers to owning `spec.md` (and `research.md`, if present) sections (do not duplicate spec tables or thresholds).
- Smallest acceptance evidence per `docs/testing.md` (or cheapest decisive verification).
- On completion, append delivered symbols, interfaces, and files so downstream tickets stay grounded.

## Close-Out

At close-out, call the Skill tool with `"repo-docs"` to sync durable decisions, contracts, traps, and terms into living docs in the same change and handle maintainer-confirmed `.scratch/` deletion.
