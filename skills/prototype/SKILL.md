---
name: prototype
description: Resolve product and architecture uncertainty with throwaway spikes, review them visually when useful, and preserve decisions as ADRs.
---

# Prototype

## Root resolution

Resolve `<root>` before reading or writing anything.
Use the product repository path if the user supplied one in this invocation; otherwise run `git rev-parse --show-toplevel`.

`<root>` is valid only when `<root>/prd/roadmap.md` exists.
A repository whose root contains both `.claude-plugin/plugin.json` and `skills/start-repo/SKILL.md` is the skill-set repository and is never a valid `<root>`.

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

Write chain documents only under `<root>/prd/`, production code only under `<root>/app/`, and prototypes only under `<root>/demos/prototypes/`.
If a destination is missing, propose its exact path and wait for approval before creating it.
Treat `client-note/` as read-only.
Read `app/knowledge-base/` freely, but never write there because it is runtime data owned by the application.
Do not write chain files outside these destinations.

## Read the concept and split the questions

Read `prd/concept.md` and list open architecture questions.
Read its `## Surfaces and logic` section first, because the recorded surface and logic level decide how every spike is built.
Treat every cell holding `TODO - chưa xác nhận` as a paper question and settle it with the user before writing any spike.
When `prd/concept.md` has no `## Surfaces and logic` section, ask the surface and logic questions once inside the decision batch and write the answers back into the concept, because `/build:to-prd` is forbidden to interview again.
Separate questions that can be decided on paper from questions that need running code.
Decide paper questions with the user and record qualifying decisions as ADRs.

## Choose a prototype mode

Read [PROTOTYPE-MODES.md](PROTOTYPE-MODES.md) and pick the mode that matches each recorded surface and each recorded logic level.
For runnable questions, create one clearly marked throwaway spike under `demos/prototypes/<question-slug>/` after approval.
Never default to a web spike when the concept records Zero UI, because a spike on the wrong surface answers a question nobody asked.
For a Web/App spike, use multiple variants on one route controlled by a URL search parameter.
Spike only the surfaces that carry an open question, ranked by risk, instead of building one prototype per stakeholder.
Every row in the concept's stakeholder table is a spike candidate, and three stakeholders do not mean three spikes.
Spike each capability at the lowest logic level that still answers its question, and climb only when a spike has shown the lower level breaks.
When a capability is recorded as agent or skill, ask once which part of it could move down to plain code before spending a spike on it.
Represent a proposed `app/` repository structure as a text tree, not production code.

## Decide with the user

When decisions are needed, ask all current questions in one numbered batch with a recommended answer for each.
Analyze the full response before asking more.
Ask follow-ups only for contradictions, newly opened issues, or answers too vague to act on, and state which answer caused each follow-up.
Investigate repository facts yourself and leave decisions to the user.

## Always ask about Lavish

Ask about Lavish at two moments and never skip either question.
Ask before the first line of spike code at any logic level whether to open a Lavish surface for the flow diagram.
Ask again after a spike runs and before writing its ADR whether to open a Lavish surface for the review.
Use the `❓ **Q<n>** - **<title>**` block followed by `➡️ <recommended answer>` for both, and recommend yes both times.
If the user agrees, call the Skill tool with "build:lavish".
Never open Lavish without asking, and never drop the question because the spike looks small.
When the user declines, say in one sentence what is lost and move on, but still draw the flow diagram in a rough form.
For a Web/App spike, open the running spike as the review surface and collect element annotations.
For a Zero UI spike, use the `table` playbook on the transcript variants, because there is nothing to open.
For logic and architecture, use the `diagram` playbook at the first question and `comparison` at the second when several options compete, include editable Mermaid, poll for feedback, and apply feedback to the decision source.

## Record decisions as ADRs

Read [ADR-FORMAT.md](ADR-FORMAT.md).
Create an ADR only when a decision is hard to reverse, surprising without context, and the result of a real tradeoff.
Apply any whiteboard edits back to the Mermaid source before finalizing the ADR.

## Discard or promote

For every spike, ask whether to discard or promote it.
On discard, remove only that approved spike directory after its ADR exists.
On promotion, move it to `demos/<name>/` and add a Vietnamese or project-language `SCRIPT.md` presentation script.
Keep the ADR in either case.
Update only the step 2 row and related decision entries in `prd/roadmap.md`.

## Next step

Recommend `/build:to-prd` as the next command, with one sentence explaining why.
Ask using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now.
If yes, tell the user to run `/clear` and then `/build:to-prd`.
If not now, stop without further action.
