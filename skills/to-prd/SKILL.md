---
name: to-prd
description: Synthesize the approved concept and prototype decisions into a PRD, architecture document, and finalized ADR history.
disable-model-invocation: true
---

# To PRD

Do not interview again.
Synthesize only `prd/concept.md`, files under `prd/adr/`, and decisions already made during prototyping.

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

Read [PRD-TEMPLATE.md](PRD-TEMPLATE.md) and [ARCHITECTURE-TEMPLATE.md](ARCHITECTURE-TEMPLATE.md).
Draft `prd/PRD.md` with Problem, Solution, numbered User Stories, Success Metrics, and Out of Scope.
Write user stories as `As an <actor>, I want <feature>, so that <benefit>`.
Do not add a required persona field.
Draft `prd/architecture.md` with the `app/` tree, modules and interfaces, data model, main flows, test seams, external dependencies, boundaries, and accepted ADR index.
Avoid concrete file paths and code snippets in the PRD unless a prototype snippet expresses an exact decision more clearly than prose.

Finalize every ADR without deleting any ADR file.
Renumber gaps continuously while preserving slugs and updating references.
Set frontmatter `Status:` to `accepted`, `superseded by ADR-NNNN`, or `deprecated`.
When a newer decision replaces an older one, mark the older ADR as superseded and state the replacement relation in the newer ADR.
Add an ADR for any qualifying prototype decision that was not recorded.

After drafting, offer a Lavish review.
If the user agrees, call the Skill tool with "lavish".
Open Lavish `plan` and `diagram` playbooks before writing the HTML artifact, poll for annotations, and apply accepted feedback back to the Markdown sources.
Treat Markdown under `prd/` as the source of truth and `.lavish/` as a disposable review surface.
If the user wants a presentation artifact, export it to `demos/<name>/`.
Update only the step 3 row and decision index in `prd/roadmap.md`.

## Next step

Recommend `/to-ticket` as the next command, with one sentence explaining why.
Ask using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now.
If yes, tell the user to run `/clear` and then `/to-ticket`.
If not now, stop without further action.
