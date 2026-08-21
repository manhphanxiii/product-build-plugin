---
name: idea-to-product-concept
description: Gather product evidence, interview the user once across all unresolved areas, and produce a traceable product concept.
---

# Idea to Product Concept

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
Treat existing files in `client-note/` as read-only.
With approval, add supplied customer material verbatim, but never rewrite existing customer language.
Read `app/knowledge-base/` freely, but never write there because it is runtime data owned by the application.
Do not write chain files outside these destinations.

## Gather material first

Before asking any other question, inspect `app/knowledge-base/` and `client-note/`, then ask exactly this opening question:

> What material can I analyze? Documents, slides, contracts, screenshots of the current product or competitors, screen recordings or user interviews, website links, data exports, spreadsheets, or anything else.

Analyze supplied material by type:

- Read text documents, PDFs, and slides directly, splitting long PDFs into page ranges.
- Inspect screenshots and images, then describe what is visible so the user can confirm the reading.
- Fetch website content.
  When several links are supplied and delegation is available and authorized, assign one sub-agent per link.
- Do not claim to watch video.
  Ask for a transcript, screenshots at important timestamps, or a five-bullet account from the user.
- For data and spreadsheets, summarize the schema and a few representative rows without dumping the full file into context.

When material is large and delegation is available and authorized, assign one sub-agent per material group.
Summarize what the material already answers and ask the user to confirm that summary before interviewing.
Do not ask again for facts the material already establishes.
Propose copying customer voice into `client-note/` verbatim only after asking.
Preserve complete objections, complaints, and the customer's own name for the problem instead of translating them into product-team language.
Industry and market knowledge belongs directly in the Problem and Constraints sections of `prd/concept.md`, with its source recorded in `## Nguồn`.
If `client-note/` is empty and the user has no material, say plainly that the repository is operating entirely on assumptions.

## Consolidate large material with Lavish

Use prose when the material remains easy to verify.
When several documents, links, long transcripts, or data exports make a prose summary hard to audit, offer a Lavish consolidation surface before building one.
If the user agrees, call the Skill tool with "build:lavish".
Open the `table` playbook before writing HTML, add `comparison` when sources conflict, and add `input` when the user needs to confirm or correct rows in the artifact.
Use the source table columns from [CONCEPT-TEMPLATE.md](CONCEPT-TEMPLATE.md) and add one column for what remains unclear.
Poll for feedback, apply it, and only then interview so the questions cover facts the material could not answer.
This surface consolidates evidence before the interview and does not replace the Review gate for the final concept.

## Do not invent the business

Record only facts the user or supplied evidence actually establishes.
Write every gap as `TODO - chưa xác nhận` instead of filling it with plausible language.
An invented buyer persona is worse than an empty field because nobody is prompted to verify it later.

## Interview once

Ask every remaining question in one numbered batch, then stop for answers.
Use this format for each question:

```text
❓ **Q1** - **<question title>**: <question and choices if useful>

➡️ <recommended answer>
```

Cover the problem, who experiences it, success measures, scope, out of scope, constraints, and the largest risks.
Cover surfaces and logic in the same batch, because `/build:prototype` cannot choose a prototyping method without those answers.
Offer operator, builder, and researcher as optional lenses for missing perspectives.
If the user says those lenses are irrelevant, drop them immediately and do not insist.
After the response, analyze the full set for contradictions, newly opened issues, and answers too vague to act on.
Ask a second round only for real gaps and explain which answer created each follow-up.
Investigate facts in the repository instead of asking the user, using sub-agents when available and authorized.
Reserve product decisions for the user.

## Surfaces and logic

Read [SURFACES-AND-LOGIC.md](SURFACES-AND-LOGIC.md) before writing these questions.
Ask one surface question for each of the three stakeholders: the person who uses the features, the developer who debugs and maintains the product, and the admin who manages and controls it.
Offer Web/App and Zero UI as the two surface types, accept `none` as a real answer, and accept both types on one stakeholder when that is the truth.
A Zero UI answer must name the host product, such as Zalo, Google Sheets, Slack, or email.

Ask one logic question for each main capability, offering all four levels: plain code, workflow, skill, and agent.
Say inside the question that the levels stack, so one product usually uses several at once.
When an answer is agent or skill, ask exactly one follow-up about which part of that capability could move down to plain code.
Ask separately what has to outlive a session, who owns it, and what already runs that the product must reuse.
Add one optional question about concrete technology and say in the question itself that "not decided yet" is a fine answer.

Record every unresolved technology or level as an open question in `## Risks and open decisions` for `/build:prototype` to settle with a spike.
Do not choose any of this for the user, and never let a recommended answer become a decision the user did not make.
Write an unanswered surface or level as `TODO - chưa xác nhận`, never as a default of Web/App and never as a default of plain code.

Build the review draft as the complete `prd/concept.md` defined by [CONCEPT-TEMPLATE.md](CONCEPT-TEMPLATE.md), together with the proposed step 2 roadmap row.

## Review gate

Run this gate after the last question of this skill is answered and before writing any file under `prd/`.
Build the full draft of every document this skill is about to write, show it on a review surface, and revise it until the user approves.
Never write the final file before that approval.

Choose the surface with this probe and state the chosen surface in one line before rendering.

1. Prefer Lavish.
   Lavish is usable when its CLI runs and a local browser can be opened: `npx -y lavish-axi --help` exits 0, and `command -v open` resolves on macOS or `command -v xdg-open` resolves on Linux.
   When `npx -y` exits opaquely, retry once with `node "$(npm root)/lavish-axi/dist/cli.mjs" --help` before declaring Lavish unusable.
2. When the probe fails, use the Artifact tool.
   Lavish serves the artifact from a local Express server, so a session whose browser is not on this machine, such as a cloud session, cannot see the page and its poll would wait forever.
   `.lavish/` is also gitignored, so a Lavish draft does not survive a cloud session at all.
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

## Write the concept

Read [CONCEPT-TEMPLATE.md](CONCEPT-TEMPLATE.md).
Create or update `prd/concept.md` only after the needed destination has been approved.
List every analyzed source and the questions it answered.
If the interview reveals durable domain knowledge, record it in the appropriate section of `prd/concept.md` and cite it in `## Nguồn`.
Update only the step 2 row in `prd/roadmap.md` and its evidence-backed next step.

## Next step

Recommend `/build:prototype` as the next command, with one sentence explaining why.
Ask using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now.
If yes, tell the user to run `/clear` and then `/build:prototype`.
If not now, stop without further action.
