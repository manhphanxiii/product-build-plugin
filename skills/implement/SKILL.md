---
name: implement
description: Implement one ready product ticket in the production application, test it, review the diff, commit it, and update status.
disable-model-invocation: true
---

# Implement

## Repository destinations

Resolve the repository root with `git rev-parse --show-toplevel`.
Write chain documents only under `<root>/prd/`, production code only under `<root>/app/`, and prototypes only under `<root>/demos/prototypes/`.
If a destination is missing, propose its exact path and wait for approval before creating it.
Treat `client-note/` as read-only.
Read `app/knowledge-base/` freely, but never edit its runtime content by hand.
Production code may read and write runtime knowledge there as specified by the approved architecture.
Any structural change or seed data must come through an approved ticket and be documented in `prd/architecture.md`.
Do not write chain files outside these destinations.

Accept a ticket number or path.
When none is supplied, read `prd/roadmap.md` and select the first ready task whose blockers are done.
Stop and identify any unfinished blocker before changing code.

Read the selected ticket, `prd/architecture.md`, and only the relevant ADRs.
Do not reread the entire PRD.
Write all production code under `app/` and follow the tree approved in `prd/architecture.md`.

Where practical, write a test at the architecture-defined seam before production code.
Run focused tests and type checking frequently using the exact commands recorded in the `Commands` section of `AGENTS.md`.
Run the full test suite once at the end.

After the implementation passes local checks, call the Skill tool with "review-code".
Resolve every actionable finding and rerun affected checks.
Commit on the current branch with the ticket identifier in the commit message.
Change the ticket frontmatter to `Status: done`.
Update its Task row and the step 5 progress row in `prd/roadmap.md`, including the commit identifier.

## Next step

Read `prd/roadmap.md` for remaining tasks whose blockers are done and status is `ready`.
If one remains, recommend `/implement` for that ticket; otherwise recommend `/evals-gate`.
State one sentence explaining why.
Ask using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now.
If yes, tell the user to run `/clear` and then run the recommended command.
If not now, stop without further action.
