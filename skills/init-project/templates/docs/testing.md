# Testing

Automated tests are a regression guard for real risks, not a line-coverage target. Every retained test carries ongoing refactor maintenance cost, so enforce each contract with the cheapest reliable lock first:

- **Static checks and types:** type-system constraints, boundary validation, linters, schemas, hooks, and static inspection.
- **Targeted manual / runtime inspection:** gross visual or interactive failures when automated checks are disproportionate.
- **Automated tests:** execution-only blind spots that meet all three criteria below.

## Admission Criteria

Every proposed or retained permanent test must satisfy all three criteria (in specs and reviews, pick the cheapest sufficient evidence from the hierarchy above, and name the risk and oracle for any proposed test):

1. **Blind spot:** catches a concrete risk that static review, types, and routine checks miss (cross-boundary serialization or packing drift, edge-state transitions, persistence migration, concurrency, or non-trivial numerical/algorithmic invariants).
2. **Independent oracle:** derives expected outcomes from a source independent of the code under test (hand derivation, pinned external reference vector, specification, mathematical invariant, or a real producer-consumer round trip) instead of duplicating production logic.
3. **Stable interface:** calls a production caller's public interface and asserts observable behavior (reading persisted state through the public read interface rather than internal storage). Leave private helpers, internal call order, and exact diagnostic wording decoupled so internal refactors pass cleanly.

**Excluded:** trivial getters, simple clamps, default-value matrices, pass-through wrappers, and exact log wording.

- **One owner per risk:** assign each risk to one owning test at the highest practical interface; deleting duplicate or low-signal tests is a net gain.
- **Variant mapping:** when adding a variant or mode to a module with retained tests, map every retained test's risk to the new variant (new case, covered by shared code, or N/A with reason).

## Boundary Mocking

Keep internal modules and collaborators real. Prefer faithful local instances (temporary directory, embedded or test database) over mocks, and introduce test doubles only at genuine external boundaries: third-party APIs or hardware you do not control, remote transport seams, and nondeterministic inputs (clocks, random generators). Inject external boundaries as narrow, operation-specific interfaces rather than generic dispatchers.

## Verification Modes

- **Local execution allowed (implementing or fixing):** write a failing test first, verify it fails for the intended reason (**red**), then implement enough to pass (**green**). Work in small vertical slices when exploring uncertain edge cases, keeping structural refactoring separate from behavior changes.
- **Locking existing behavior, writing specs, or auditing a suite:** skip red-green and apply the Admission Criteria directly.
- **Local execution unavailable or reserved for the maintainer:** evaluate tests statically against the Admission Criteria and deliver a minimal runtime verification checklist for any tests added, changed, or removed.

## Portfolio Review and Hygiene

Tests written during exploration or bug isolation are **provisional** scaffolding. Before finishing a feature or bug fix, audit touched tests:

- **Keep** tests that satisfy all three Admission Criteria and own a distinct risk.
- **Merge or lift** tests whose risk belongs at a higher practical interface.
- **Delete** duplicate, superseded, or implementation-coupled tests once their risk is covered by a named owning test or cheaper lock.

State the protected risk when the test name does not, record hand derivations or reference pins beside assertions, and note the error source bounded by any numeric tolerance (never loosen tolerances just to pass). Clean up all created files, handles, and shared state in teardown.
