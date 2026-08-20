# Routine: Weekly ops review

**Cadence**: chiều thứ Sáu
**Output**: `/report/weekly-ops.md` (append theo tuần, giữ lịch sử)

## Prompt

Tổng kết tuần bằng bằng chứng từ `prd/roadmap.md`, artifact và commit thật:

1. Mục tiêu tuần là gì và có đạt không, kèm bằng chứng.
2. Đã ship gì thật sự.
3. Việc nào trượt và nguyên nhân thật là gì.
4. Có gì lọt qua `prd/evals/checklist.md` mà đáng lẽ phải bị chặn; nếu có thì đề xuất mục checklist mới.
5. Có prompt nào được gõ lại từ ba lần trở lên; nếu có thì đề xuất biến thành skill.
6. `AGENTS.md` còn khớp thực tế không; nếu một quy ước phải nhắc bằng tay hoặc bị chép sang hai file thì đề xuất sửa nguồn canonical.
7. Đề xuất mục tiêu tuần sau cùng out of scope tuần sau.

Kết thúc bằng bản nháp thay đổi cho `prd/roadmap.md` để người dùng duyệt.
Không ghi đè roadmap; `/update` làm tươi nó sau khi đề xuất được duyệt.
