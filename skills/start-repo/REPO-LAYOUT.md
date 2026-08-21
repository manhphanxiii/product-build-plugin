# Repository Layout

Use `<root>` resolved in phase 0.

Every artifact must answer a clear workspace question.

| Question | Canonical location |
|---|---|
| Where does production work happen? | `app/` |
| How is work performed here? | `AGENTS.md` |
| What evidence and runtime context matter? | `client-note/` and `app/knowledge-base/` |
| What is being built now? | `prd/roadmap.md` and the remaining documents in `prd/` |
| Is it good enough to ship? | `prd/evals/` |
| What repeats and when? | `routines/` |
| What did those routines produce? | `report/` |
| What can be shown to a customer? | `demos/` |

| Path | Purpose | Write policy |
|---|---|---|
| `<root>/app/` | Production application | Production code only |
| `<root>/app/knowledge-base/` | Runtime knowledge read and written by the application | Agents may read but never edit runtime content by hand |
| `<root>/client-note/` | Verbatim customer voice | Read-only for agents |
| `<root>/prd/` | Concept, PRD, architecture, ADRs, tickets, evals, and roadmap | Chain documents only |
| `<root>/demos/` | Throwaway prototypes and promoted demos | Prototypes start under `demos/prototypes/` |
| `<root>/routines/` | Recurring workflow definitions | Write only after approval |
| `<root>/report/` | Dated routine output | Product reports go under `report/product/` |

`/start-repo` always seeds `routines/weekly-ops-review.md` and `routines/pr-auto-review.md`.
It seeds `routines/update-roadmap.md` only when the user approves a morning brief in phase 4b; `/update` owns refreshing that file afterward.

The six top-level destinations answer where production code, evidence, plans, demonstrations, recurring work, and dated output belong.
Root governance files answer how work is performed.

| Canonical fact | Source |
|---|---|
| Repository commands, conventions, constraints, and completion rules | `AGENTS.md` |
| Product, buyer, and promise | `prd/concept.md` |
| Product progress and out of scope | `prd/roadmap.md` |
| Product behavior | `prd/PRD.md` |
| System structure and boundaries | `prd/architecture.md` |
| Architectural rationale | `prd/adr/` |
| Ship quality | `prd/evals/` |

Never silently create a missing destination.
Show its exact path, purpose, and proposed initial README, then wait for approval.

## Linked layout

In `restructure` mode, some canonical paths may be symlinks to matching existing folders.
The write policy for a role does not change when the role is a symlink, but every write through it changes the real target and belongs to the Git repository containing that target.
When `app/` is a symlink, do not create `app/knowledge-base/`; keep it as a TODO until `prd/architecture.md` defines runtime data behavior.
The repository-specific mapping between canonical roles and real paths lives only in `AGENTS.md` and must not be copied to another file.
