# Evidence Model

## Evidence Strength

Grade every **load-bearing** claim (one whose truth can change a decision, correctness judgment, or scope):

- **Confirmed:** verified directly in the current checkout, active configuration, or another primary source below, with exact location cited. Re-read if the maintainer may have edited files during the session.
  - For a consumer or reused helper, verify the actual call site (activation gate, called overload or branch, and preconditions of reused values), not just the definition.
  - For a configurable setting, cite the active value in effect (and the code default if different).
  - For an absence, uniqueness, universal, or equivalence claim (`"no X"`, `"only X"`, `"every X"`, `"matches Y"`), state the checked scope and forms of `X`, and assert it only within that scope.
- **Inferred:** supported by observations without direct proof.
- **Unresolved:** missing evidence, conflicting evidence, or execution-dependent.

Source boundaries:

- **Leads to verify:** historical specs, closed tickets, code comments, second-hand summaries, and existing tests require verification against primary sources and the current checkout. Test code shows intended coverage, not a passing run; `.scratch/` files are evidence only within the work they were drafted for.
- **External sources:** cite pinned revision or canonical URL with date, plus version and environment context for behavior or performance claims.
- **Runtime observations:** local check outputs (when allowed) or maintainer observations (stating what and where) confirm execution-dependent claims.

## Unresolved Claims

When the repository allows local execution, settle runtime or build questions with the smallest local check rather than leaving them unresolved. When execution is unavailable or reserved for the maintainer, settle every statically decidable claim by inspection and leave only execution-dependent checks for the maintainer.

For each `Unresolved` load-bearing claim, state four items: what is unknown, what was inspected, how it affects the decision or conclusion, and the cheapest check to settle it.

When a statically decidable material claim cannot be inspected (such as an inaccessible external source), report it as an **Uninspected gap** separately from maintainer **runtime checks**: neither a confirmed defect nor a static pass.

## Falsify

Before reporting a defect or proposed gap, seek the strongest counter-evidence in the current checkout. Drop it if disproved; restate it at the narrower scope or lower severity if partially countered.

## Findings

Grade surviving review findings on two levels:

- **Blocking:** acting on the artifact produces a wrong result (correctness failure, contract/lifetime/order defect, regression, broken invariant, or Product Scope violation).
- **Non-blocking:** the result stays correct, with a concrete performance, maintainability, extensibility, or misreading risk.

## Clean-Context Review

When running an independent review of an artifact this session authored or discussed, dispatch a read-only subagent with a **fresh context window** (never a fork inheriting parent context) passing only the artifact, required inputs, and review criteria, never prior chat reasoning or conclusions. Keep returned findings intact and state any disagreement separately with its reason.

If the environment cannot dispatch a subagent, run the review inline and state explicitly that it is an author self-review.
