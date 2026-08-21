---
name: implement
description: Implement one ready product ticket in the production application, test it, review the diff, commit it, and update status.
---

# Implement

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
