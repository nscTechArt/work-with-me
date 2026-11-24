---
name: are-you-sure
description: Challenge a proposed software-engineering or technical-project solution before adopting it.
disable-model-invocation: true
---

# Are You Sure?

Challenge the most recent concrete technical proposal in the conversation before adopting it. Stay strictly read-only: leave tracked files, configuration, dependencies, and persistent data as you found them, and delete any temporary diagnostic files before replying.

Follow `docs/evidence-model.md` if present (otherwise verify every load-bearing claim against the current checkout, seek counter-evidence to falsify findings before reporting, and state what is unknown, what was inspected, impact, and cheapest check for unresolved claims). When challenging a proposal written in the same session, dispatch a read-only sub-agent with a **fresh context window** (never a fork inheriting parent context) when available so the critique does not anchor on prior reasoning.

## 1. Pin down the goal

State in one plain sentence the real problem, core goal, and hard constraints, leaving out the proposal's mechanisms. Ask one focused question and wait only if no concrete proposal exists or an unresolved trade-off changes the verdict; otherwise proceed directly.

## 2. Check the facts

Treat the proposal and its earlier rationale as an unverified hypothesis to falsify. Inspect relevant code, call sites, tests, configuration, and existing capabilities, starting with facts that could falsify the proposal or render it unnecessary. Run safe, local checks when they settle a factual question.

Before moving to Step 3, verify that every load-bearing assumption in the proposal has a specific file reference, a check result, or an explicit uncertainty.

## 3. Challenge the proposal

Focus strictly on issues that change whether the goal is met or what meeting it costs:

- **Effectiveness**: Does the proposal meet the goal and constraints, and do its load-bearing assumptions survive falsification?
- **Simplicity**: Identify the strongest simpler alternative (doing nothing, deferring, reusing an existing project, standard-library, or dependency capability, or trimming the proposal) and test whether it meets the goal with less machinery.
- **Consequences**: What new coupling, regression risk, migration cost, security exposure, or maintenance burden does adoption introduce?

## 4. Deliver the verdict

Recommend adopting as-is only when evidence rules out the strongest simpler alternative and every load-bearing assumption holds. Reply in the user's language with:

- **Goal**: the one-sentence goal and constraints used as the benchmark.
- **Verdict**: **Adopt as-is**, **Simplify or modify**, **Replace or drop**, or **Hold** (missing facts or user trade-off).
- **Findings**: concise, evidence-backed points for Effectiveness, Simplicity (compared directly against the strongest simpler alternative), and Consequences.
- **Recommendation**: concrete changes to make, the simpler alternative to take instead, or the single question needed to unblock a Hold.
