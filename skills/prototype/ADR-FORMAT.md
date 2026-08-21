# ADR Format

Name files `NNNN-<slug>.md` under `prd/adr/`.
Use `proposed` while a decision is under review, `accepted` when it is active, `superseded by ADR-NNNN` when a newer ADR replaces it, and `deprecated` when it is no longer active without a replacement.

```md
---
ADR: ADR-NNNN
Status: proposed
Date: YYYY-MM-DD
---

# <Decision title>

## Context

<Why this decision exists and why it is difficult to reverse or surprising>
Record constraints as they existed then without rewriting them using current knowledge.

## Decision

<The chosen option>

## Tradeoff

List every rejected alternative and the reason it lost, one alternative per line.
This is the most valuable part of the ADR because future contributors will rediscover the same options and otherwise restart the debate.

- <Alternative>: rejected because <reason>

## Evidence

<Prototype, measurement, or discussion that supports the decision>

## Revisit condition

<State when this decision should be reconsidered>
If there is no condition, state that it is intended to remain long term.
```

An ADR may be one concise paragraph when that preserves the decision and rationale.
Do not create an ADR unless all three gates in the skill are met.
