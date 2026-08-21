# Routine: Morning brief

**Cadence**: hàng ngày {{BRIEF_TIME}} ({{TIMEZONE}})
**Output**: `report/product/roadmap-<YYYY-MM-DD>.md`

## Prompt

Chạy `/build:update` không tương tác trong `<root>`.
Bỏ qua câu hỏi ngôn ngữ và lấy ngôn ngữ cùng múi giờ từ các dòng Conventions trong `AGENTS.md`.
Ghi báo cáo ba phần theo `REPORT-FORMAT.md`.
Không tự ghi vào `prd/roadmap.md`; để phần đề xuất lại cho người dùng duyệt ở lần chạy có người.
