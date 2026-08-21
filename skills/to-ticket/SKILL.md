---
name: to-ticket
description: Split an approved PRD and architecture into dependency-ordered vertical-slice tickets sized for one context window.
---

# To Ticket

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

Write chain documents only under `<root>/prd/`, production code only under `<root>/app/`, and prototypes only under `<root>/demos/prototypes/`.
If a destination is missing, propose its exact path and wait for approval before creating it.
Treat `client-note/` as read-only.
Read `app/knowledge-base/` freely, but never write there because it is runtime data owned by the application.
Do not write chain files outside these destinations.

Read `prd/PRD.md`, `prd/architecture.md`, and all ADRs under `prd/adr/`.
Split work into thin vertical slices that cross the required schema, API, UI, and test layers, can be demonstrated independently, and fit one context window.
Order tickets by dependency.

Build the review draft as the complete ticket set with each ticket's size, dependency edges, vertical-slice boundary, and independently deliverable outcome, together with the proposed step 5 roadmap row.

## Review gate

Run this gate after the last question of this skill is answered and before writing every document this skill is about to write.
Build the full draft of every document this skill is about to write, show it on a review surface, and revise it until the user approves.
Never write the final file before that approval.

Choose the surface with this probe and state the chosen surface in one line before rendering.

1. Prefer Lavish.
   Lavish is usable when its CLI runs, any required package is already installed or network access is available, and a local browser can be opened: `npx -y lavish-axi --help` exits 0, and `command -v open` resolves on macOS or `command -v xdg-open` resolves on Linux.
   When `npx -y` exits opaquely, retry once with `node "$(npm root)/lavish-axi/dist/cli.mjs" --help` before declaring Lavish unusable.
2. When the probe fails and both the Artifact tool and `artifact-design` skill are available, use the Artifact tool.
   Lavish serves the artifact from a local Express server, so a session whose browser is not on this machine, such as a cloud session, cannot see the page and its poll would wait forever.
   Lavish drafts are temporary and do not survive a cloud session.
3. When neither surface is available, print the draft in the conversation as Markdown and collect approval there.
   A user-started asynchronous cloud run is interactive across turns: print the Markdown draft, stop before writing any approval-gated file, and wait for explicit approval in a follow-up.

With Lavish, invoke `lavish` through the active host mapping in `## Host resolution`.
Open every playbook that matches the draft, and always open `input`, because this gate collects a decision.
Poll for feedback, apply every returned prompt, and poll again until the user approves or ends the session.
State the artifact path in one line, and add that the user may reply `artifact` to switch surfaces if the page does not open for them.

With the Artifact tool, load the `artifact-design` skill first, write the draft to a file in the session scratchpad, publish it, and give the user the link.
The user approves or gives feedback in this conversation.
Read comment threads with the Artifact tool's `comments` action when the user says they commented on the page.
Republish the same file path after each revision so the link stays stable.

`prd/` stays the source of truth, and both `.lavish/` and the published artifact are disposable review surfaces.
Skip this gate only for genuinely unattended automation with no user available to approve a draft; a user-started asynchronous cloud run does not qualify.

Read [TICKET-TEMPLATE.md](TICKET-TEMPLATE.md).
Write one approved ticket per file at `prd/tickets/NN-<slug>.md`, starting at `01`.
Set `Status: ready` unless repository evidence requires another state.
Declare `Blocked by` explicitly, using `none` where appropriate.
Add one row per ticket to the roadmap Task table with the ticket path in `Nguồn`.
Update only the step 5 row and the inserted task rows in `prd/roadmap.md`.

## Next step

Recommend `/build:implement` as the next command, with one sentence explaining why.
Ask using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now.
If yes, tell the user to run `/clear` and then `/build:implement`.
If not now, stop without further action.
