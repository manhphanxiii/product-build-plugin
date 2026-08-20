# Architecture

## Application tree

Show the approved directory tree inside `app/`.
Include `app/knowledge-base/` and identify exactly which application module may write runtime knowledge there.
Agents may not edit its runtime content by hand.

## Modules and interfaces

For each module, state responsibility, public interface, dependencies, and invariants.

## Data model

Describe entities, ownership, lifecycle, and persistence boundaries.

## Main flows

Describe important request, event, and state transitions.

## Test seams

Name the seams where behavior can be tested with focused feedback.
Record the suitable test level and required fakes or adapters.

## External dependencies

Every dependency must have a stated reason to exist.

| Dependency | Purpose | Replaceable? |
|---|---|---|

## Boundaries

State which modules must not call each other directly and why.
This is the boundary agents are most likely to violate because crossing it is often the shortest path to making a task run.

## Accepted decisions

Link every accepted ADR and summarize its consequence.
