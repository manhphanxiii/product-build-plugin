---
name: evals-gate
description: Derive and run a permanent product eval set, enforce a measurable ship gate, and block shipping on failures or regressions.
---

# Evals Gate

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

Read `prd/PRD.md` and [EVAL-FORMAT.md](EVAL-FORMAT.md).
Turn every relevant user story into stable eval cases in `prd/evals/cases.md`.
Each case must have a stable `id`, `input`, `must`, `must_not`, `source`, and `added` date.
State the numeric ship gate at the top of the file.
Default to pass rate at least 90 percent, zero critical failures, and zero pass-to-fail regressions unless the product has an approved stricter gate.

Run the entire eval set against the current product behavior.
Append every run, including failures, to `prd/evals/results.md`.
When the gate fails, explicitly refuse to ship.
Diagnose failed cases before changing implementation.
After a fix, rerun the complete set, not only failed cases.
Before shipping a fix for any real-world bug, add a permanent regression case that reproduces it.
Update only the step 6 row and related blocker entries in `prd/roadmap.md`.

## Next step

Only when the gate passes, recommend `/update` as the next command, with one sentence explaining why.
Ask using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now.
If yes, tell the user to run `/clear` and then `/update`.
If not now, stop without further action.
While the gate is failing, do not offer a next command; stay focused on fixing the failures.
