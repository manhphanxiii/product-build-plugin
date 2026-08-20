---
name: evals-gate
description: Derive and run a permanent product eval set, enforce a measurable ship gate, and block shipping on failures or regressions.
disable-model-invocation: true
---

# Evals Gate

## Repository destinations

Resolve the repository root with `git rev-parse --show-toplevel`.
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
