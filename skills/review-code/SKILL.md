---
name: review-code
description: Use when reviewing an implementation diff against its product specification and the repository's code standards on separate axes.
---

# Review Code

## Root resolution

Use the `<root>` supplied by the calling skill.
When no caller supplied one, resolve it with `git rev-parse --show-toplevel`, and reject a repository whose root contains both `.claude-plugin/plugin.json` and `skills/start-repo/SKILL.md`, because that is the skill-set repository and never a valid `<root>`.
Every path in this skill without an explicit prefix is relative to `<root>`, and every Git command runs as `git -C <root> ...`.
Pass `<root>` to every sub-agent so both axes read the same repository.

Verify that the diff is non-empty before delegating.
Use the merge base with the default branch as the fixed point unless the caller supplies another one.
Review `git -C <root> diff <fixed-point>...HEAD`.

When delegation is available, run two sub-agents in parallel so their contexts remain independent; otherwise review the two axes sequentially and keep their reports separate.
Limit each report to fewer than 400 words.

## Spec axis

Read the relevant files under `prd/tickets/` and `prd/PRD.md` directly.
Do not use an issue tracker as the specification source.
Find only three classes of mismatch: missing or partial behavior, out-of-scope behavior, and implemented behavior that is incorrect.
For each finding, cite the corresponding specification line and the affected code location.

## Standards axis

Read [SMELLS.md](SMELLS.md), the repository's `prd/evals/checklist.md`, relevant repository standards, and nearby code under `app/`.
Evaluate clarity, consistency, maintainability, and fit with local patterns.

Return findings under exactly `## Spec` and `## Standards`.
Do not mix the axes or rank findings across them.
If an axis has no findings, say so explicitly.
