# Report Format

`/update` prints this three-part report on every interactive run.
Every routine or morning brief report at `report/product/roadmap-<YYYY-MM-DD>.md` uses the same three parts.

```md
# Update - <YYYY-MM-DD HH:MM>

## 1. Cập nhật roadmap.md

| Bước | Lệnh | Trạng thái | Artifact | Ngày | Bằng chứng |
|---|---|---|---|---|---|
| 1. Concept | /idea-to-product-concept | xong | prd/concept.md | 2026-08-20 | file tồn tại, commit <sha> |
| 2. Prototype | /prototype | đang làm | prd/adr/ | | ADR-0001 nháp |

Đã xong: <danh sách bước>.
Chưa xong: <danh sách bước>.

Đề xuất ghi vào roadmap: <n> dòng bước, <n> task mới, <n> đổi trạng thái.

## 2. Current task

| # | Task | Nguồn | Blocked by | Trạng thái | Bước |
|---|---|---|---|---|---|

Lệnh tiếp theo: /<command> - <một câu lý do>.

## 3. Note

- <xung đột nguồn, blocker, nguồn bị tắt, lệch ngôn ngữ>
```

## Part 1 - Cập nhật roadmap.md

The table is the same six-step big picture that `/start-repo` creates, plus one line naming which steps are done and one line naming which are not.
Every status cell must carry repository evidence such as a file path, a ticket `Status: done`, or a commit identifier; never guess a status.
End this part with the proposed diff grouped as new tasks, status changes, and conflicts, so the user approves a specific set of edits.

## Part 2 - Current task

List every open task in one list: Task rows from `prd/roadmap.md`, open tickets in `prd/tickets/`, new tasks found from the sources in [SOURCES.md](SOURCES.md), and whatever the chain's current step still needs.
Order `ready` tasks first by value; list blocked tasks after them, each naming what blocks it.
End this part with exactly one recommended next command and one sentence explaining why.

## Part 3 - Note

Optional.
Use it for source conflicts, disabled sources, blockers that do not fit a single task row, and language mismatches against `AGENTS.md`.
Omit the whole section when there is nothing to note; never write a placeholder line such as `Chưa có.`.
