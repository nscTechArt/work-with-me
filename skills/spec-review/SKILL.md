---
name: spec-review
description: Single-pass pre-code Blocking check of concrete spec contracts and open multi-ticket seams under .scratch/<slug>/.
disable-model-invocation: true
---

# Spec Review

Single-pass pre-code check of `.scratch/<slug>/spec.md` and open (non-`done`) `issues/*.md`, repairing actionable Blocking findings in place.

## 1. Review Isolation

If this session authored or discussed the spec, dispatch Step 2 to a read-only subagent with a **fresh context window** (never a fork inheriting parent context), passing only Step 2's instructions inline (do not assume the subagent can read skill files outside the repository) and `AGENTS.md` (if present), `docs/evidence-model.md` (if present), `.scratch/<slug>/spec.md`, open `issues/*.md`, and any `done` ticket IDs (never prior chat reasoning or conclusions). Otherwise run Step 2 directly here (if no subagent is available for a self-authored spec, run inline and state explicitly that it is an author self-review).

## 2. Targeted Checks and Falsify

Follow `docs/evidence-model.md` if present (otherwise verify load-bearing claims against `HEAD` and falsify every candidate finding against counter-evidence before reporting). Report **Blocking** findings only (defects causing wrong behavior, broken contracts or persistent state, violated product scope, or multi-ticket rework). Skip architectural direction, local single-pass guards fixable during coding, test-plan tuning, and Non-blocking polish.

Use **targeted reads**: open only the producer/consumer files directly coupled to a contract under check, plus `docs/product-scope.md` or a touched `docs/architecture/<module>.md` when a contract touches its invariant.

Check both surfaces, then falsify every candidate Blocking finding against `HEAD`:

1. **Concrete seam contracts:** trace each cross-seam value (units, range, encoding, packing, formula, default), resource/data format, ownership, execution-order assumption, and persistent-state or edge-state rule against each other and actual producer/consumer call sites at `HEAD`.
2. **Multi-ticket seams (when open tickets exist):** verify every spec contract not already satisfied at `HEAD` is covered by an open ticket, shared interfaces/formats/ownership agree across tickets, and `Blocked by` dependencies (treating `done` tickets as satisfied) form an acyclic producer-to-consumer order.

Return each surviving Blocking finding with: spec/ticket `file:line`, direct evidence (opened `HEAD` or conflicting spec/ticket `file:line`), failure consequence, and smallest repair. Also return any load-bearing `Unresolved` claim or `Uninspected gap` (missing external evidence blocking a contract) with what is unknown, what was inspected, its impact, and the cheapest check.

## 3. Repair and Report

- **Repair in place:** fix actionable Blocking findings in the owning section of `spec.md` and affected open tickets. Hold items hitting `AGENTS.md` pause rules (product trade-offs, locked or compatibility departures, broken premises) or needing missing external evidence for the maintainer.
- **Report:** state the Blocking count, applied repairs, and any held items.
