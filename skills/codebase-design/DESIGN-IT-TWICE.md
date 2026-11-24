# Design It Twice

Explore structurally distinct candidate interfaces before committing to a module boundary.

## 1. Frame the constraints

State the boundary constraints first in project domain terms (from `GLOSSARY.md` and relevant `docs/architecture/<module>.md` if present), before proposing any interface shape:

- Caller requirements and invariants.
- Caller-owned costs that must stay explicit.
- Dependencies inside the module and their categories from [SKILL.md](SKILL.md).

## 2. Generate 2 to 3 contrasting candidates

Draft 2 to 3 structurally distinct interfaces (differing in caller responsibilities, state ownership, or seam placement), using contrasting lenses suited to the problem, such as:

- **Minimal surface**: fewest entry points, highest leverage per entry point.
- **Ergonomic default**: trivial common case with explicit opt-in controls for non-default cases.
- **Explicit-control or seam-first**: caller directly controls resource lifetimes, execution stages, or cross-boundary ports.

**Single session by default.** Draft the candidates in the current session. Dispatch parallel sub-agents (each with a **fresh context window**, never a fork inheriting parent context) only when rework cost is high and breaking anchoring bias justifies separate contexts. Pass each sub-agent the framed constraints from Step 1, one distinct design lens, and the relevant file paths and coupling facts.

For each candidate, specify:

1. **Interface**: full caller contract and explicit caller-owned costs.
2. **Caller usage**: a short realistic usage example.
3. **Hidden complexity**: what the implementation absorbs behind the interface.
4. **Seam and adapter strategy**: how each dependency category is handled.

## 3. Compare and recommend

Contrast all candidates on **depth** (leverage and locality), **explicitness of caller-owned costs**, **seam placement**, and **implementation complexity**.

End with one clear recommendation (or a concrete hybrid combining strengths across candidates), stating why it wins and which trade-off it accepts.
