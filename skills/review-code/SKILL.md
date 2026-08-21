---
name: review-code
description: Use when reviewing an implementation diff against its product specification and the repository's code standards on separate axes.
---

# Review Code

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

Use the `<root>` supplied by the calling skill.
When no caller supplied one, resolve it with `git rev-parse --show-toplevel`, and reject a repository whose root contains `skills/start-repo/SKILL.md` and either `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json`, because that is the skill-set repository and never a valid `<root>`.
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
