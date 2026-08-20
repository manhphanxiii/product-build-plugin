# Roadmap Format

`/start-repo` creates this file once.
`/update` refreshes overall progress, weekly goal, out of scope, blockers, and the next command.
Each chain skill updates only its own step and the task or decision rows it just completed.

```md
# Roadmap - <product name or TODO>

Cập nhật: <YYYY-MM-DD HH:MM>

## Mục tiêu tuần này

Hoàn thành `prd/concept.md`.

## Out of scope

TODO - `/idea-to-product-concept` sẽ xác nhận và điền từ concept.

## Tiến độ

| Bước | Lệnh | Trạng thái | Artifact | Ngày |
|---|---|---|---|---|
| 1. Concept | /idea-to-product-concept | chưa bắt đầu | prd/concept.md | |
| 2. Prototype | /prototype | chưa bắt đầu | prd/adr/ | |
| 3. PRD | /to-prd | chưa bắt đầu | prd/PRD.md, prd/architecture.md | |
| 4. Tickets | /to-ticket | chưa bắt đầu | prd/tickets/ | |
| 5. Implement | /implement | chưa bắt đầu | app/ | |
| 6. Evals | /evals-gate | chưa bắt đầu | prd/evals/ | |

## Task

| # | Task | Nguồn | Blocked by | Trạng thái | Commit |
|---|---|---|---|---|---|

## Quyết định đã chốt

- [ADR-0001](adr/0001-<slug>.md): <summary>

## Đang vướng

- <open question, what unlocks it, and source>

## Bước kế tiếp

/idea-to-product-concept - cần chốt concept có bằng chứng trước mọi quyết định sản phẩm khác.
```

Every status and cell must come from repository evidence.
Preserve Task rows created from external sources when refreshing progress.

