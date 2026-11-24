---
name: init-project
description: Guided onboarding and checkup for a repository's AGENTS.md, standing docs, and .agents/ guardrails from templates.
disable-model-invocation: true
---

# Init Project

Run a transparent, guided onboarding or checkup for a new or existing repository using the templates bundled in [`templates/`](templates/).

## 1. Inspect the repository

Read the repository before proposing anything:

- Check root `AGENTS.md`, `CLAUDE.md`, and duplicate mirrors (`CLAUDE.md`, `GEMINI.md`, `.claude/`, or subdirectory `AGENTS.md` files).
- Detect the primary language, source directories, build/test tooling, and verification mode: whether agents can safely run local builds and tests (for example, `npm test`, `pytest`, `cargo test`, `go test`) versus an external GUI or engine where the maintainer owns execution.
- Inspect existing `docs/` (`product-scope.md`, `architecture.md`, `architecture/`, `evidence-model.md`, `testing.md`), `GLOSSARY.md`, `.agents/hooks.json`, and `.agents/scripts/`, comparing any existing files against their counterparts in `templates/` to spot missing sections or template drift.
- Check whether the codebase already has distinct modules and whether there are generated/uneditable directories or commands agents must not run.

## 2. Present full checklist and confirm in one round

Keep onboarding scoped to the six template areas below unless the maintainer asks for more. Present one concise checklist covering all six areas with a plain one-line gloss of each file's stance or role, its current status, and a recommended action (`install`, `update` with a one-line summary of concrete template additions or differences, or `skip` with a brief reason). Bundle every human-only decision into **at most one short confirmation block** with sensible defaults (never multi-turn interrogation):

1. **Root `AGENTS.md`** ([`templates/AGENTS.md`](templates/AGENTS.md)): single cross-tool entry point for project facts, verification mode, and 1-hop routes to existing files. Confirm the detected (or ask for the planned) one-sentence project summary and verification mode, plus any proposed `CLAUDE.md` merge or duplicate-mirror cleanup.
2. **Product scope and compatibility boundaries** ([`templates/docs/product-scope.md`](templates/docs/product-scope.md)): confirmed platform assumptions, core capabilities, exclusions, and external compatibility commitments. Ask for any binding redlines; keep the top 1 to 2 in `AGENTS.md`, and create or update `docs/product-scope.md` when boundaries grow beyond a few bullets or when the maintainer wants it now.
3. **Testing policy (`docs/testing.md`)** ([`templates/docs/testing.md`](templates/docs/testing.md)): cheapest reliable lock first, risk-based test admission criteria, real internal collaborators with boundary-only mocks, and post-task test pruning. **Recommended ON (install) by default** for both new and existing repositories (opt-out to skip); ask whether to tailor any rules to the repo's stack or verification mode.
4. **Evidence model (`docs/evidence-model.md`)** ([`templates/docs/evidence-model.md`](templates/docs/evidence-model.md)): grading load-bearing claims, falsifying findings against counter-evidence, and clean-context reviews. **Recommended ON (install) by default** for both new and existing repositories (opt-out to skip; especially valuable when runtime verification is maintainer-owned or invariants are high).
5. **Architecture catalog (`docs/architecture.md`)** ([`templates/docs/architecture.md`](templates/docs/architecture.md)): module map linking code to per-module decisions, contracts, and traps. Recommend skipping on repositories without distinct modules yet (brand-new or small flat repos; it can be added later via `repo-docs`). On repositories with distinct modules, draft the `docs/architecture.md` module catalog leaving unauthored module docs as `(none yet)` so link checks pass, and leave individual `docs/architecture/<module>.md` files to grow lazily when modules are touched.
6. **Guardrails (`.agents/`)** ([`templates/.agents/hooks.json`](templates/.agents/hooks.json), [`templates/.agents/scripts/pre_tool_guard.py`](templates/.agents/scripts/pre_tool_guard.py), [`templates/.agents/scripts/check_repo_hygiene.py`](templates/.agents/scripts/check_repo_hygiene.py)): static link/pointer/hygiene checks and `PreToolUse` command/path blocks. Recommend skipping on brand-new or small repositories that only have `testing.md` and `evidence-model.md`; recommend `check_repo_hygiene.py` once `docs/architecture.md` or growing living docs exist, and recommend `hooks.json` plus `pre_tool_guard.py` when the repo has banned commands, generated/uneditable directories, or wants hook enforcement against duplicate rule files (`.agents/hooks.json` uses Antigravity's `PreToolUse` format; `pre_tool_guard.py` handles both Antigravity and Claude Code payloads, so another harness only needs its own hook registration config).

Stop after presenting the checklist and confirmation block; wait for the maintainer's reply before creating or editing any file.

## 3. Apply and update incrementally

After maintainer confirmation:

- **Safe incremental merges:** merge only the approved template additions into existing customized `AGENTS.md`, `docs/`, or `.agents/` files while preserving repo-specific sections, rules, and custom checks.
- Write or update root `AGENTS.md`: strip template HTML comments, fill all `<...>` placeholders (write `- None confirmed yet.` under `Product Scope` if no redlines were confirmed), migrate unique rules from any confirmed `CLAUDE.md` merge and remove confirmed redundant mirrors, and keep 1-hop `Read Before Acting` routes pointing only to files that exist in the repository.
- Copy or merge approved `docs/` templates and tailor obvious repo facts; leave unconfirmed product decisions in `docs/product-scope.md` as explicit placeholders for maintainer input rather than inventing decisions.
- When installing or updating `.agents/scripts/check_repo_hygiene.py`: configure `CODE_DIRS`, `CODE_EXTS`, `REQUIRE_HEADER_POINTER`, and `UNOWNED_CODE_FILES`, add the `check_repo_hygiene.py` verification line to `AGENTS.md`, and run `python -B .agents/scripts/check_repo_hygiene.py` (fixing any failures before finishing when Python is available).
- When installing or updating hook enforcement: copy or update `.agents/hooks.json` (or adapt hook registration for another harness) and `.agents/scripts/pre_tool_guard.py`, and configure `BANNED_EDIT_TOP_DIRS` and `BANNED_COMMAND_PATTERNS`.
- Leave all edits uncommitted in the working tree for review, and remind the maintainer that repo-specific domain skills live in `.agents/skills/` and override global skills.
