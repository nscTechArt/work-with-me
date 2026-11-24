# Architecture

Entry point to this project's module map. Each module's decisions, contracts, and traps live in its flat file under `docs/architecture/<module>.md` once authored, linked from the catalog below.

Module entry files point back to their owning architecture doc with a whole-file pointer (no `#section` fragment):

`// Contract and decisions: docs/architecture/<module>.md`

## Module Catalog

| Module | Location | Responsibility | Doc |
|---|---|---|---|
| <Module Name> | `<path>/` | <One-sentence responsibility> | [<module>.md](architecture/<module>.md) or `(none yet)` |
