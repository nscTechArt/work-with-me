---
name: reclaim-code-entropy
description: Dedicated audit or end-to-end removal of obsolete maintenance surfaces and mirrored truths across a subsystem or repository.
disable-model-invocation: true
---

# Reclaim Code Entropy

Run a dedicated pass over a named subsystem or repository to remove **entropy**: obsolete maintenance surfaces and mirrored truths with no current load-bearing reason, measured by fewer truths and contracts the codebase must keep coherent. Keep scope strictly on those two targets; leave local behavior-preserving polish, redesigning active module boundaries, and closing in-flight task drafts out of this pass.

Follow `docs/evidence-model.md` if present (otherwise grade load-bearing claims `Confirmed` / `Inferred` / `Unresolved` against the current checkout and falsify every candidate before reporting).

## 1. Lock scope, mode, and boundaries

- **Mode**: default to read-only **audit** unless the user explicitly asks to apply or remove.
- **Scope**: pin the named subsystem or whole repository as the cleanup target; reachability searches and internal caller updates still span the whole repository. Check `git status` to preserve unrelated uncommitted edits, and exclude generated outputs, vendored code, and historical migrations from direct edits.
- **Contracts**: read project guidance (`AGENTS.md`, `docs/product-scope.md`, `docs/architecture/`, `GLOSSARY.md` where present) and package, API, or config manifests to establish confirmed product decisions, declared compatibility boundaries (public APIs, wire protocols, persisted formats), and local execution rules.

## 2. Prove candidates

Survey for two classes of entropy:

- **Obsolete surface**: dead paths, expired switches or config keys, unused fallbacks, unused dependencies, expired temporary workarounds, abandoned stubs, superseded compatibility branches, or residue consumed only by tests, docs, or snapshots.
- **Mirrored truth**: duplicate states, caches, contracts, lifecycle flags, forwarding-only wrappers, or duplicate internal mechanisms that require synchronization.

Distinguish duplication from intentional independence, trust-boundary guards, and resource cleanup on surviving paths. Treat static-analyzer warnings and historical notes as leads, not proof.

For each candidate:

1. **Trace real reachability** across the whole repository: code, active configs, file paths, event or wire strings, dependency manifests, and dynamic entrypoints (reflection, registries, DI, serialization, lazy imports).
2. **Apply the boundary rule**:
   - **External or product boundary**: never cut a reachable user capability, confirmed product decision, or declared compatibility boundary without explicit user approval. In audit mode, flag it as a product decision and continue; in apply mode, leave it untouched, pausing to ask now only if remaining cuts depend on it, and otherwise finish independent internal cuts and surface it in the report.
   - **Internal surface**: existing internal callers or recorded past rationales do not automatically protect a surface. Verify recorded reasons against current code, derivation, or measurement; when the premise has expired, is provisional or unrecorded, or cutting wins clearly on the finished end state (correctness, runtime cost, simplicity), plan an end-to-end internal cut.
3. **Falsify and confirm net reduction**: seek counter-evidence that the surface is still load-bearing or intentionally independent, and drop candidates that relocate complexity without reducing truths or contracts. Finding nothing safe to cut is a valid result.

**Cut gate**: edit only candidates whose reachability, expired or superseded rationale, and net reduction are `Confirmed`, with a named smallest decisive check to verify the cut. Leave anything not `Confirmed` untouched; report high-value `Unresolved` items with what is unknown, what was inspected, impact, and cheapest check.

## 3. Apply and verify (apply mode)

Run a proportional baseline check first when local execution is permitted, so pre-existing failures stay distinct from regressions.

Apply confirmed cuts one ownership boundary at a time:

- **Remove end to end**: delete obsolete code, config, dependencies, behavior-specific tests, and stale docs together; update internal callers directly with no compatibility shims, and keep tests guarding surviving observable contracts.
- **Collapse onto one truth**: converge mirrored state or contracts onto the single load-bearing representation rather than adding a synchronization wrapper.
- **Per-batch check (when local execution is permitted)**: run the batch's smallest decisive check before moving on; on failure, distinguish a load-bearing surface, an incomplete cut, or a red baseline, and complete the cut or revert only that batch rather than weakening a check.

After all batches:

- **Residual sweep**: re-search deleted symbols, strings, paths, dependencies, and doc references across the repository.
- **Broad verification**: when local execution is permitted, run relevant broad gates and any analyzer that flagged a cut; when execution is unavailable or forbidden, finish statically and deliver the smallest decisive user checklist.
- **Independent review**: for cross-boundary or wide-scope cuts, run a clean-context review via a read-only sub-agent with a **fresh context window** (never a fork inheriting parent context) to verify the diff against surviving contracts, dynamic reachability, and missed residue.

## 4. Report

- **Audit mode**: rank confirmed candidates by net maintenance reduction and risk, with their evidence, exact cut, and decisive check; list product-decision candidates and high-value `Unresolved` items separately.
- **Apply mode**: report removed contracts or mirrored truths, any user-approved behavior or compatibility impact (confirm none when only internal surfaces changed), verification results or static checklist, and high-value candidates left untouched for user decision or missing evidence.
