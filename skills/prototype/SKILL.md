---
name: prototype
description: Resolve product and architecture uncertainty with throwaway spikes, review them visually when useful, and preserve decisions as ADRs.
disable-model-invocation: true
---

# Prototype

## Repository destinations

Resolve the repository root with `git rev-parse --show-toplevel`.
Write chain documents only under `<root>/prd/`, production code only under `<root>/app/`, and prototypes only under `<root>/demos/prototypes/`.
If a destination is missing, propose its exact path and wait for approval before creating it.
Treat `client-note/` as read-only.
Read `app/knowledge-base/` freely, but never write there because it is runtime data owned by the application.
Do not write chain files outside these destinations.

Read `prd/concept.md` and list open architecture questions.
Separate questions that can be decided on paper from questions that need running code.
Decide paper questions with the user and record qualifying decisions as ADRs.

For runnable questions, create one clearly marked throwaway spike under `demos/prototypes/<question-slug>/` after approval.
Use multiple variants on one route controlled by a URL search parameter for UI spikes.
If the concept identified user roles, suggest one view for each relevant role, but drop the suggestion when it is not useful.
Use one runnable file and hard cases for logic or backend spikes.
Represent a proposed `app/` repository structure as a text tree, not production code.

When decisions are needed, ask all current questions in one numbered batch with a recommended answer for each.
Analyze the full response before asking more.
Ask follow-ups only for contradictions, newly opened issues, or answers too vague to act on, and state which answer caused each follow-up.
Investigate repository facts yourself and leave decisions to the user.

After a spike runs and before writing its ADR, offer a Lavish review.
If the user agrees, call the Skill tool with "lavish".
For a UI spike, open the running spike as the review surface and collect element annotations.
For architecture, use Lavish `comparison` and `diagram` playbooks before writing the HTML artifact, include editable Mermaid, poll for feedback, and apply feedback to the decision source.

Read [ADR-FORMAT.md](ADR-FORMAT.md).
Create an ADR only when a decision is hard to reverse, surprising without context, and the result of a real tradeoff.
Apply any whiteboard edits back to the Mermaid source before finalizing the ADR.

For every spike, ask whether to discard or promote it.
On discard, remove only that approved spike directory after its ADR exists.
On promotion, move it to `demos/<name>/` and add a Vietnamese or project-language `SCRIPT.md` presentation script.
Keep the ADR in either case.
Update only the step 2 row and related decision entries in `prd/roadmap.md`.

## Next step

Recommend `/to-prd` as the next command, with one sentence explaining why.
Ask using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now.
If yes, tell the user to run `/clear` and then `/to-prd`.
If not now, stop without further action.
