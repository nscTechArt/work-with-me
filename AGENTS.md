# Work With Me

Personal AI collaboration workflow and reusable project governance templates for solo software engineering. Maintained independently with no releases and no marketplace packaging.

## Layout

- `skills/<name>/SKILL.md`: installable global workflow skills.
- `skills/init-project/templates/`: reusable project templates (`AGENTS.md`, standing `docs/`, and `.agents/` guard scripts) kept inside `init-project` so `/init-project` can access them from any repository after local sync.
- `scripts/sync-skills.ps1`: local Windows sync script for agent skill junctions and Antigravity config.

## Conventions

- **Invocation**: every `SKILL.md` is either user-invoked (`disable-model-invocation: true`, concise human-facing `description`, never invoked by other skills; tell the user to run `/<name>` instead) or model-invoked (omit `disable-model-invocation`, write concrete `"Use when..."` trigger conditions).
- **Standing docs vs skills**: static project norms (`docs/product-scope.md`, `docs/evidence-model.md`, `docs/testing.md`, `docs/architecture/`) live as project docs provisioned via `skills/init-project/templates/`, not as global rule-manual skills. Global skills carry reusable workflows and fall back inline when a small repo has not provisioned `docs/`.
- **Skill dependencies**: never link across skill folders with `../`; call another model-invoked skill via the Skill tool (one skill per call) only when delegating a shared workflow. Merely reading `GLOSSARY.md` or `docs/` does not require a skill call.
- **Language**: write skill instructions in English.
- **Punctuation**: no em-dashes anywhere in this repo's prose (`SKILL.md` files, docs, comments). Rewrite with commas, colons, periods, parentheses, or conjunctions instead.
- **Fresh sub-agents**: every skill that dispatches a sub-agent must state that it starts with a fresh context window (never a fork inheriting parent context).
- **Local sync**: whenever a skill under `skills/` is added, renamed, or removed, run `.\scripts\sync-skills.ps1` to refresh local Windows agent directory junctions.
- **Working tree**: leave edits uncommitted for user review unless the user explicitly asks to commit.
