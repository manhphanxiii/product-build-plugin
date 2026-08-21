---
name: to-ticket
description: Split an approved PRD and architecture into dependency-ordered vertical-slice tickets sized for one context window.
---

# To Ticket

## Root resolution

Resolve `<root>` before reading or writing anything.
Use the product repository path if the user supplied one in this invocation; otherwise run `git rev-parse --show-toplevel`.

`<root>` is valid only when `<root>/prd/roadmap.md` exists.
A repository whose root contains both `.claude-plugin/plugin.json` and `skills/start-repo/SKILL.md` is the skill-set repository and is never a valid `<root>`.

When `<root>` is invalid, print the resolved path and the reason, then look for candidates by listing sibling directories of the resolved repository that contain `prd/roadmap.md`.
Ask exactly one question using `❓ **Q0** - **<title>**` followed by `➡️ <recommended answer>` for the product repository path, recommending the single candidate when exactly one was found.
Never create chain destinations in an invalid `<root>`, never write anything into the skill-set repository, and never silently fall back to the current working directory.
When no candidate exists and the user names no repository holding `prd/roadmap.md`, stop and tell the user to run `/start-repo` first instead of asking again.

State the confirmed `<root>` once before the first read.
Every path in this skill without an explicit prefix is relative to `<root>`, never to the current working directory.
Run repository commands with `<root>` as the working directory and every Git command as `git -C <root> ...`.
Read `<root>/AGENTS.md` before the first question and before the first write, because the product repository's own agent instructions are not loaded automatically when the current working directory is elsewhere.
Follow its Conventions line about the language used with the user; when that line is absent, use the language of the user's own messages and do not ask the user to choose a language again.

## Repository destinations

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

## Next step

Recommend `/implement` as the next command, with one sentence explaining why.
Ask using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now.
If yes, tell the user to run `/clear` and then `/implement`.
If not now, stop without further action.
