# Prototype modes

`prd/concept.md` records a surface for each stakeholder and a logic level for each capability in `## Surfaces and logic`.
Each of those has a cheapest honest spike, and using the wrong one produces a demo that proves nothing.

| What needs a spike | Cheapest honest spike | What it proves | What it cannot prove |
|---|---|---|---|
| Web/App | one route with variants selected by a URL search parameter, pinned to a real device viewport when the target is an installed app | layout, flow, information density, the one risky interaction | device capability, real data volume, permissions, latency |
| Web/App needing a device capability | a single screen in the real toolchain, running on a real device or emulator | camera, offline, push, background work, biometrics, store review rules | everything else about the product |
| Zero UI | a scripted transcript played inside the real host product | wording, turn order, whether the stakeholder understands what to do | host platform limits, quotas, approval rules |
| Any logic level, required first step | draw the flow before writing code | the steps, the provider at each step, the input and output of each step, the branching conditions | anything that only appears when it runs |
| Logic, plain code | one runnable file driven by the hard cases, with assertions | the algorithm, the failure modes, the shape of the data | production load, real integration behaviour |
| Logic, workflow | run the approved graph on fixtures and force every LLM node to return garbage once | node boundaries, the failure path, where a human must approve | long term stability of the LLM nodes |
| Logic, skill | the prompt itself plus a small fixed input set, run repeatedly on the same input | variance, disagreement rate, whether the prompt is clear enough | behaviour on inputs never seen before |
| Logic, agent | a trajectory transcript on the hardest inputs, with a loop cap, a tool call cap, and a cost cap | whether the model picks the right tool and knows when to stop | cost and latency at real scale |
| Data model | a seeded throwaway store plus the three hardest reads and writes | identity, uniqueness, the query that will hurt | migration cost at real volume |

## Web/App

Keep the spike on one route, select variants with a URL search parameter, and print the variant name on screen.
Use fixture data that lives inside the spike directory, and never connect the spike to a real database.
Skip auth, build steps, and routing frameworks unless auth, build, or routing is itself the open question.

When the target is an app installed on a device, start in the browser at a real device width with real touch target sizes, and write in the spike README which questions that spike cannot answer.
Build a runnable app in the real toolchain only when the open question is a device capability, and keep it to one screen that touches only the capability in question.
Ask which devices and OS versions actually matter before choosing a toolchain, because that constraint decides the toolchain more often than the feature list does.
Toolchain choice is hard to reverse, so it needs an ADR.

## Zero UI

The prototype is the transcript or the document itself, not a screen.
The first spike is Wizard of Oz: a person plays the product inside a real conversation or a real sheet, with no code, so the surface is exactly the one the stakeholder will meet.
The second spike is one runnable file that prints the full transcript for the hard cases: ambiguous input, wrong format, empty state, a repeated request, and the moment the product has to say no.

Build a real bot, webhook, or add-on in a sandbox workspace only when the open question belongs to the host platform: message template approval, rate limits, permission scopes, delivery latency, or what the host will not allow at all.
Ask what the host platform forbids before designing the interaction, because that finding kills more Zero UI designs than any other.
Record how the stakeholder discovers and triggers the product, since Zero UI has no home screen and no navigation.

## Draw the flow before writing code

This step is required before the first line of spike code at every logic level, from plain code to agent.
For a logic heavy product the flow diagram is the design, standing exactly where a UI mockup stands for a screen product, not decorating it afterwards.

The diagram must carry four things: the steps, the provider at each step, the input and output of each step, and the branching conditions.
Ask whether to open a Lavish surface for it and recommend yes, then call the Skill tool with "lavish" and open the `diagram` playbook with editable Mermaid.
If the user declines Lavish, still draw it, and accept raw Mermaid in the conversation, a draw.io export, or a photo of paper, but never skip the step.
Poll for feedback, apply it back to the Mermaid source, and write the spike only after the flow is approved.
The approved diagram belongs in the `## Context` of the ADR, because it is what explains why the spike was written this way.

## Logic, plain code

One runnable file, the hard cases, and assertions on the expected output.
This level is fully determined, so the spike either passes or fails and does not need repeated runs.
For an external system, spike against the real sandbox with real credentials and record the auth model, rate limits, latency, and error shape.
Never point a spike at production data or production credentials.

## Logic, workflow

The approved diagram is already the first spike, because most workflow disagreements are disagreements about node boundaries rather than about code.
Once the graph is approved, run it on fixture inputs across the hard cases.
Force every LLM node to return garbage once, since that failure path is where a workflow actually differs from plain code.
Record which nodes need a human approval and which are allowed to run unattended.

## Logic, skill

The prototype is the prompt plus a small, hard, fixed input set.
Run the same input several times and record the variance, because this level is semi determined and one good run proves nothing.
Record the disagreement rate in the ADR, and keep that input set so `/build:evals-gate` can reuse it as eval cases.

## Logic, agent

The prototype is the agent's own trajectory transcript on the hardest inputs, not its final answer.
Put a loop cap, a tool call cap, and a cost cap inside the spike, and treat hitting a cap as a finding rather than a bug to patch.
What must be proven is whether the model picks the right tool and knows when to stop, not whether it produced one nice answer.
Before settling on the agent level, try one level down and say where that level breaks; if nobody can point at the break, the agent level has not been shown to be necessary.

## Data model

Seed a throwaway store and run the three hardest reads and writes.
Record entity identity, uniqueness constraints, and the query that will hurt at real volume.

## Two closing rules

One spike answers one question.
When a spike would need a second surface to be believable, that is a second spike, not a bigger one.

The four logic levels stack, so spike at the lowest level that still answers the question, and climb only when a spike has shown the lower level breaks.
A good system is usually an agent that coordinates, calls a skill, and the skill calls determined code.
