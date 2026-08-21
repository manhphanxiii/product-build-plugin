# Routine Setup

Offer these choices before writing configuration:

| Option | Runs when | Best fit | Tradeoff |
|---|---|---|---|
| Stop hook | A coding session ends | Roadmap should stay fresh without memory | Runs frequently, not on a wall-clock schedule; fires only for a session opened at `<root>` |
| `/loop` | At an interval during one long session | Continuous building for several hours | Stops with the session |
| `/schedule` routine | A cron-like schedule, such as each morning | Long-running products with daily reporting | Runs on Anthropic-managed cloud infrastructure; requires the product repository on GitHub with Claude Code routines enabled on the account |

A Stop hook written to `<root>/.claude/settings.json` fires in a cloud session too, since that file travels with the clone; it is still not a wall-clock schedule; it fires whenever a session at `<root>` stops, cloud or local.

When `routines/update-roadmap.md` already exists, read it and propose changes to its cadence or mechanism instead of offering to create a second file for the same job.
`/build:start-repo` may seed this file once, during phase 4b, as a morning brief; `/build:update` owns refreshing it afterward.
Neither skill touches `weekly-ops-review.md` or `pr-auto-review.md`, which belong to `/build:start-repo` alone.

Write the approved routine definition to `routines/update-roadmap.md` with schedule, enabled sources, scan root, deduplication policy, conflict policy, and report path.
Each run appends `report/product/roadmap-<YYYY-MM-DD>.md` using the three parts in [REPORT-FORMAT.md](REPORT-FORMAT.md).
This daily roadmap routine and its report replace a separate daily brief.

An unattended run skips the Phase 0 language question and reads both the language and the working timezone from the Conventions lines in `AGENTS.md` instead.

For a Stop hook, show the exact merged JSON patch for `<root>/.claude/settings.json`.
State plainly that such a hook fires only for sessions opened in `<root>`, so it does nothing while the chain is driven from the skill-set repository; when that is the user's normal way of working, recommend `/loop` or a scheduled routine instead.
Preserve existing settings.
Wait for explicit approval before writing the settings file.
The hook should invoke the roadmap update command without suppressing its conflict report.
