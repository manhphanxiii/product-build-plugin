# Routine Setup

Offer these choices before writing configuration:

| Option | Runs when | Best fit | Tradeoff |
|---|---|---|---|
| Stop hook | A coding session ends | Roadmap should stay fresh without memory | Runs frequently and changes local settings |
| `/loop` | At an interval during one long session | Continuous building for several hours | Stops with the session |
| Scheduled routine | A cron-like schedule, such as each morning | Long-running products with daily reporting | Requires scheduler setup and credentials |

Write the approved routine definition to `routines/update-roadmap.md` with schedule, enabled sources, scan root, deduplication policy, conflict policy, and report path.
Each run appends `report/product/roadmap-<YYYY-MM-DD>.md` with scanned sources, skipped sources, proposed changes, applied changes, and unresolved conflicts.
This daily roadmap routine and its report replace a separate daily brief.
`/update` owns only `routines/update-roadmap.md`; routines installed by `/start-repo` are outside its write scope.

For a Stop hook, show the exact merged JSON patch for `<root>/.claude/settings.json`.
State plainly that such a hook fires only for sessions opened in `<root>`, so it does nothing while the chain is driven from the skill-set repository; when that is the user's normal way of working, recommend `/loop` or a scheduled routine instead.
Preserve existing settings.
Wait for explicit approval before writing the settings file.
The hook should invoke the roadmap update command without suppressing its conflict report.
