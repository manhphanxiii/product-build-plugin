# Roadmap Format

`/build:start-repo` creates this file once.
`/build:update` refreshes overall progress, weekly goal, out of scope, blockers, and the next command.
Each chain skill updates only its own step and the task or decision rows it just completed.
The step 1 row and the note line under the Tiến độ table are owned exclusively by `/build:start-repo`; no other skill edits them.

```md
# Roadmap - <product name or TODO>

Cập nhật: <YYYY-MM-DD HH:MM>

## Mục tiêu tuần này

Hoàn thành `prd/concept.md`.

## Out of scope

TODO - `/build:idea-to-product-concept` sẽ xác nhận và điền từ concept.

## Tiến độ

| Bước | Lệnh | Trạng thái | Artifact | Ngày |
|---|---|---|---|---|
| 1. Start repo | /build:start-repo | hoàn thành | AGENTS.md, CLAUDE.md, prd/evals/checklist.md | <YYYY-MM-DD> |
| 2. Concept | /build:idea-to-product-concept | chưa bắt đầu | prd/concept.md | |
| 3. Prototype | /build:prototype | chưa bắt đầu | prd/adr/ | |
| 4. PRD | /build:to-prd | chưa bắt đầu | prd/PRD.md, prd/architecture.md | |
| 5. Tickets | /build:to-ticket | chưa bắt đầu | prd/tickets/ | |
| 6. Implement | /build:implement | chưa bắt đầu | app/ | |
| 7. Evals | /build:evals-gate | chưa bắt đầu | prd/evals/ | |

Ngôn ngữ: <ngôn ngữ hội thoại>. Múi giờ: <timezone>. Routine morning brief: <đã cài lúc HH:MM / chưa cài>.

## Task

| # | Task | Nguồn | Blocked by | Trạng thái | Commit |
|---|---|---|---|---|---|

## Quyết định đã chốt

- [ADR-0001](adr/0001-<slug>.md): <summary>

## Đang vướng

- <open question, what unlocks it, and source>

## Bước kế tiếp

/build:idea-to-product-concept - cần chốt concept có bằng chứng trước mọi quyết định sản phẩm khác.
```

Every status and cell must come from repository evidence.
Preserve Task rows created from external sources when refreshing progress.

