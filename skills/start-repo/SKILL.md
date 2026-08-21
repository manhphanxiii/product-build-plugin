---
name: start-repo
description: Use only when the user explicitly invokes this one-time initializer for a product repository; create canonical instructions, quality gates, workspace structure, and the first product-building roadmap.
---

# Start Repo

Run this one-time initializer only when the user explicitly invokes the active host selector for `start-repo`.
If the skill was selected implicitly, stop before reading or writing repository state and tell the user to invoke `/build:start-repo`, `$build:start-repo`, or `$start-repo` for the installed host.

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

This is the one-time initialization command for a product repository.
After initialization, use `/build:update` to refresh progress and choose the next command.

## Ground rules

Resolve `<root>` in phase 1 before using it in any later phase.
A repository whose root contains `skills/start-repo/SKILL.md` and either `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json` is the skill-set repository and is never a valid `<root>`; refuse such a path and ask again.
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

Before phase 1, follow the plan-mode entry behavior defined in `## Plan gate`.

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
Do not create the directory or initialize Git until the plan is approved.

## Phase 4: inspect

Reuse the findings from phase 2 instead of re-scanning `<root>` from scratch; read [REPO-CHECKS.md](REPO-CHECKS.md) and [REPO-LAYOUT.md](REPO-LAYOUT.md) and run only the checks grouped under "Phase 4 checks" there, plus a clone proposal row when Q2 named a Git link not yet cloned.
State the selected mode and whether an existing `<root>` is already initialized before any change.
Present exactly one table with `Item`, `Status`, and `Proposal` columns.
Treat every row as input to the plan, not as a separate approval request.
Do not create files, initialize Git, authenticate services, or create directories before plan approval.
When the phase 4 checks conclude that scaffold will initialize Git and `<root>` will have no `origin`, include exactly one `Remote GitHub` row in that table.
The row must print the concrete owner, repository name, visibility, initial commit message, and exact repository creation command or tool action that will run.
The plan must group repository creation, the initial commit, and the first push together.
The user may change the owner, repository name, visibility, or initial commit message while reviewing the plan.

If `prd/roadmap.md` already exists, report what exists and what is missing.
Propose only the missing files, never modify `prd/roadmap.md`, skip phase 8 except for questions required to fill a missing file, and finish by directing the user to `/build:update`.

If a root-level `REVIEW.md` exists, that is the old layout.
Propose migrating its content to `prd/evals/checklist.md` and deleting the root file as one row in the phase 4 table.
Never overwrite `prd/evals/checklist.md` if it already exists.

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
Treat every row as input to the plan and do not run the scaffold before plan approval.
Do not reorganize or edit anything inside the existing application repository.

## Phase 6: decide the morning brief

Ask `❓ **Q4** - **Morning brief**` whether to run `/build:update` as a daily morning brief and at what time, recommending `➡️ Có, 08:00` and stating that time is in the working timezone selected in phase 1.
When the answer is no, record that no routine file or activation will be created, skip Q5, and continue to the plan gate.

When the answer is yes, present exactly one table of activation mechanisms and their tradeoffs in the same style as the table in [../update/ROUTINE-SETUP.md](../update/ROUTINE-SETUP.md).
Ask `❓ **Q5** - **Activation**` which available mechanism to use and whether to activate it, but do not write or activate anything yet.
On Claude Code when `/schedule` is available, recommend it because it fires on a wall-clock schedule; it requires `<root>` to be on GitHub and Claude Code routines enabled on the account.
A Stop hook in `.claude/settings.json` does not fire on a schedule and only runs for sessions opened in `<root>`, cloud or local; offer it only as an alternative for a session-based brief instead of a time-based one.
Offer `/schedule`, `/loop`, and the Stop hook only when the current host exposes that mechanism.
On Codex, when no native mechanism capable of running this routine is available, offer an unactivated routine definition with manual `$build:update`, or an external scheduler that runs `codex exec` from `<root>`.
Use the `Remote GitHub` decision from phase 4 when describing whether `/schedule` is viable.
Record the selected routine file content and the exact activation definition or merged JSON patch as inputs to the plan.

## Plan gate

At the start of the run, before phase 1, enter plan mode when the host exposes it and plan mode is not already active, then state that transition in one line.
When the user already enabled plan mode, respect it and do not enter it again.
When the host has no plan mode, enforce the same discipline in this skill: run no approval-gated write before the plan is approved.

After phases 1 through 6, build one complete action plan from every inspection result and answer.
The plan must include:

- the resolved `<root>` and selected mode: `new`, `restructure` in place, or `restructure` in a separate folder;
- every row from the phase 4 table, including the `Remote GitHub` owner, repository name, visibility, initial commit message, and exact repository creation command or tool action;
- every row from the phase 5 role-mapping table when that phase runs;
- the exact scaffold command with every applicable `--init-git`, `--retrofit`, `--no-knowledge-base`, and `--link ROLE=PATH` flag;
- every file that will be created and filled from `assets/`;
- every proposed `.gitignore` entry for a symlink;
- the complete phase 9 GitHub publication command sequence; and
- the routine file and selected activation mechanism, including the exact merged JSON patch or `/schedule` definition, or an explicit statement that no routine or activation will be created.

Choose the surface with this probe and state the chosen surface in one line before rendering.

1. Prefer Lavish.
   Lavish is usable when its CLI runs, any required package is already installed or network access is available, and a local browser can be opened: `npx -y lavish-axi --help` exits 0, and `command -v open` resolves on macOS or `command -v xdg-open` resolves on Linux.
   When `npx -y` exits opaquely, retry once with `lavish-axi --help`; if that binary is unavailable, run `npm root -g`, then run `node <global-node-modules>/lavish-axi/dist/cli.mjs --help` using the printed path before declaring Lavish unusable.
2. When the probe fails and both the Artifact tool and `artifact-design` skill are available, use the Artifact tool.
   Lavish serves the artifact from a local Express server, so a session whose browser is not on this machine, such as a cloud session, cannot see the page and its poll would wait forever.
   Lavish drafts are temporary and do not survive a cloud session.
3. When neither surface is available, print the plan in the conversation as Markdown and collect approval there.
   A user-started asynchronous cloud run is interactive across turns: print the Markdown plan, stop before writing any approval-gated file, and wait for explicit approval in a follow-up.

If plan mode blocks Lavish from rendering, state the surface substitution in one line and continue down the same fallback order.
With Lavish, invoke `lavish` through the active host mapping in `## Host resolution`, open the `plan` playbook and the `input` playbook, then poll for feedback.
With the Artifact tool, load the `artifact-design` skill first, publish the plan from a session scratchpad file, and collect feedback in this conversation.
Apply every requested edit to the plan and present it again until the user approves or ends the session.
The user may edit any row in the approval response, and every such edit becomes part of the approved plan before execution.

When the host exposes `ExitPlanMode`, submit the approved plan through it.
After approval, run phases 7 through 10 in order without another approval request.
The secret scan stop in phase 9 remains a safety check, and Q6 in phase 10 remains the final handoff question.
For an already initialized repository, include only missing files in the plan; when nothing is missing, execute nothing and direct the user to `/build:update`.

## Phase 7: scaffold and fill canonical files

After plan approval, run the mode-appropriate scaffold command and relay its created, skipped, and symlink lists verbatim.
The scaffold script ships with this skill, so always address it as `<skill_dir>/scripts/scaffold.py` and never through a path relative to the current working directory, which is `<root>` and not the skill folder.
Use `python3 "<skill_dir>/scripts/scaffold.py" <root> --init-git` for `new`.
For the separate-folder branch of `restructure`, keep the same `python3 "<skill_dir>/scripts/scaffold.py" <root>` prefix and add `--init-git --no-knowledge-base` and every approved `--link ROLE=PATH` mapping.
For the in-place branch, keep that same prefix and use `--retrofit` and every approved non-app `--link ROLE=PATH` mapping.

The scaffold never creates or edits `.gitignore`.
After symlinks are created, add the `.gitignore` entries included in the approved plan.
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

## Phase 8: initialize the chain

Explain step 1 (start-repo, just completed) and steps 2 through 7 for someone new to the workflow.
For every step, state the question it answers, the decision the user must make, its artifact and location, an honest time estimate, and evidence of completion.
Recommend one context window per step, `/clear` between steps, and `/clear` between implementation tickets.

Read [ROADMAP-FORMAT.md](ROADMAP-FORMAT.md) and fill the roadmap the scaffold seeded.
Mark step 1 (start-repo) completed with today's date and its artifacts (`AGENTS.md`, `CLAUDE.md`, `prd/evals/checklist.md`); leave the routine part of the note line as not yet installed until phase 10 applies the phase 6 decision.
Set steps 2 through 7 to not started.
Set the weekly goal to completing `prd/concept.md`.
Leave Out of scope empty with a note that `/build:update` will fill it from `prd/concept.md`.
Do not infer progress or add tasks for steps 2 through 7.

## Phase 9: publish <root> to GitHub

Run this phase only when the approved plan contains a `Remote GitHub` row.
Recheck `git -C <root> remote get-url origin` before any write; when `origin` exists, print one line with its URL and skip the rest of this phase.

Before staging anything, run `git -C <root> status --short` and print the exact file list that would be included in the initial commit.
If any listed path looks like a secret, including `.env`, `.env.*`, `*.pem`, `*.key`, or a private key, stop and ask the user what to do without staging or committing anything.

When authenticated `gh` is available, run the approved values through this sequence:

```bash
git -C <root> add -A
git -C <root> commit -m "<initial commit message>"
git -C <root> branch -M main
gh repo create <owner>/<name> --private --source <root> --push
```

Use the visibility flag approved in the plan in place of `--private` when the user changed the default.

Apply these fallbacks in order and report the substitution in one line, following Host resolution:

1. When `gh` exists but is not authenticated, do not run `gh auth login` because its OAuth flow may not finish in one cloud turn; continue to the next available fallback.
2. When a GitHub connector or built-in GitHub tool is available, create the approved repository with that tool, then run `git -C <root> remote add origin <url>` and `git -C <root> push -u origin main` after the same status review, staging, commit, and branch normalization above.
3. When repository creation or push fails because the sandbox token lacks the required scope, handle it like the no-tool fallback below and do not claim publication succeeded.
4. When no publication mechanism is available, keep the repository local, print the exact commands the user must run, state plainly that an ephemeral cloud workspace will not survive the session, and do not leave a partially configured remote.

After publication succeeds, replace `{{GITHUB_STATUS}}` and `{{GITHUB_ROOT}}` in `prd/README.md` with the published status and the created remote URL.
Commit and push that canonical source update before continuing so it also survives an ephemeral cloud session:

```bash
git -C <root> add prd/README.md
git -C <root> commit -m "Record GitHub source"
git -C <root> push
```

Verify the result with `git -C <root> remote -v` and `git -C <root> log --oneline -1` before continuing.

## Phase 10: install the morning brief and hand off

Apply the morning brief and activation decisions approved in the plan.
When Q4 was no, create no routine file or activation and note that routine mode in `/build:update` can enable this later.
When Q4 was yes, write `routines/update-roadmap.md` from the [morning brief template](assets/routines/update-roadmap.md) with the chosen time and the `AGENTS.md` timezone filled in.
When activation was approved, apply the exact mechanism from the plan while preserving existing settings.
When the user declined activation, keep the routine definition file, state plainly that nothing runs it yet, and give the command to enable it later.
After activation, run the routine once so its first dated report at `report/product/roadmap-<YYYY-MM-DD>.md` exists.

Whatever Q4/Q5 resolved to, update the note line under the Tiến độ table in `prd/roadmap.md` with the final routine status: installed with its time, or not installed.
This is the one direct edit `/build:start-repo` makes to `prd/roadmap.md` after phase 8, and it is allowed because `/build:start-repo` owns step 1's row and note line exclusively.

Tell the user to use `/build:update`, not `/build:start-repo`, to refresh roadmap progress and choose future commands.

Recommend `/build:idea-to-product-concept` as the next command with one sentence explaining why.
Ask using `❓ **Q6** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now.
If yes, tell the user to run `/clear` and then `/build:idea-to-product-concept`.
If not now, stop without further action.
Do not start product code in the same turn.

## Repository operating rules to preserve

When the user challenges the workspace structure, read [PRINCIPLES.md](PRINCIPLES.md) and explain the relevant reason.
