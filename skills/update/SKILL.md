---
name: update
description: Refresh evidence-backed product progress, reconcile configured sources into roadmap tasks, and optionally install a recurring update routine.
disable-model-invocation: true
---

# Update

Do not create or rebuild `prd/roadmap.md`.
Add new task rows, update changed task rows, and add unresolved conflicts to `Đang vướng`.

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
Routine definitions may additionally go to `<root>/routines/` and routine reports to `<root>/report/product/` after approval.
If a destination is missing, propose its exact path and wait for approval before creating it.
Treat `client-note/` as read-only.
Read `app/knowledge-base/` freely, but never write there because it is runtime data owned by the application.
Do not write chain files outside these destinations.

## Refresh progress

Read the roadmap and refresh the six-step progress table only from repository evidence such as existing artifacts, tickets with `Status: done`, recorded commits, and the latest eval result.
Update the weekly goal and Out of scope from `prd/concept.md` together with actual progress.
Do not recreate the file, remove externally sourced Task rows, or invent progress.

Read the `Nguồn thông tin` section in `prd/README.md` and [SOURCES.md](SOURCES.md).
State every disabled source that will be skipped.
When delegation is available and authorized, scan each enabled source with a separate sub-agent to keep evidence contexts independent.
Every proposed row must cite a concrete source.

Merge duplicate work found in several sources into one row and list every source in `Nguồn`.
When sources disagree about the status of the same work, do not choose a winner.
Propose an entry under `Đang vướng` with both sources and ask the user to resolve it.

Before writing, show a diff grouped as new tasks, status changes, and conflicts.
Wait for approval, then modify only the affected roadmap rows and blocker entries.

## Routine mode

Read [ROUTINE-SETUP.md](ROUTINE-SETUP.md).
Offer Stop hook, `/loop`, and scheduled routine options with their tradeoffs.
After the user selects and approves a setup, write its definition to `routines/update-roadmap.md` and append each run report as `report/product/roadmap-<YYYY-MM-DD>.md`.
Run the approved routine once after setup so its first dated report exists.
Show the exact `.claude/settings.json` change and obtain separate approval before writing it.

## Next step

Recommend exactly one next command and one sentence explaining why it is next.
Also list the three most valuable roadmap actions in order and the current blocker, writing `none` when repository evidence shows no blocker.
Ask using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now.
If yes, tell the user to run `/clear` and then run the recommended command.
If not now, stop without further action.
Do not propose work outside the roadmap.
