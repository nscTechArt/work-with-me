---
name: repo-docs
description: Living repository docs and governance. Use when creating, editing, splitting, or auditing docs/, GLOSSARY.md, AGENTS.md routes, code pointers, or .scratch/ lifecycle (including close-out cleanup).
---

# Living Repository Docs and Governance

Living repository docs exist for agents and maintainers reading the current codebase (pair with `writing-for-agents` when authoring skills or `AGENTS.md`). Follow repository-specific doc conventions when present.

## Inclusion Test

Keep a sentence only if deleting it would cause an agent reading current code and inline comments to violate a confirmed decision or repo convention, break a cross-file invariant, or hit a hidden trap.

- **Keep code-derivable facts in code:** data tables, field/flag inventories, signatures, and algorithm steps belong in code or inline comments.
- **Short by omission, not compression:** put one rule or fact per bullet in 1 to 2 short sentences rather than packing clauses into a dense paragraph.
- **Single-site vs cross-site:** rationale bearing on one code site lives in an inline comment; cross-file decisions, contracts, and traps live in `docs/architecture/`.

## Fact Owners

Each fact has one owning document; other files link instead of restating it. On a shared resource, each module owns what it writes. Record product or compatibility decisions only after explicit maintainer confirmation. Use the default owners below alongside any repo-specific standing docs routed in root `AGENTS.md` (repo routes take precedence on overlap):

| Fact | Owner |
|---|---|
| Cross-task working rules, verification mode, top 1 to 2 product redlines | Root `AGENTS.md` |
| All other confirmed product boundaries and external compatibility commitments | `docs/product-scope.md` (or root `AGENTS.md` when small) |
| Module catalog and whole-file code pointer convention | `docs/architecture.md` |
| Module technical decisions, cross-site contracts, and non-local traps | `docs/architecture/<module>.md` |
| Evidence grading, falsification, and clean-context review rules | `docs/evidence-model.md` |
| Test admission policy, mocking boundaries, and verification modes | `docs/testing.md` |
| Collision-prone domain terms and cross-module abstractions | `GLOSSARY.md` |
| Disposable research, specs, and multi-session tickets | `.scratch/<slug>/` |
| Change history and rejected designs (outside Traps) | Git only |

## Module Docs (`docs/architecture/<module>.md`)

Keep one flat file per module under **1,500 words** (`wc -w` on Markdown source). When a file approaches or exceeds 1,500 words, prune code-derivable prose first or split independent sub-domains into sibling files and update `docs/architecture.md`. Group bullets under three headings:

1. **Decisions:** choices with a non-obvious Why (deliberate omissions, accepted trade-offs, cross-site departures from an external specification or reference). Decisions are **revisitable by default**; mark rare maintainer-locked choices explicitly. When editing a module file, clean legacy bullets in that file lacking a non-obvious Why or mark useful unexplained ones as `"reason not recorded"` without digging through git history.
2. **Contracts:** cross-file or cross-module invariants an agent editing one side could break without reading the other (formats, ownership, lifetime, ordering, neutral values, non-obvious coupling).
3. **Traps:** counter-intuitive intentional code, platform/runtime hazards, or plausible-looking designs that fail, each with its reason in one clause.

## Code Pointers and Inline Comments

An inline comment must be **non-derivable**, **site-bound**, and **durable**.

- **Module pointer:** link a whole module doc file without any `#section` fragment at module entry files (or every module-owned file when required by repo policy):
  `// Contract and decisions: docs/architecture/<module>.md` (use `#` in Python/shell).
- **Intentional-trap or reference-departure guardrail:** write 1 to 2 self-contained sentences directly at the counter-intuitive line explaining why not to "fix" it, without relying on fragile doc heading anchors.

## Glossary (`GLOSSARY.md`)

Create `GLOSSARY.md` at the repo root lazily when terms settle. Include a term only when it meets at least one criterion:

1. **Collision risk** with a framework, standard, library, or another project term.
2. **Non-self-evident cross-module abstraction** not obvious from a class or file name.

Entry format:

```markdown
**Term Name**:
One sentence identifying what it is and any term it is distinct from.
_Also called_: Real synonym (Source).
```

Use `_Also called_` for real synonyms only, and never include an `_Avoid_` line. Exclude general programming terms and module-local details; behavior belongs in the owning module doc. Remove terms no current code or doc uses.

## Disposable Drafts (`.scratch/`)

- **Keep `.scratch/` unreferenced:** cite only living docs or code from repository files and comments, never `.scratch/`.
- **Close and delete on maintainer confirmation:** when work finishes, sync surviving decisions, contracts, traps, and terms into living docs in the same change, and note that `.scratch/<slug>/` is ready to delete once verification is accepted. Physically delete `.scratch/<slug>/` (and empty `.scratch/` unless kept by repo convention) only after explicit maintainer confirmation, never archiving completed drafts.

## Repo Governance and Route Audit

- **Single root entry:** keep standing rules in one root `AGENTS.md` (no subdirectory `AGENTS.md` or tool-specific mirrors such as `CLAUDE.md`, `GEMINI.md`, or `.claude/`), project skills in `.agents/skills/`, and task-triggered standards under `docs/` with direct 1-hop routes in `AGENTS.md`.
- **Hard guards and hygiene checks:** when the repository uses `.agents/` guardrails, enforce zero-exception tool and write bans in `.agents/hooks.json` and `.agents/scripts/pre_tool_guard.py`, and keep mechanical doc or code checks in `.agents/scripts/check_repo_hygiene.py`.
- **Reference sync:** when moving, renaming, splitting, or removing any living doc, skill, or heading, repair every inbound link, backticked repo path, `AGENTS.md` route, and code module pointer in the same change.
- **Route audit:** when auditing agent docs or editing `AGENTS.md` pointers, trace each common task from `AGENTS.md` following only pointers and fix three defects: **Gap** (needed doc unreachable or trigger too vague), **Conflict** (fact duplicated or outside its owner), and **Excess** (unrelated material loaded on the route).
