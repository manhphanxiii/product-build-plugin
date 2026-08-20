---
name: to-ticket
description: Split an approved PRD and architecture into dependency-ordered vertical-slice tickets sized for one context window.
disable-model-invocation: true
---

# To Ticket

## Repository destinations

Resolve the repository root with `git rev-parse --show-toplevel`.
Write chain documents only under `<root>/prd/`, production code only under `<root>/app/`, and prototypes only under `<root>/demos/prototypes/`.
If a destination is missing, propose its exact path and wait for approval before creating it.
Treat `client-note/` as read-only.
Read `app/knowledge-base/` freely, but never write there because it is runtime data owned by the application.
Do not write chain files outside these destinations.

Read `prd/PRD.md`, `prd/architecture.md`, and all ADRs under `prd/adr/`.
Split work into thin vertical slices that cross the required schema, API, UI, and test layers, can be demonstrated independently, and fit one context window.
Order tickets by dependency.

Before writing files, show a numbered proposal with Title, Blocked by, and independently deliverable outcome.
Ask whether ticket size is right, dependency edges are right, and any ticket should be merged or split.
Revise until the user approves.

Read [TICKET-TEMPLATE.md](TICKET-TEMPLATE.md).
Write one approved ticket per file at `prd/tickets/NN-<slug>.md`, starting at `01`.
Set `Status: ready` unless repository evidence requires another state.
Declare `Blocked by` explicitly, using `none` where appropriate.
Add one row per ticket to the roadmap Task table with the ticket path in `Nguồn`.
Update only the step 4 row and the inserted task rows in `prd/roadmap.md`.
