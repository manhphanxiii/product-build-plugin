---
name: idea-to-product-concept
description: Gather product evidence, interview the user once across all unresolved areas, and produce a traceable product concept.
disable-model-invocation: true
---

# Idea to Product Concept

## Repository destinations

Resolve the repository root with `git rev-parse --show-toplevel`.
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
If the user agrees, call the Skill tool with "lavish".
Open the `table` playbook before writing HTML, add `comparison` when sources conflict, and add `input` when the user needs to confirm or correct rows in the artifact.
Use the source table columns from [CONCEPT-TEMPLATE.md](CONCEPT-TEMPLATE.md) and add one column for what remains unclear.
Poll for feedback, apply it, and only then interview so the questions cover facts the material could not answer.
Markdown under `prd/` remains the source of truth and `.lavish/` is a disposable review surface.

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
Offer operator, builder, and researcher as optional lenses for missing perspectives.
If the user says those lenses are irrelevant, drop them immediately and do not insist.
After the response, analyze the full set for contradictions, newly opened issues, and answers too vague to act on.
Ask a second round only for real gaps and explain which answer created each follow-up.
Investigate facts in the repository instead of asking the user, using sub-agents when available and authorized.
Reserve product decisions for the user.

## Write the concept

Read [CONCEPT-TEMPLATE.md](CONCEPT-TEMPLATE.md).
Create or update `prd/concept.md` only after the needed destination has been approved.
List every analyzed source and the questions it answered.
If the interview reveals durable domain knowledge, record it in the appropriate section of `prd/concept.md` and cite it in `## Nguồn`.
Update only the step 1 row in `prd/roadmap.md` and its evidence-backed next step.

## Next step

Recommend `/prototype` as the next command, with one sentence explaining why.
Ask using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>` whether to continue now.
If yes, tell the user to run `/clear` and then `/prototype`.
If not now, stop without further action.
