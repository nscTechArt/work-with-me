---
name: spec-review
description: Single-pass pre-code check of concrete spec contracts, open multi-ticket seams, and spec boundary under .scratch/<slug>/.
disable-model-invocation: true
---

# Spec Review

Single-pass pre-code check of `.scratch/<slug>/spec.md` and open (non-`done`) `issues/*.md`, repairing actionable contract and single-owner defects in place.

## 1. Review Isolation

If this session authored or discussed the spec, dispatch Step 2 to a read-only subagent with a **fresh context window** (never a fork inheriting parent context), passing only Step 2's instructions inline (do not assume the subagent can read skill files outside the repository) plus `AGENTS.md` (if present), `docs/evidence-model.md` (if present), `.scratch/<slug>/spec.md`, open `issues/*.md`, and any `done` ticket IDs (never prior chat reasoning or conclusions). Otherwise run Step 2 directly here (if no subagent is available for a self-authored spec, run inline and state explicitly that it is an author self-review).

## 2. Targeted Checks and Falsify

Follow `docs/evidence-model.md` if present (otherwise verify load-bearing claims against `HEAD` and falsify candidate Blocking findings against counter-evidence before reporting). Report only the four checks below and load-bearing evidence gaps; skip architectural direction, local single-unit guards fixable during coding, test-plan tuning, and style polish.

Use **targeted reads**: open only the producer/consumer files directly coupled to a contract under check, plus `docs/product-scope.md`, a touched `docs/architecture/<module>.md` when a contract touches its invariant, or `.scratch/<slug>/research.md` when cited by `spec.md`.

**Blocking checks** (defects causing wrong behavior, broken contracts or persistent state, violated product scope, or multi-ticket rework; falsify every candidate against `HEAD` or conflicting spec/ticket lines):

1. **Concrete seam contracts:** trace each cross-seam value (units, range, encoding, packing, formula, default), resource/data format, ownership, execution-order assumption, and persistent-state or edge-state rule against each other and actual producer/consumer call sites at `HEAD`.
2. **Multi-ticket seams (when open tickets exist):** verify every spec contract not already satisfied at `HEAD` is covered by an open ticket, shared interfaces/formats/ownership agree across tickets, and `Blocked by` dependencies (treating `done` tickets as satisfied) form an acyclic producer-to-consumer order.

**Ownership and boundary checks** (structural checks on `spec.md` and open `issues/*.md`; do not require `HEAD` falsification):

3. **Single-owner links:** flag any matching contract, table, or threshold restated across sections of `spec.md` or copied into open `issues/*.md` instead of linking to one owning section. Treat conflicting restatements as Blocking under #1 or #2.
4. **Spec boundary (inlined internals):** flag any `spec.md` section or passage that spells out single-unit internals (local algorithm steps, helper math, and tuning constants) that neither cross a seam nor depart from a cited source.

Return:

- **Blocking findings:** spec/ticket `file:line`, direct evidence (opened `HEAD` or conflicting spec/ticket `file:line`), failure consequence, and smallest repair.
- **Evidence gaps:** any load-bearing `Unresolved` claim or `Uninspected gap` (missing external evidence blocking a contract) with what is unknown, what was inspected, its impact, and the cheapest check.
- **Duplicate copies:** each matching copy's `file:line` and its owning section in `spec.md`.
- **Candidate internals to omit:** each passage's `file:line` and why it stays within one unit, for maintainer decision.

## 3. Repair and Report

- **Repair in place:** fix actionable Blocking findings in the owning section of `spec.md` and affected open tickets, and replace matching duplicate copies with links to their owning section.
- **Hold for maintainer:** items hitting `AGENTS.md` pause rules (product trade-offs, locked or compatibility departures, broken premises), evidence gaps (`Unresolved` claims or `Uninspected gaps`), and candidate single-unit internals to omit.
- **Report:** state the Blocking count, applied repairs (including deduplicated links), and any held items.
