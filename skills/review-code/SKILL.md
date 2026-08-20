---
name: review-code
description: Use when reviewing an implementation diff against its product specification and the repository's code standards on separate axes.
---

# Review Code

Resolve the repository root and verify that the diff is non-empty before delegating.
Use the merge base with the default branch as the fixed point unless the caller supplies another one.
Review `git diff <fixed-point>...HEAD`.

Run two sub-agents in parallel so their contexts remain independent.
Limit each report to fewer than 400 words.

## Spec axis

Read the relevant files under `prd/tickets/` and `prd/PRD.md` directly.
Do not use an issue tracker as the specification source.
Find only three classes of mismatch: missing or partial behavior, out-of-scope behavior, and implemented behavior that is incorrect.
For each finding, cite the corresponding specification line and the affected code location.

## Standards axis

Read [SMELLS.md](SMELLS.md), the repository's `prd/evals/checklist.md`, relevant repository standards, and nearby code under `app/`.
Evaluate clarity, consistency, maintainability, and fit with local patterns.
Do not report issues already enforced by the configured linter.
Treat smell guidance as judgment, with repository standards taking precedence.

Return findings under exactly `## Spec` and `## Standards`.
Do not mix the axes or rank findings across them.
If an axis has no findings, say so explicitly.
