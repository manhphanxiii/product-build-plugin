# Routine: PR auto-review

**Cadence**: mỗi khi có PR mới
**Output**: comment trên PR

## Prompt

Chạy toàn bộ `prd/evals/checklist.md` với diff của PR này.
Với mỗi mục, báo pass, fail hoặc không áp dụng kèm dẫn chứng file và dòng.

Sau checklist, trả lời riêng:

- PR có nằm trong mục tiêu ở `prd/roadmap.md` không?
- PR có đủ nhỏ để review trong một lượt không; nếu không thì nên tách thế nào?
- `prd/architecture.md`, `prd/adr/` và tài liệu liên quan đã được cập nhật chưa?
- `/evals-gate` đã pass khi thay đổi cần cổng eval chưa?

Nếu chạm auth, payment hoặc production data, gắn nhãn cần người duyệt và dừng.
