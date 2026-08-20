---
name: to-prd
description: Synthesize the approved concept and prototype decisions into a PRD, architecture document, and finalized ADR history.
disable-model-invocation: true
---

# To PRD

Do not interview again.
Synthesize only `prd/concept.md`, files under `prd/adr/`, and decisions already made during prototyping.

## Repository destinations

Resolve the repository root with `git rev-parse --show-toplevel`.
Write chain documents only under `<root>/prd/`, production code only under `<root>/app/`, and prototypes only under `<root>/demos/prototypes/`.
If a destination is missing, propose its exact path and wait for approval before creating it.
Treat `client-note/` as read-only.
Read `app/knowledge-base/` freely, but never write there because it is runtime data owned by the application.
Do not write chain files outside these destinations.

Read [PRD-TEMPLATE.md](PRD-TEMPLATE.md) and [ARCHITECTURE-TEMPLATE.md](ARCHITECTURE-TEMPLATE.md).
Draft `prd/PRD.md` with Problem, Solution, numbered User Stories, Success Metrics, and Out of Scope.
Write user stories as `As an <actor>, I want <feature>, so that <benefit>`.
Do not add a required persona field.
Draft `prd/architecture.md` with the `app/` tree, modules and interfaces, data model, main flows, test seams, external dependencies, boundaries, and accepted ADR index.
Avoid concrete file paths and code snippets in the PRD unless a prototype snippet expresses an exact decision more clearly than prose.

Finalize every ADR without deleting any ADR file.
Renumber gaps continuously while preserving slugs and updating references.
Set frontmatter `Status:` to `accepted`, `superseded by ADR-NNNN`, or `deprecated`.
When a newer decision replaces an older one, mark the older ADR as superseded and state the replacement relation in the newer ADR.
Add an ADR for any qualifying prototype decision that was not recorded.

After drafting, offer a Lavish review.
If the user agrees, call the Skill tool with "lavish".
Open Lavish `plan` and `diagram` playbooks before writing the HTML artifact, poll for annotations, and apply accepted feedback back to the Markdown sources.
Treat Markdown under `prd/` as the source of truth and `.lavish/` as a disposable review surface.
If the user wants a presentation artifact, export it to `demos/<name>/`.
Update only the step 3 row and decision index in `prd/roadmap.md`.
