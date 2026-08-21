# Routine Setup

Offer these choices before writing configuration:

| Option | Availability | Runs when | Best fit | Tradeoff |
|---|---|---|---|---|
| Stop hook | Claude Code when hooks are available | A coding session ends | Roadmap should stay fresh without memory | Runs frequently, not on a wall-clock schedule; fires only for a session opened at `<root>` |
| `/loop` | Claude Code when the command is available | At an interval during one long session | Continuous building for several hours | Stops with the session |
| `/schedule` routine | Claude Code when routines are available | A cron-like schedule, such as each morning | Long-running products with daily reporting | Requires the product repository on GitHub with Claude Code routines enabled on the account |
| External `codex exec` scheduler | Codex | At the scheduler's configured time | A portable Codex fallback | Scheduling, credentials, logging, and failure alerts are owned outside this skill set |

A Stop hook written to `<root>/.claude/settings.json` fires in a cloud session too, since that file travels with the clone; it is still not a wall-clock schedule; it fires whenever a session at `<root>` stops, cloud or local.

When `routines/update-roadmap.md` already exists, read it and propose changes to its cadence or mechanism instead of offering to create a second file for the same job.
`/build:start-repo` may seed this file once, during phase 8, as a morning brief; `/build:update` owns refreshing it afterward.
Neither skill touches `weekly-ops-review.md` or `pr-auto-review.md`, which belong to `/build:start-repo` alone.

Write the approved routine definition to `routines/update-roadmap.md` with schedule, enabled sources, scan root, deduplication policy, conflict policy, and report path.
Each run appends `report/product/roadmap-<YYYY-MM-DD>.md` using the three parts in [REPORT-FORMAT.md](REPORT-FORMAT.md).
This daily roadmap routine and its report replace a separate daily brief.

An unattended run skips the Phase 0 language question and reads both the language and the working timezone from the Conventions lines in `AGENTS.md` instead.
A user-started asynchronous Codex Cloud run is not unattended and still waits for review approval across turns.

Offer only mechanisms exposed by the current host.
When Codex has no native mechanism capable of running this routine, keep the approved routine file, state that nothing runs it automatically, and offer manual `$build:update` or an external scheduler that runs `codex exec` from `<root>`.

For a Stop hook, show the exact merged JSON patch for `<root>/.claude/settings.json`.
State plainly that such a hook fires only for sessions opened in `<root>`, so it does nothing while the chain is driven from the skill-set repository; when that is the user's normal way of working, recommend only another mechanism exposed by the current host.
Preserve existing settings.
Wait for explicit approval before writing the settings file.
The hook should invoke the roadmap update command without suppressing its conflict report.
