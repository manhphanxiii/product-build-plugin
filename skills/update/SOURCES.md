# Information Sources

Read source enablement and roots from `prd/README.md`.
Report disabled sources before scanning.
Every path here is relative to the `<root>` resolved in [SKILL.md](SKILL.md), and every `git` or `gh` command runs with `<root>` as the working directory.

## GitHub Issues

Use the built-in GitHub tools to list open issues; fall back to `gh issue list --state open --json number,title,labels,assignees` only when the built-in tools are unavailable and `gh` is installed. A cloud session does not have `gh` installed.
Create source labels such as `github#12`.

## GitHub pull requests

Use the built-in GitHub tools to list pull requests; fall back to `gh pr list --json number,title,state` only when the built-in tools are unavailable and `gh` is installed.
Extract unfinished work and review blockers.

## Commits

Run `git -C <root> log` from the last update timestamp recorded in the roadmap or latest product report.
Use commits only as evidence that tracked work may already be complete.

## Notion

Use the available Notion connector to search pages and databases under the configured product root.
Do not search outside that root.
Use source labels such as `notion:<page title>`.

## Current chat

Extract product work agreed in the current conversation but not yet recorded.
Use `chat:<date>` as the source.

## Repository tickets

Read `Status:` and `Blocked by:` in `prd/tickets/*.md`.
Use the ticket path as the source.

## Reconciliation

Normalize titles by intended outcome, not wording alone.
Merge sources only when they refer to the same deliverable.
List all supporting sources in one cell.
If completion state differs, preserve both claims as a conflict and ask the user.
