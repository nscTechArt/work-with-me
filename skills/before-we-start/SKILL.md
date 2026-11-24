---
name: before-we-start
description: Align on a plan with minimal user attention before building. Use before work where rework is costly, when aligning on a plan or design, or when the user asks to align before starting.
---

Align on the plan before building, spending the user's attention only where their judgement changes the outcome.

## 1. Gather facts

Look up codebase, file, and tool facts yourself before surfacing defaults or asking questions. Dispatch a sub-agent with a fresh context window when the lookup is broad.

## 2. Put defaults on the table

If the core goal is too vague to assume defaults, ask one root question to settle the direction first.

Once the core goal is clear, open with a short **Assumed defaults** list (up to 5 lines) covering the key decisions you can settle yourself: technical choices, reversible details, conventions, and clearly winning options. These are opt-out: the user interrupts only where a default is wrong. Include this list in the same message as **Q1**, or ask directly for confirmation if zero questions remain.

When a later answer settles new downstream defaults, state them in one line before the next question.

## 3. Ask only true forks, one per turn

Ask a question only when a choice is costly to reverse or materially changes the visible result, and multiple valid options exist where the user's preference decides. Skip everything else; zero questions is valid.

Ask the single highest-leverage fork first and wait for the answer before asking the next. Present named options rather than a yes/no question, describing each in plain, observable consequences and costs (gains, trade-offs, behavior changes) that require no prior context or jargon. Add a one-line fallback default when a sensible one exists, and leave it out on a root question or pure goal fork:

```
❓ **Q1** - **<fork title>**:
- **A (<label>)**: <observable consequences and costs>
- **B (<label>)**: <observable consequences and costs>

➡️ Default if you have no preference: <option and one-line reason>
```

## 4. Confirm and finish

Stop as soon as no true forks remain. Summarize the settled direction briefly and wait for explicit user confirmation before acting, even when zero questions were asked.
