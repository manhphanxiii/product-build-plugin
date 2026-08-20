# Code Smells Baseline

Repository standards override this baseline.
Every smell is a judgment call, not a hard violation.
Skip conditions already enforced by the repository linter.

## Misleading names

What it is: a name hides side effects, uses a different domain term, or promises broader behavior than the code provides.
How to fix it: rename around observable responsibility and the repository vocabulary.

## Mixed responsibilities

What it is: one module changes for unrelated reasons or combines policy with infrastructure details.
How to fix it: separate responsibilities at a stable interface that improves locality.

## Long parameter lists

What it is: callers must know too many unrelated details or repeatedly pass the same group of values.
How to fix it: introduce a cohesive input object or move behavior to the abstraction that owns the data.

## Primitive obsession

What it is: important domain rules are spread across strings, numbers, or booleans with no validating boundary.
How to fix it: introduce a small domain type only where it centralizes real invariants.

## Shotgun surgery

What it is: one behavior change requires small edits across many unrelated modules.
How to fix it: move the behavior behind the interface that owns the reason for change.

## Hidden temporal coupling

What it is: functions must be called in an undocumented order for state to remain valid.
How to fix it: encode the sequence in an API, state machine, or constructed valid state.

## Accidental duplication

What it is: the same rule is independently encoded in several places and can drift.
How to fix it: centralize the rule when the duplication represents the same reason to change, but keep coincidental similarity separate.

## Unnecessary indirection

What it is: wrappers and abstractions add navigation cost without hiding volatility or enforcing a rule.
How to fix it: inline the layer or give it a concrete responsibility.

## Broad error handling

What it is: errors are swallowed, converted without context, or caught farther from the recovery decision than necessary.
How to fix it: preserve cause and context, and handle only errors the current boundary can resolve.

## Brittle tests

What it is: tests assert implementation detail instead of behavior at the approved seam.
How to fix it: assert observable behavior and keep implementation-specific checks only where they protect an intentional contract.
