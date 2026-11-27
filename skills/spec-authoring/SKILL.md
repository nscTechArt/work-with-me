---
name: spec-authoring
description: Disposable specs (spec.md) and multi-session tickets (issues/) under .scratch/<slug>/. Use when writing a multi-seam or high-risk spec, splitting it into local tickets, or updating in-flight contracts.
---

# Spec Authoring

`.scratch/<slug>/` holds disposable working drafts; cite only living docs or code from repository files and comments.

## Spec (`.scratch/<slug>/spec.md`)

Write a spec only when work spans multiple seams or carries high design or rework risk; skip it for local single-session work. Keep `spec.md` **short by omission, not compression**:

- **Scope:** define the goal, out-of-scope exclusions, concrete **cross-seam contracts** (inputs, outputs, formats, ownership, ordering, invariants), departed module-doc decisions with verified reasons, and acceptance evidence (per `docs/testing.md` if present, otherwise choose the cheapest reliable lock and require a blind spot, independent oracle, and stable interface for permanent tests).
- **Omit single-unit internals:** leave local algorithm steps, helper math, and tuning constants to code unless they cross a seam or depart from a cited source.
- **Single owner:** define each contract or rule in one owning section and link to it elsewhere.
- **Grounding:** verify every load-bearing claim against current code at `HEAD` (per `docs/evidence-model.md` if present, otherwise cite inspected `file:line` or mark unknowns explicitly). When `.scratch/<slug>/research.md` exists, resolve its unresolved claims, finalize departures from adopted references, and cite `research.md` or exact source locations directly.

Specify three failure-prone boundaries whenever they apply:

- **Traced cross-seam values:** trace every introduced or changed value crossing a seam (e.g., config/serializer to runtime, CPU to GPU) through conversions to consumer use at `HEAD` (units, ranges, encodings, scale, packing, defaults).
- **Edge states:** define inputs and outputs for first use, reset, resize, retry, empty/missing/invalid/non-finite inputs, and out-of-range outputs.
- **Persistent state invalidation:** for each keyed/indexed store, cache, history, or pending commit, define behavior on overwrite, skip, failed or abandoned attempt, and implicit input changes (not reflected in its key) enumerated from the producer at `HEAD`.

Update `spec.md` during implementation only when a contract changes while open downstream tickets still depend on it.

## Tickets (`.scratch/<slug>/issues/<NN>-<ticket-slug>.md`)

Split into numbered, independently deliverable vertical slices from `01` covering every spec contract only when implementation spans multiple sessions. Propose the slice breakdown briefly before writing ticket files if the split has meaningful ordering trade-offs.

Each ticket tracks:

- `Status: open | done` (mark `done` once implementation and the repository's required verification pass: local checks when allowed, or static review with any pending manual runtime check noted).
- `Blocked by:` acyclic producer-to-consumer ticket dependencies, or `None`.
- Concrete code entry points at `HEAD`, links to owning sections in `spec.md` for all contracts, tables, and thresholds, and links to `research.md` only for background or external reference context.
- Smallest acceptance evidence per `docs/testing.md` (or cheapest decisive verification).
- Delivered symbols, interfaces, and files, appended on completion so downstream tickets stay grounded.

## Close-Out

At close-out, call the Skill tool with `"repo-docs"` to sync durable decisions, contracts, traps, and terms into living docs in the same change and handle maintainer-confirmed `.scratch/` deletion.
