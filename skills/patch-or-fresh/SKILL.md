---
name: patch-or-fresh
description: Re-examine an upcoming change from zero against current requirements and sibling conventions before editing, then settle the shape and scope.
disable-model-invocation: true
---

# Patch or Fresh

Stay read-only until the user confirms. Cite inspected files for every claim, boundary, and scope item; mark anything unread as `uninspected`.

## 1. Frame the requirement and locked boundaries

Define the upcoming change in one plain sentence describing the behavior and invariants the system needs now, independent of the current code layout or prior plan. If product direction or the requirement is unsettled or too vague to design from zero, ask one focused question and wait.

Read the enclosing `AGENTS.md` (or `CLAUDE.md`), `docs/product-scope.md`, and directly relevant architecture docs (when present), and note any declared compatibility boundaries (public APIs, wire formats, persisted schemas). Separate **locked boundaries** (confirmed product rules and compatibility contracts) from mutable internals.

## 2. Design from zero and audit against reality

When this session has already proposed a plan, fix, or implementation anchored to existing code, dispatch this step to a read-only sub-agent with a **fresh context window** (never a fork inheriting parent context), passing only this step, the requirement, locked boundaries, and target area (no prior plan or reasoning). Verify every returned file claim against the checkout before Step 3.

Read the target files in full, plus their direct callers, owning tests, relevant architecture docs, and representative sibling modules of the same kind (when present; if fan-out is large, sample and mark unread areas `uninspected`).

1. **Sketch the fresh shape**: the cleanest data model, interface, validation, naming, and control flow you would author from zero for the current requirement within locked boundaries, aligned with sibling conventions.
2. **Audit every mismatch**: compare the fresh shape against current code and reverse-check every awkward or seemingly redundant existing detail against actual callers, secondary paths, and recorded rationale. Classify each mismatch as **expired drift** (legacy assumptions, duplicate logic, split control flow, naming or type drift free to reshape) or a **load-bearing constraint** (hidden invariants, secondary contracts, or edge cases that must survive). If inspected code and docs still cannot settle whether an existing detail holds, flag it as an unverified assumption for Step 4 instead of guessing.

Done when every in-scope item above is inspected (or marked `uninspected`), and every mismatch is classified or flagged with file citations.

## 3. Settle the landing mode

Choose the landing mode from inspected code facts (plus any user-stated experimental or roadmap constraint), reserving a user fork for genuine cost-vs-quality trade-offs:

- **Fits as-is**: current code matches the fresh shape with no material drift; proceed with the minimal file scope.
- **Direct reshape**: reshaping to the fresh shape delivers clear net gain within roughly the same file set and negligible extra blast radius. Adopt the fresh shape directly instead of fabricating a strawman patch path.
- **Scoped reshape**: a clean middle cut dominates: reshaping the core data model or interface pays off now, while sweeping untouched siblings or distant callers expands the blast radius disproportionately or outruns an unvalidated experiment. Define an explicit cut line: what reshapes now, what stays untouched, and what deferred debt remains.
- **True fork**: no single path dominates: minimal landing adds concrete structural friction (flags, branching, coupling, split truths), while any clean reshape carries a genuinely wide blast radius (cross-module interfaces, many callers, sibling sweeps) or commits to an unvalidated direction. Price both paths concretely (exact touched files, structural friction of patching vs concrete end-state gain of reshaping, and blast-radius or reversibility risk) and pick an evidence-based lean.

## 4. Hand off for confirmation

Reply concisely in the user's language, verdict and landing mode first:

- **Requirement & locked boundaries**: the one-sentence goal and hard constraints.
- **Shape & surviving constraints**: for **Fits as-is**, state plainly that current code fits. Otherwise summarize the fresh shape, the concrete expired drift it clears, and any load-bearing constraints that must survive (plus the cut line and deferred debt for **Scoped reshape**).
- **Scope (or both paths when forked)**: full file-level scope to confirm (target files, callers, tests, docs, and any siblings). Only under **True fork**, present both priced paths and your evidence-based lean.
- **Assumptions to confirm** (omit if none): any unverified legacy behavior from Step 2, or external, roadmap, or schedule assumption that could overturn the shape, cut line, scope, or fork lean.

Stop and wait for confirmation (or a path choice under **True fork**).
