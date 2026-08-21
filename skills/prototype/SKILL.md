---
name: prototype
description: Resolve product and architecture uncertainty with throwaway spikes, review them visually when useful, and preserve decisions as ADRs.
---

# Prototype

## Host resolution

Resolve the host once, before anything else, and apply these mappings for the rest of the run.
`<skill_dir>` is the directory containing this `SKILL.md`; resolve every relative reference and bundled script from that directory, never from the current working directory.
On Claude Code, commands use `/build:<skill>`, and cross-skill calls use the Skill tool with `build:<skill>`.
On Codex with the `build` plugin installed, commands use `$build:<skill>`.
On Codex with the standalone fallback installed, commands use `$<skill>`.
On Codex, a cross-skill call means reading the complete sibling file at `<skill_dir>/../<skill>/SKILL.md`, resolving its relative references from that sibling directory, passing the caller's explicit inputs, following it in place, and then returning to the caller's workflow.
Read every `/build:<skill>` mention in this skill set through the active mapping above, and read `/clear` on Codex as starting a fresh conversation.
Use the selector exposed by the current skill list when both Codex installation forms are present, preferring the namespaced plugin selector and never invoking both copies.
Use tools by capability, not by assumed host; when a named tool is unavailable, apply the fallback stated by the current phase and report the substitution in one line.

## Root resolution

Resolve `<root>` before reading or writing anything.
Use the product repository path if the user supplied one in this invocation; otherwise run `git rev-parse --show-toplevel`.

`<root>` is valid only when `<root>/prd/roadmap.md` exists.
A repository whose root contains `skills/start-repo/SKILL.md` and either `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json` is the skill-set repository and is never a valid `<root>`.

When `<root>` is invalid, print the resolved path and the reason, then look for candidates by listing sibling directories of the resolved repository that contain `prd/roadmap.md`.
Ask exactly one question using `❓ **Q0** - **<title>**` followed by `➡️ <recommended answer>` for the product repository path, recommending the single candidate when exactly one was found.
Never create chain destinations in an invalid `<root>`, never write anything into the skill-set repository, and never silently fall back to the current working directory.
When no candidate exists and the user names no repository holding `prd/roadmap.md`, stop and tell the user to run `/build:start-repo` first instead of asking again.

State the confirmed `<root>` once before the first read.
Every path in this skill without an explicit prefix is relative to `<root>`, never to the current working directory.
Run repository commands with `<root>` as the working directory and every Git command as `git -C <root> ...`.
Read `<root>/AGENTS.md` before the first question and before the first write, because the product repository's own agent instructions are not loaded automatically when the current working directory is elsewhere.
Follow its Conventions line about the language used with the user; when that line is absent, use the language of the user's own messages and do not ask the user to choose a language again.

## Repository destinations

Write chain documents only under `<root>/prd/`, production code only under `<root>/app/`, prototypes only under `<root>/demos/prototypes/`, and promoted demos only under `<root>/demos/<name>/`.
If a destination is missing, propose its exact path and wait for approval before creating it.
Treat `client-note/` as read-only.
Read `app/knowledge-base/` freely, but never write there because it is runtime data owned by the application.
Do not write chain files outside these destinations.

## Read the concept and split the questions

Read `prd/concept.md` and list open architecture questions.
Read its `## Workflow and story map` and `## Surfaces and logic` sections first, because the approved journey, recorded surface, and logic level decide how every spike is built.
Use the approved flow diagram as the starting point instead of redrawing the journey from a blank page.
Create one spike candidate for every HITL row, even when the surrounding workflow decision is already settled.
Each HITL spike targets that exact review moment and shows what the person sees and what they are allowed to do.
Treat every cell holding `TODO - chưa xác nhận` as a paper question and settle it with the user before writing any spike.
When `prd/concept.md` has no `## Workflow and story map` section, ask the tool landscape, journey, HITL, and unclear UI/UX pattern questions once inside the decision batch and write the answers back into the concept, because `/build:to-prd` is forbidden to interview again.
When `prd/concept.md` has no `## Surfaces and logic` section, ask the surface and logic questions once inside the decision batch and write the answers back into the concept, because `/build:to-prd` is forbidden to interview again.
Separate questions that can be decided on paper from questions that need running code.
Decide paper questions with the user and record qualifying decisions as ADRs.

## Choose a prototype mode

Read [PROTOTYPE-MODES.md](PROTOTYPE-MODES.md) and pick the mode that matches each recorded surface and each recorded logic level.
For runnable questions, create one clearly marked throwaway spike under `demos/prototypes/<question-slug>/` after approval.
Track and commit the spike alongside its ADR in the same PR; "throwaway" means code run once and later discarded, not uncommitted code.
Never default to a web spike when the concept records Zero UI, because a spike on the wrong surface answers a question nobody asked.
For a Web/App spike, use multiple variants on one route controlled by a URL search parameter.
Spike only the surfaces that carry an open question, ranked by risk, instead of building one prototype per stakeholder.
Every row in the concept's stakeholder table is a spike candidate, and three stakeholders do not mean three spikes.
Spike each capability at the lowest logic level that still answers its question, and climb only when a spike has shown the lower level breaks.
Represent a proposed `app/` repository structure as a text tree, not production code.

## Decide with the user

When decisions are needed, ask all current questions in one numbered batch with a recommended answer for each.
Analyze the full response before asking more.
Ask follow-ups only for contradictions, newly opened issues, or answers too vague to act on, and state which answer caused each follow-up.
Investigate repository facts yourself and leave decisions to the user.

Read [ADR-FORMAT.md](ADR-FORMAT.md).
For every spike, ask whether to discard or promote it before building the review draft.
After every spike in the current batch has run, build the review draft as the complete ADR set defined by [ADR-FORMAT.md](ADR-FORMAT.md), the discard or promote conclusion for each spike, and the proposed step 3 roadmap row.
For a Web/App spike, include the running spike as a matching review surface when it helps the user annotate elements.
For a Zero UI spike, use the `table` playbook for transcript variants.
For logic and architecture, use `diagram`, and add `comparison` when several options compete.

## Review gate

Run this gate after the last question of this skill is answered and before writing every document this skill is about to write.
Build the full draft of every document this skill is about to write, show it on a review surface, and revise it until the user approves.
Never write the final file before that approval.

Choose the surface with this probe and state the chosen surface in one line before rendering.
Run the probe as two separate commands and judge each one by its own exit status.
Never join the CLI check and the browser-opener check into one chained command, because the platform branch that does not apply always exits non-zero and would make a working setup read as a failure.

1. Prefer Lavish.
   Lavish is usable when its CLI runs, any required package is already installed or network access is available, and a local browser can be opened.
   Check one: `npx -y lavish-axi --help` must exit 0.
   Check two: run `command -v open` on macOS or `command -v xdg-open` on Linux, and only the command for the current platform must exit 0.
   The probe passes when both checks pass, and a non-zero exit from the opener that does not belong to the current platform means nothing.
   When `npx -y` exits opaquely, retry once with `lavish-axi --help`; if that binary is unavailable, run `npm root -g`, then run `node <global-node-modules>/lavish-axi/dist/cli.mjs --help` using the printed path before declaring Lavish unusable.
2. When the probe fails and both the Artifact tool and `artifact-design` skill are available, use the Artifact tool.
   Lavish serves the artifact from a local Express server, so a session whose browser is not on this machine, such as a cloud session, cannot see the page and its poll would wait forever.
   Lavish drafts are temporary and do not survive a cloud session.
3. When neither surface is available, print the draft in the conversation as Markdown and collect approval there.
   A user-started asynchronous cloud run is interactive across turns: print the Markdown draft, stop before writing any approval-gated file, and wait for explicit approval in a follow-up.

With Lavish, invoke `lavish` through the active host mapping in `## Host resolution`.
Open every playbook that matches the draft, and always open `input`, because this gate collects a decision.
Poll for feedback, apply every returned prompt, and poll again until the user approves or ends the session.
Prefer a harness-native tracked background job whose completion result is guaranteed to resume or notify the same agent, because a real human review usually outlasts any foreground command timeout.
Read the delivered output completely when the harness resumes or notifies the agent, because poll delivery consumes the response.
Use a foreground poll only when the harness exposes no such facility, and expect it to need re-running.
Create the artifact at `<root>/.lavish/<name>.html` and pass lavish-axi that absolute path, because the current working directory may not be `<root>` and the relative default would write the artifact into an unrelated repository.
State that artifact path in one line, and add that the user may reply `artifact` to switch surfaces if the page does not open for them.

With the Artifact tool, load the `artifact-design` skill first, write the draft to a file in the session scratchpad, publish it, and give the user the link.
The user approves or gives feedback in this conversation.
Read comment threads with the Artifact tool's `comments` action when the user says they commented on the page.
Republish the same file path after each revision so the link stays stable.

`prd/` stays the source of truth, and both `.lavish/` and the published artifact are disposable review surfaces.
Skip this gate only for genuinely unattended automation with no user available to approve a draft; a user-started asynchronous cloud run does not qualify.

## Record decisions as ADRs

Create an ADR only when a decision is hard to reverse, surprising without context, and the result of a real tradeoff.
Apply any whiteboard edits back to the Mermaid source before finalizing the ADR.

## Discard or promote

On discard, remove only that approved spike directory after its ADR exists.
On promotion, move it to `demos/<name>/` and add a Vietnamese or project-language `SCRIPT.md` presentation script.
Keep the ADR in either case.
Update only the step 3 row and related decision entries in `prd/roadmap.md`.

## Next step

Recommend `/build:to-prd` as the next command, with one sentence explaining why.
Ask whether to continue now using the next question number after the last one used, formatted as `❓ **Q<n>** - **<title>**` followed by `➡️ <recommended answer>`.
If yes, tell the user to run `/clear` and then `/build:to-prd`.
If not now, stop without further action.
