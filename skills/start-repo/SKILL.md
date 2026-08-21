---
name: start-repo
description: Initialize a product repository once with canonical instructions, quality gates, workspace structure, and the first product-building roadmap.
disable-model-invocation: true
---

# Start Repo

This is the one-time initialization command for a product repository.
After initialization, use `/build:update` to refresh progress and choose the next command.

## Ground rules

Resolve `<root>` in phase 1 before using it in any later phase.
A repository whose root contains both `.claude-plugin/plugin.json` and `skills/start-repo/SKILL.md` is the skill-set repository and is never a valid `<root>`; refuse such a path and ask again.
Every path in this skill without an explicit prefix is relative to `<root>`, never to the current working directory.
Run repository commands with `<root>` as the working directory and every Git command as `git -C <root> ...`.
Write chain documents only under `<root>/prd/`, production code only under `<root>/app/`, and prototypes only under `<root>/demos/prototypes/`.
Root governance files `AGENTS.md` and `CLAUDE.md` may be written only by `/build:start-repo`, after approval. The ship checklist at `prd/evals/checklist.md` is also seeded only by `/build:start-repo`, after approval.
Treat `client-note/` as read-only.
Read `app/knowledge-base/` freely, but never write there because it is runtime data owned by the application.
In the separate-folder branch of `restructure`, never create, edit, or delete anything inside the existing application repository, including `knowledge-base`.
Do not write chain files outside these destinations and approved root governance files.
Never propose creating a new product repository or a new separate folder before inspecting the repository the user named in phase 2. When that existing repository already satisfies most of the canonical roles in [REPO-LAYOUT.md](REPO-LAYOUT.md), propose keeping it in place and filling only what is missing.

Keep one canonical source for each fact and follow [PRINCIPLES.md](PRINCIPLES.md); reduce other agent instruction files to thin pointers plus genuinely tool-specific instructions.

Do not interview about the product, buyer, promise, or scope.
Those decisions belong to `/build:idea-to-product-concept`.
Record unknown setup facts as explicit TODOs and never invent project commands.

## Phase 1: language, timezone, and the product repository

Before anything else, ask exactly one question using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>`.
Combine two things in this single question: conversation and content language, and working timezone.
For language, offer Vietnamese for both, English for both, or a different language for each.
For timezone, read the machine's current offset and name (`date +%Z` and `date +%z`) and suggest it as part of the recommended answer, using its IANA name, for example `➡️ Tiếng Việt cho cả hai, Asia/Ho_Chi_Minh (UTC+7)`.
That answer sets the language of the conversation for the rest of the chain, the language of generated repository file content, and the working timezone recorded later in `AGENTS.md`.
Only when the user picks a different language for each, ask one follow-up naming which language applies to which.
Use the chosen conversation language from the next message onward, including every question below.

Then ask `❓ **Q2** - **Product repository**`, always, regardless of what the product repository turns out to be.
Accept any of three answers:

1. A local path.
2. A Git link (a GitHub URL). Use `gh repo view <url>` read-only to confirm the repository exists and to read its default branch and description; when `gh` is unavailable, ask the user for the default branch. Do not clone yet; recognizing this case is the only requirement of this question, the actual clone proposal happens in phase 4.
3. Nothing yet, no product repository exists at all.

Do not ask `new` versus `restructure` here. The mode is a conclusion of phase 2, not an opening question.
When the answer to Q2 is "nothing yet," skip phase 2 entirely, treat the mode as `new`, and let phase 3 ask only for the new repository's path.

## Phase 2: inspect the product repository (read-only)

Run only when Q2 named an existing local path or Git link.
Run the checks grouped under "Phase 2 checks" in [REPO-CHECKS.md](REPO-CHECKS.md) against the repository Q2 named.
Read-only: create no directories, run no `git init`, and do not clone a Git link here.
For a Git link not yet cloned, inspect as much as `gh` exposes and mark the rest "unknown until cloned"; state plainly that any placement proposal is provisional until the clone happens.

Reach these conclusions before phase 3:

- Whether `prd/roadmap.md` already exists. If it does, the repository is already initialized; follow the report-only behavior phase 4 already describes for that case.
- How many canonical roles from [REPO-LAYOUT.md](REPO-LAYOUT.md) already exist, and which real folder matches which role.
- Whether the repository is a Git repository, and what its real production code path is (`src/`, `apps/web/`, etc).
- Whether the repository already holds product documentation (`docs/product/`, `prd/`, etc).

## Phase 3: propose where the product repository belongs, then ask

Print exactly one short table of what phase 2 found, and a proposed `<root>` placement with its reason.
Then ask `❓ **Q3** - **Product repository location**` with exactly one recommended answer marked `➡️`, offering three choices:

| Choice | `<root>` | Recommended when |
|---|---|---|
| Keep it in place (`restructure`, in-place branch) | the existing repository itself | it already satisfies most canonical roles, or it is already the product's real home. This is the default whenever the existing repository is already close to correct |
| A separate folder beside it (`restructure`, separate-folder branch) | a new folder next to the existing application repository | the existing repository is a plain, shared, or otherwise unsuitable home for product documents |
| A new repository (`new`) | the path the user supplies | no product code exists yet |

Resolve and print the resulting `<root>` after Q3 is answered.
Do not create the directory or initialize Git until the phase 4 proposal is approved.

## Phase 4: inspect

Reuse the findings from phase 2 instead of re-scanning `<root>` from scratch; read [REPO-CHECKS.md](REPO-CHECKS.md) and [REPO-LAYOUT.md](REPO-LAYOUT.md) and run only the checks grouped under "Phase 4 checks" there, plus a clone proposal row when Q2 named a Git link not yet cloned.
State the selected mode and whether an existing `<root>` is already initialized before any change.
Present exactly one table with `Item`, `Status`, and `Proposal` columns.
Do not create files, initialize Git, authenticate services, or create directories before approval.

If `prd/roadmap.md` already exists, report what exists and what is missing.
Propose only the missing files, never modify `prd/roadmap.md`, skip phase 7 except for questions required to fill a missing file, and finish by directing the user to `/build:update`.

If a root-level `REVIEW.md` exists, that is the old layout. Propose migrating its content to `prd/evals/checklist.md` and deleting the root file, as one row in the phase 4 table, and wait for approval. Never overwrite `prd/evals/checklist.md` if it already exists.

## Phase 5: propose the role mapping

Run this phase only when Q3 chose a `restructure` option.
Scan the existing code read-only, compare real folders with the roles in [REPO-LAYOUT.md](REPO-LAYOUT.md), and print exactly one mapping table:

| Canonical role | Proposal | Existing source | Reason |
|---|---|---|---|
| `app/` | symlink | `../my-running-app/` | that repository is the production application |
| `prd/` | symlink | `docs/product/` | existing product documents live here |
| `client-note/` | create | - | no folder matching customer voice was found |

Propose a symlink only when an existing folder genuinely matches the role.
Otherwise propose creating the canonical folder.
Never propose symlinks for `routines/` or `report/`; those belong to the product repository.

For the in-place branch, do not symlink `app/`.
Detect the real production code path such as `src/` or `apps/web/`, record it as `app-dir` in the `AGENTS.md` mapping, and scaffold with `--retrofit`.
For the separate-folder branch, propose `app/` as a symlink to the existing application repository.

Explain that writing through a symlink writes directly to its real target and that those changes belong to the Git history of the repository containing that target, not the product repository.
Wait for approval of every row before running the scaffold.
Do not reorganize or edit anything inside the existing application repository.

## Phase 6: scaffold and fill canonical files

After approval, run the mode-appropriate scaffold command and relay its created, skipped, and symlink lists verbatim.
The scaffold script ships with this skill, so always address it through `${CLAUDE_PLUGIN_ROOT}` and never through a path relative to the current working directory, which is `<root>` and not the skill folder.
Use `python3 "${CLAUDE_PLUGIN_ROOT}/skills/start-repo/scripts/scaffold.py" <root> --init-git` for `new`.
For the separate-folder branch of `restructure`, keep the same `python3 "${CLAUDE_PLUGIN_ROOT}/skills/start-repo/scripts/scaffold.py" <root>` prefix and add `--init-git --no-knowledge-base` and every approved `--link ROLE=PATH` mapping.
For the in-place branch, keep that same prefix and use `--retrofit` and every approved non-app `--link ROLE=PATH` mapping.

The scaffold never creates or edits `.gitignore`.
After symlinks are created, separately propose adding each symlink name to `.gitignore`, then apply only entries the user approves.
The scaffold seeds `.claude/settings.json` with the plugin marketplace declaration required by other sessions; follow the merge and preservation rules in [REPO-LAYOUT.md](REPO-LAYOUT.md).
Fill `AGENTS.md` first, then `CLAUDE.md`, `prd/evals/checklist.md`, `prd/README.md`, and `prd/roadmap.md` from the templates in [assets](assets/).
In `AGENTS.md`, record the approved canonical-role mapping and whether each role is a symlink or a real directory.
In `new` mode, record that every role is a real directory in this repository.
Fill both Conventions lines in `AGENTS.md` from phase 1: the conversation language and the working timezone chosen in Q1. Every later chain skill reads both from these lines, so neither may be left as a template placeholder.
Write a conservative permission posture into `AGENTS.md` and state how it may loosen after the review system proves reliable.
Populate commands only with values verified by the Phase 2 checks in [REPO-CHECKS.md](REPO-CHECKS.md).
Leave every unverified command as `TODO`; do not ask and do not guess.
A missing command is safer than a plausible but incorrect command.
Leave product-specific quality criteria as the self-describing TODOs owned by `/build:to-prd` in the checklist template.
Always install both `weekly-ops-review.md` and `pr-auto-review.md` in `routines/`.
When the scaffold skips a seeded file because its canonical role is a symlink, create it from the matching template only for an in-place link whose target is inside `<root>`; in the separate-folder branch, do not fill or seed anything through the link.
If `.cursorrules`, `GEMINI.md`, or another agent configuration duplicates canonical instructions, propose reducing it to a thin pointer.
Fill the templates in the file content language chosen in phase 1, translating any template written in another language.

## Phase 7: initialize the chain and hand off

Explain step 1 (start-repo, just completed) and steps 2 through 7 for someone new to the workflow.
For every step, state the question it answers, the decision the user must make, its artifact and location, an honest time estimate, and evidence of completion.
Recommend one context window per step, `/clear` between steps, and `/clear` between implementation tickets.

Read [ROADMAP-FORMAT.md](ROADMAP-FORMAT.md) and fill the roadmap the scaffold seeded.
Mark step 1 (start-repo) completed with today's date and its artifacts (`AGENTS.md`, `CLAUDE.md`, `prd/evals/checklist.md`); leave the routine part of the note line as not yet installed until phase 8 resolves Q4/Q5.
Set steps 2 through 7 to not started.
Set the weekly goal to completing `prd/concept.md`.
Leave Out of scope empty with a note that `/build:update` will fill it from `prd/concept.md`.
Do not infer progress or add tasks for steps 2 through 7.

## Phase 8: offer the morning brief routine

Ask `❓ **Q4** - **Morning brief**` whether to run `/build:update` as a daily morning brief and at what time, recommending `➡️ Có, 08:00` and stating that time is in the working timezone recorded in `AGENTS.md` during phase 6.
When the answer is no, skip the rest of this phase, create no file, and note that routine mode in `/build:update` can enable this later.

When the answer is yes, write `routines/update-roadmap.md` from the [morning brief template](assets/routines/update-roadmap.md) with the chosen time and the `AGENTS.md` timezone filled in.
Then present exactly one table of activation mechanisms and their tradeoffs, the same style as the table in `skills/update/ROUTINE-SETUP.md`, and show the exact content that will be written or run before asking.
Ask `❓ **Q5** - **Activation**` which mechanism to use and whether to activate now, recommending `/schedule`, the mechanism that actually fires on a wall-clock schedule; it requires `<root>` to be on GitHub and Claude Code routines enabled on the account.
A Stop hook in `.claude/settings.json` does not fire on a schedule and only runs for sessions opened in `<root>`, cloud or local; offer it only as an alternative for a session-based brief instead of a time-based one, and when chosen show the exact merged JSON patch and preserve existing settings.
Wait for approval separate from the phase 4 approval before writing `.claude/settings.json` or creating a `/schedule` routine.
When the user declines activation, keep the routine definition file, state plainly that nothing runs it yet, and give the command to enable it later.
After activation, run the routine once so its first dated report at `report/product/roadmap-<YYYY-MM-DD>.md` exists.

Whatever Q4/Q5 resolved to, update the note line under the Tiến độ table in `prd/roadmap.md` with the final routine status: installed with its time, or not installed. This is the one direct edit `/build:start-repo` makes to `prd/roadmap.md` after phase 7, and it is allowed because `/build:start-repo` owns step 1's row and note line exclusively.

Tell the user to use `/build:update`, not `/build:start-repo`, to refresh roadmap progress and choose future commands.

Recommend `/build:idea-to-product-concept` as the next command with one sentence explaining why.
Ask using `❓ **Q6** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now.
If yes, tell the user to run `/clear` and then `/build:idea-to-product-concept`.
If not now, stop without further action.
Do not start product code in the same turn.

## Repository operating rules to preserve

When the user challenges the workspace structure, read [PRINCIPLES.md](PRINCIPLES.md) and explain the relevant reason.
