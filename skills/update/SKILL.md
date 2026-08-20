---
name: update
description: Refresh evidence-backed product progress, reconcile configured sources into roadmap tasks, and optionally install a recurring update routine.
disable-model-invocation: true
---

# Update

Do not create or rebuild `prd/roadmap.md`.
Add new task rows, update changed task rows, and add unresolved conflicts to `Đang vướng`.

## Repository destinations

Resolve the repository root with `git rev-parse --show-toplevel`.
Write chain documents only under `<root>/prd/`, production code only under `<root>/app/`, and prototypes only under `<root>/demos/prototypes/`.
Routine definitions may additionally go to `<root>/routines/` and routine reports to `<root>/report/product/` after approval.
If a destination is missing, propose its exact path and wait for approval before creating it.
Treat `client-note/` as read-only.
Read `app/knowledge-base/` freely, but never write there because it is runtime data owned by the application.
Do not write chain files outside these destinations.

## Refresh progress

If `prd/roadmap.md` does not exist, stop and tell the user to run `/start-repo` first.
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

Finish with exactly one next command and one sentence explaining why it is next.
Also list the three most valuable roadmap actions in order and the current blocker, writing `none` when repository evidence shows no blocker.
Do not propose work outside the roadmap.
