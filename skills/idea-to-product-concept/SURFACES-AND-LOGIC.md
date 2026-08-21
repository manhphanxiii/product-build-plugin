# Surfaces and logic

This reference exists so the interview asks where the product lives and how determined it must be.
Without these answers `/build:prototype` cannot choose a prototyping method, and `/build:to-prd` is forbidden to ask again.

## Three stakeholders

Ask about all three, every time.
`none` is a real answer and is recorded as `none`, which is different from an unanswered question.

| Stakeholder | Who they are | Surfaces usually seen |
|---|---|---|
| User | The person who directly uses the product's features | Web/App or Zero UI |
| Developer | The person who debugs, operates, and maintains the product | Zero UI for operations such as logs, a CLI, or another tool's dashboard, plus Web/App for the documents and runbooks they read every day |
| Admin | The person who manages, configures, and controls the product | Usually Web/App, sometimes Zero UI such as a Google Sheet |

One stakeholder may hold both surfaces at once, so record both on the same row instead of forcing a single choice.

## Two surface types

| Type | Meaning |
|---|---|
| Web/App | The stakeholder opens something the team built, in a browser or installed on a device |
| Zero UI | The stakeholder opens nothing the team built, because the product lives inside another product such as a Zalo conversation, a Google Sheet, a Slack channel, a Telegram chat, or an email thread |

A Zero UI answer must name the host product, because every later decision depends on what that host allows.

Signs the answer is really Zero UI:

- The stakeholder already spends the working day inside the host product and will not open a second tab for this.
- The product's output is a message, a row, a comment, or a file inside something the team does not own.
- Adoption depends on the host product's existing habit, not on a login the team would have to create.

An admin dashboard on the web does not make the whole product Web/App.
Record the surface per stakeholder, never one surface for the entire product.

## Four logic levels

The levels stack instead of excluding each other, so one product usually spans several of them.

| Level | What it is | How determined | What it costs |
|---|---|---|---|
| Plain code | if-else, API calls, SQL | Fully determined | Cheap, testable, clearly logged |
| Workflow | A fixed graph with an LLM sitting at a few nodes, such as n8n or a LangGraph DAG. A person designs the flow, the model does not choose it | Determined in the frame, open at the LLM nodes | Still testable node by node |
| Skill, or prompt as logic | The logic is written in natural language and the model reads it and follows it | Semi determined, because the same input can produce different output | Needs measured variance before it can be trusted |
| Agent | The model chooses the flow, chooses the tools, and loops or retries on its own | Not determined | The most flexible, the most expensive, the hardest to test and debug |

A good system is usually an agent that coordinates, calls a skill, and the skill calls determined code.
Push as much work down to plain code as it will hold, and keep an agent only where the input is genuinely open and cannot be predicted.

Signs a level has been misread:

- A graph that a person drew is a workflow even when several of its nodes call a model, so do not call it an agent.
- A long prompt is a skill, not a workflow, because nothing forces the order of its steps.
- A capability that only ever runs one fixed sequence is plain code wearing a model's costume.
- When nobody can say what the model is allowed to decide, the level has not been chosen yet.

Record the level per capability, not one level for the whole system.

## Question shapes

One question per stakeholder:

> Where does the `<stakeholder>` do this work: something we build as Web/App, or Zero UI inside another product they already use, or none for now?
> If Zero UI, name the product.

One question for logic level, listing all four levels and saying plainly that they stack:

> For `<capability>`, how determined must it be: plain code, a workflow graph with a model at a few nodes, a skill written in natural language, or an agent that decides its own flow?
> These stack, so a product usually uses several at once.

When the answer is agent or skill, ask exactly one follow-up:

> Which part of `<capability>` could move down to plain code?

One question for data:

> What has to outlive a single session, who owns it, and is anything already running that this product must reuse?

One optional question for technology:

> If you already know the technology for the logic and the store, name it.
> "Not decided yet" is a fine answer and `/build:prototype` will settle it with a spike.

## Recording rules

- Surface and logic level are not technology choices.
  Record where each stakeholder works and how determined each capability must be, and leave framework choice to `/build:prototype` and its ADRs.
- A Zero UI row without a named host product is incomplete.
- "Not decided yet" belongs in `## Risks and open decisions` as an open question, never in the table as a settled fact.
- An unanswered cell is `TODO - chưa xác nhận`.
  Never default a surface to Web/App and never default a level to plain code, because an invented answer stops anyone from checking it later.
