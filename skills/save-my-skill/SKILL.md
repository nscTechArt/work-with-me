---
name: save-my-skill
description: Evaluate a skill against its core intent for alignment and simplicity, then discuss concrete edits.
disable-model-invocation: true
---

# Save My Skill

Evaluate a target skill against the user's **core intent** and stay read-only until the user agrees to edit.

## Setup

Locate the target `SKILL.md` and take the user's core intent; if either is missing, ask in one short question and wait.

If the target skill was written or edited earlier in this session, dispatch a read-only sub-agent with a **fresh context window** (never a fork inheriting parent context) carrying only these instructions, the target path, and the core intent.

Read only the target `SKILL.md`, any local files it explicitly links to, any skills it explicitly calls, and the enclosing repository's `AGENTS.md` (if present).

## Review

Test every clause, step, and external reference against two lenses:

- **Alignment**: anything that weakens or contradicts the core intent or `AGENTS.md`, plus any gap where a cold agent would miss the intent, hit an undefined boundary, or slip past an unenforceable rule.
- **Simplicity**: any ceremony (extra steps, coined terms, completion criteria, templates, recording rules) or duplication across the inspected files that slows down work better reasoned through directly.

Before proposing to cut or loosen a clause, steelman why it exists: keep the finding only when the burden outweighs the protection or a simpler guard covers the same risk.

## Reply

Reply in direct, plain conversation without a formal report or verdict template. If the skill is already aligned and lean, say so plainly. Otherwise, list each real issue with its exact passage, why it hurts alignment or adds burden, and a concrete edit.
