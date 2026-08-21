# Roadmap Format

The scaffold seeds this file and `/build:start-repo` fills it.
`/build:update` refreshes overall progress, weekly goal, out of scope, blockers, and the next command.
Each chain skill updates only its own step and the task or decision rows it just completed.
The step 1 row and the note line under the Tiến độ table are owned exclusively by `/build:start-repo`; no other skill edits them.

Use [assets/roadmap.md.template](assets/roadmap.md.template) as the canonical structure.
`/build:update` owns Out of scope and fills it from `prd/concept.md`.
Use only `chưa bắt đầu`, `đang làm`, and `hoàn thành` for progress-row status, translated to the file's content language when needed.
Task-row status comes from ticket frontmatter and remains the English values `ready` or `done`.

Every status and cell must come from repository evidence.
Preserve Task rows created from external sources when refreshing progress.
