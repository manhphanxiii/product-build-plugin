---
name: update
description: Refresh evidence-backed product progress, reconcile configured sources into roadmap tasks, and optionally install a recurring update routine.
---

# Update

Do not create or rebuild `prd/roadmap.md`.
After approval, this skill may update only step 2 through 7 progress rows, the weekly goal, Out of scope, Task rows, `Đang vướng`, and `## Bước kế tiếp`, while preserving step 1 and externally sourced Task rows; it may also write the dated report and, in Routine mode, the approved routine definition.

## Phase 0: choose the conversation language

Before anything else in an interactive run, ask exactly one question using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>`.
Ask whether to use Vietnamese or English for this conversation, recommending the language of the user's own messages.
This question sets only the conversation language for this run; content written into `prd/roadmap.md` stays in whatever language the file already uses, so the file is never mixed.
Use the chosen language from the next message onward, including the root question in the next section.

Skip this question and the Review gate when the run has no one to ask, such as a routine, morning brief, Stop hook, or `/loop` invocation.
In that case, read the Conventions line in `<root>/AGENTS.md` and use its language instead.

## Root resolution

Resolve `<root>` before reading or writing anything.
Use the product repository path if the user supplied one in this invocation; otherwise run `git rev-parse --show-toplevel`.

`<root>` is valid only when `<root>/prd/roadmap.md` exists.
A repository whose root contains both `.claude-plugin/plugin.json` and `skills/start-repo/SKILL.md` is the skill-set repository and is never a valid `<root>`.

When `<root>` is invalid, print the resolved path and the reason, then look for candidates by listing sibling directories of the resolved repository that contain `prd/roadmap.md`.
Ask exactly one question using `❓ **Q2** - **<title>**` followed by `➡️ <recommended answer>` for the product repository path, recommending the single candidate when exactly one was found.
Never create chain destinations in an invalid `<root>`, never write anything into the skill-set repository, and never silently fall back to the current working directory.
When no candidate exists and the user names no repository holding `prd/roadmap.md`, stop and tell the user to run `/build:start-repo` first instead of asking again.

State the confirmed `<root>` once before the first read.
Every path in this skill without an explicit prefix is relative to `<root>`, never to the current working directory.
Run repository commands with `<root>` as the working directory and every Git command as `git -C <root> ...`.
Read `<root>/AGENTS.md` before the first question and before the first write, because the product repository's own agent instructions are not loaded automatically when the current working directory is elsewhere.
When its Conventions line names a language different from the one chosen in Phase 0, use the Phase 0 choice for this run, print one line noting the mismatch, and do not edit `AGENTS.md`; only `/build:start-repo` writes that file.

## Repository destinations

Write chain documents only under `<root>/prd/`, production code only under `<root>/app/`, and prototypes only under `<root>/demos/prototypes/`.
Routine definitions may additionally go to `<root>/routines/` and routine reports to `<root>/report/product/` after approval.
If a destination is missing, propose its exact path and wait for approval before creating it.
Treat `client-note/` as read-only.
Read `app/knowledge-base/` freely, but never write there because it is runtime data owned by the application.
Do not write chain files outside these destinations.

## Refresh and report

Read the roadmap and gather evidence for the progress rows within the scope above only from repository evidence such as existing artifacts, tickets with `Status: done`, recorded commits, and the latest eval result.

Read the `Nguồn thông tin` section in `prd/README.md` and [SOURCES.md](SOURCES.md).
State every disabled source that will be skipped.
When delegation is available and authorized, scan each enabled source with a separate sub-agent to keep evidence contexts independent.
Every proposed row must cite a concrete source.

Merge duplicate work found in several sources into one row and list every source in `Nguồn`.
When sources disagree about the status of the same work, do not choose a winner.
Propose an entry under `Đang vướng` with both sources and ask the user to resolve it.

Print the report using [REPORT-FORMAT.md](REPORT-FORMAT.md): exactly three parts, roadmap progress with the proposed diff grouped as new tasks, status changes, and conflicts; current task listing every open task in priority order and ending with one recommended next command; and an optional note, omitted entirely when there is nothing to note.
Update the fields listed in the scope above from `prd/concept.md` and actual progress without inventing evidence.

Build the review draft as the proposed roadmap-row diff and the complete `report/product/roadmap-<YYYY-MM-DD>.md` content.

## Review gate

Run this gate after the last question of this skill is answered and before writing every document this skill is about to write.
Build the full draft of every document this skill is about to write, show it on a review surface, and revise it until the user approves.
Never write the final file before that approval.

Choose the surface with this probe and state the chosen surface in one line before rendering.

1. Prefer Lavish.
   Lavish is usable when its CLI runs and a local browser can be opened: `npx -y lavish-axi --help` exits 0, and `command -v open` resolves on macOS or `command -v xdg-open` resolves on Linux.
   When `npx -y` exits opaquely, retry once with `node "$(npm root)/lavish-axi/dist/cli.mjs" --help` before declaring Lavish unusable.
2. When the probe fails, use the Artifact tool.
   Lavish serves the artifact from a local Express server, so a session whose browser is not on this machine, such as a cloud session, cannot see the page and its poll would wait forever.
   Lavish drafts are temporary and do not survive a cloud session.
3. When neither surface is available, print the draft in the conversation as Markdown and collect approval there.

With Lavish, call the Skill tool with "build:lavish".
Open every playbook that matches the draft, and always open `input`, because this gate collects a decision.
Poll for feedback, apply every returned prompt, and poll again until the user approves or ends the session.
State the artifact path in one line, and add that the user may reply `artifact` to switch surfaces if the page does not open for them.

With the Artifact tool, load the `artifact-design` skill first, write the draft to a file in the session scratchpad, publish it, and give the user the link.
The user approves or gives feedback in this conversation.
Read comment threads with the Artifact tool's `comments` action when the user says they commented on the page.
Republish the same file path after each revision so the link stays stable.

`prd/` stays the source of truth, and both `.lavish/` and the published artifact are disposable review surfaces.
Skip this gate when the skill runs non-interactively, because no user is present to approve a draft.

After approval, apply only the scope defined above.
State in one line what was actually applied.
Do not propose work outside the roadmap.

Ask using `❓ **Q3** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now with the recommended next command.
If yes, tell the user to run `/clear` and then run that command.
If not now, stop without further action.

## Routine mode

Read [ROUTINE-SETUP.md](ROUTINE-SETUP.md).
Offer Stop hook, `/loop`, and scheduled routine options with their tradeoffs.
After the user selects and approves a setup, write its definition to `routines/update-roadmap.md` and append each run report as `report/product/roadmap-<YYYY-MM-DD>.md`.
Run the approved routine once after setup so its first dated report exists.
Show the exact `.claude/settings.json` change and obtain separate approval before writing it.
