---
name: retro
description: Conduct a retrospective on a coding session to improve AGENTS.md, hooks, living docs, and skills.
disable-model-invocation: true
---

# Retrospective

Review a completed coding session and propose concrete improvements to the coding agent's **environment** (`AGENTS.md`, hooks, living docs, skills, or local checks) ranked by severity.

Call the Skill tool twice, for "writing-for-agents" and "repo-docs".

## Steps

1. **Read primary sources.** Inspect the session specified by the user (defaulting to the current session and its git diff or logs).
2. **Identify improvements across categories:**
   - **Navigation and doc routes**: did the agent miss a file or contract, or load excess context? Run the `repo-docs` route audit (Gap, Conflict, Excess) and sharpen conditional pointers in `AGENTS.md` or whole-file code module pointers.
   - **Hard guardrails (hooks and local checks)**: did the agent break a zero-exception rule (banned command, generated directory edit, mechanical syntax or lint violation)? Prefer a deterministic hook or local linter/script over adding prose rules. Skip proposing CI pipelines for solo repos that do not use CI.
   - **Living module docs**: did the agent hit an undocumented trap, cross-site contract, or stale decision reason? Add or update it in its single owning module file under `docs/architecture/` (within the 1,500-word limit).
   - **Always-loaded bloat and no-ops**: trim `AGENTS.md` lines that duplicate code/environment facts or state defaults the model already obeys. Move branch-specific guidance behind conditional pointers or skills.
   - **Review rules**: if a reviewer missed a non-mechanical defect (judgement call no tool can catch), tighten the relevant review skill or project convention.
   - **Tool and token economy**: flag repeated expensive commands or missing read-only access that wasted turns.
3. **Present findings.** List concrete, actionable proposals ordered by impact, naming the exact owning file for each change. Do not edit files until the user confirms which proposals to apply.
