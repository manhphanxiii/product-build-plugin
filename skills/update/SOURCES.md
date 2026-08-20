# Information Sources

Read source enablement and roots from `prd/README.md`.
Report disabled sources before scanning.

## GitHub Issues

Run `gh issue list --state open --json number,title,labels,assignees`.
Create source labels such as `github#12`.

## GitHub pull requests

Run `gh pr list --json number,title,state`.
Extract unfinished work and review blockers.

## Commits

Run `git log` from the last update timestamp recorded in the roadmap or latest product report.
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
