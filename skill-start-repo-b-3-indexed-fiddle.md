# Sửa skill `start-repo`: rút gọn interview và thêm hai chế độ khởi tạo

## Context

`/start-repo` hiện hỏi bốn câu ở phase 2, trong đó ba câu gây vấn đề:

- Câu về commands trùng với check số 10 ở [REPO-CHECKS.md](skills/start-repo/REPO-CHECKS.md#L14), vốn đã tự dò lệnh từ manifest.
- Câu về tiêu chí chất lượng sản phẩm mâu thuẫn với chính ground rule của skill: "Do not interview about the product, buyer, promise, or scope" ([SKILL.md:26](skills/start-repo/SKILL.md#L26)).
- Câu về routines là lựa chọn nhị phân mà mặc định cài cả hai luôn đúng hơn, vì routine chỉ là file mô tả, không tự chạy.

Đồng thời skill giả định người dùng đã đứng sẵn trong đúng repo sản phẩm.
Trường hợp thật hay gặp là đã có một app đang chạy với cấu trúc riêng, không muốn đập đi xây lại.
Skill hiện không có đường nào để bọc app đó lại theo layout chuẩn.

Kết quả mong muốn: phase 2 chỉ còn một câu hỏi ngôn ngữ, và `/start-repo` mở đầu bằng việc chọn một trong hai chế độ rõ ràng - `new` cho trang giấy trắng, `restructure` cho khi đã có code.

## Quyết định đã chốt với user

- Đúng hai chế độ: `new` và `restructure`. Hành vi cũ "chạy ngay trong repo sản phẩm" không còn là chế độ riêng, nó là một nhánh của `restructure`.
- Cả hai chế độ đều hỏi đường dẫn repo sản phẩm rồi tự `mkdir -p` + `git init`, không bắt user chuẩn bị trước.
- Ánh xạ ở `restructure`: skill quét code có sẵn và đề xuất một bảng - vai trò nào trỏ symlink sang folder có sẵn, vai trò nào tạo mới - user duyệt từng dòng.
- `app/knowledge-base/`: không tạo khi `app/` là symlink, chỉ ghi TODO. Không ghi bất cứ thứ gì vào app repo có sẵn.
- Routines: cài cả hai mặc định, không hỏi.

## Hai chế độ

### `new` - trang giấy trắng

Chưa có code. Skill hỏi đường dẫn repo sản phẩm, `mkdir -p` + `git init`, dựng đủ layout gồm cả `app/` và `app/knowledge-base/`, rồi đi thẳng theo chuỗi skill từ bước 1.
Không có bảng ánh xạ vì không có gì để ánh xạ.

### `restructure` - đã có app hoặc code

Skill hỏi hai đường dẫn trong cùng một batch:

1. App repo đang chạy nằm ở đâu.
2. Repo sản phẩm dựng ở đâu - **tại chỗ** trong chính app repo đó, hoặc **tại folder riêng** cạnh nó.

Hai nhánh dùng chung một cơ chế duy nhất là bảng đề xuất từng vai trò, chỉ khác gốc:

- **Tại chỗ**: gốc là chính app repo. Code production giữ nguyên vị trí, ghi vào `AGENTS.md` là `app-dir` thật (`src/`, `apps/web/`...). Vai trò nào đã có folder tương ứng thì symlink tên canonical vào nó, còn lại tạo mới.
- **Folder riêng**: gốc là repo sản phẩm mới. `app/` symlink sang app repo có sẵn, các vai trò khác symlink hoặc tạo mới theo bảng.

Trong cả hai nhánh, app repo có sẵn không bị di chuyển, đổi tên hay sửa nội dung.

## Thay đổi

### 1. `skills/start-repo/SKILL.md`

**Thêm "Phase 0: chọn chế độ"** đặt trước phase 1.

Hỏi `new` hay `restructure` theo mô tả ở mục Hai chế độ bên trên, rồi hỏi đường dẫn tương ứng.
Nêu rõ tiêu chí chọn: chưa có dòng code nào thuộc sản phẩm này thì `new`, ngược lại là `restructure`.
Chốt và in ra `<root>` đã giải quyết trước khi sang phase 1, vì mọi phase sau đều tính đường dẫn từ nó.

**Sửa ground rules** ở khối [SKILL.md:12-19](skills/start-repo/SKILL.md#L12-L19):

- `<root>` đến từ phase 0, không còn luôn là `git rev-parse --show-toplevel` của thư mục hiện tại.
- Ở nhánh folder riêng, không bao giờ tạo, sửa hay xoá file bên trong app repo có sẵn, kể cả `knowledge-base`.
- Sau khi tạo symlink, đề xuất riêng việc thêm tên các symlink đó vào `.gitignore`, giữ nguyên nguyên tắc scaffold không tự sửa `.gitignore`.

**Thêm "Phase 1b: đề xuất ánh xạ"**, chỉ chạy ở chế độ `restructure`, sau phase 1.

Quét read-only code có sẵn, đối chiếu với bảng vai trò ở [REPO-LAYOUT.md](skills/start-repo/REPO-LAYOUT.md), rồi in đúng một bảng:

| Vai trò canonical | Đề xuất | Nguồn có sẵn | Lý do |
|---|---|---|---|
| `app/` | symlink | `../my-running-app/` | toàn bộ repo đó là code production |
| `prd/` | symlink | `docs/product/` | đã có tài liệu sản phẩm ở đây |
| `client-note/` | tạo mới | - | không tìm thấy tiếng nói khách hàng |

Quy tắc đề xuất:

- Chỉ đề xuất symlink khi tìm thấy folder có sẵn thật sự khớp vai trò. Không khớp thì đề xuất tạo mới.
- Nhánh tại chỗ: `app/` không symlink; ghi `app-dir` thật vào bảng ánh xạ trong `AGENTS.md` và chạy scaffold với `--retrofit --app-dir <đường dẫn đã dò>`.
- Không bao giờ đề xuất symlink cho `routines/` và `report/`: hai thư mục này thuộc về repo sản phẩm.
- Nêu rõ hệ quả: folder symlink là cửa ghi thẳng vào đích thật, mọi thay đổi ở đó nằm trong git history của repo chứa đích, không phải repo sản phẩm.

Chờ duyệt từng dòng trước khi chạy scaffold. Không tự sửa cấu trúc bên trong app repo có sẵn.

**Phase 2 rút còn một câu.**
Thay khối [SKILL.md:42-54](skills/start-repo/SKILL.md#L42-L54) bằng một câu hỏi duy nhất về ngôn ngữ file sinh ra (Vietnamese hoặc English), giữ định dạng `❓ **Q1** - **<title>**` + `➡️ <recommended answer>`.
Bỏ toàn bộ ba câu còn lại và các đoạn hướng dẫn đi kèm chúng.

**Bù lại phần dữ liệu ba câu kia từng cung cấp**, thêm vào phase 3:

- Commands: chỉ điền lệnh đã xác minh được ở check số 10. Mọi lệnh chưa xác minh giữ nguyên `TODO`. Không hỏi, không đoán. Giữ câu "A missing command is safer than a plausible but incorrect command" nhưng chuyển xuống phase 3.
- Tiêu chí chất lượng riêng: không điền. Template để sẵn TODO có ghi rõ chủ sở hữu là `/to-prd`.
- Routines: luôn copy cả `weekly-ops-review.md` và `pr-auto-review.md` vào `routines/`, thay cho câu "Install only the routines selected in question 4".

### 2. `skills/start-repo/scripts/scaffold.py`

Thêm ba khả năng, giữ nguyên bất biến "không bao giờ ghi đè file đã tồn tại":

- `--link ROLE=PATH` (lặp lại được): tạo symlink `<root>/ROLE` trỏ tới `PATH` thay vì tạo thư mục thật. Dùng `os.path.relpath` để lưu symlink tương đối khi có thể, tuyệt đối khi không. Bỏ qua và báo `skipped` nếu `<root>/ROLE` đã tồn tại. Thoát lỗi rõ ràng nếu `PATH` không tồn tại hoặc không phải thư mục. Role đã symlink thì không tạo README bên trong.
- `--no-knowledge-base`: bỏ qua việc tạo `<app-dir>/knowledge-base`, dùng khi `app/` là symlink.
- `--init-git`: chạy `git init` nếu `<root>` chưa là git repo, phục vụ cả hai chế độ vì cả hai đều có thể tạo folder mới.

`--retrofit` và `--app-dir` giữ nguyên, dùng cho nhánh tại chỗ.
Output in thêm mục riêng liệt kê symlink đã tạo kèm đích thật, để relay verbatim theo phase 3.

### 3. `skills/start-repo/REPO-CHECKS.md`

- Sửa check 1: `<root>` đến từ phase 0. Chế độ `new` xác minh đường dẫn chưa tồn tại hoặc còn trống. Chế độ `restructure` xác minh app repo có sẵn tồn tại, là git repo, đọc được, và nếu chọn folder riêng thì folder đó chưa có gì xung đột.
- Thêm check quét ánh xạ ở chế độ `restructure`: liệt kê thư mục cấp một của app repo và đối chiếu vai trò canonical, không sửa gì.
- Thêm check symlink: xác minh filesystem hỗ trợ symlink và không có va chạm tên ở gốc.
- Sửa check 11: ở chế độ `restructure`, đề xuất `.gitignore` gồm cả tên các symlink.
- Sửa dòng 18-20 để phản ánh việc commands giờ hoàn toàn đến từ discovery, không từ interview.

### 4. `skills/start-repo/REPO-LAYOUT.md`

Thêm một mục "Linked layout" mô tả:

- Ở chế độ `restructure`, một vài đường dẫn canonical là symlink trỏ sang folder có sẵn.
- Write policy của vai trò không đổi khi nó là symlink, nhưng ghi vào đó là ghi vào repo chứa đích.
- `app/knowledge-base/` là TODO cho tới khi `prd/architecture.md` định nghĩa dữ liệu runtime, khi `app/` là symlink.
- Bảng ánh xạ thật của repo cụ thể sống ở `AGENTS.md`, không chép sang file khác.

### 5. `skills/start-repo/assets/AGENTS.md.template`

Thêm section `## Cấu trúc và liên kết` ngay sau `## Canonical sources`, chứa bảng vai trò canonical -> đường dẫn thật, cùng cột ghi rõ là symlink hay thư mục thật.
Ở chế độ `new`, section này ghi một dòng "toàn bộ vai trò là thư mục thật trong repo này".

### 6. `skills/start-repo/assets/checklist.md.template`

Thay `{{PRODUCT_CRITERION_1}}` và `{{PRODUCT_CRITERION_2}}` bằng TODO tự mô tả, ghi rõ tiêu chí riêng được `/to-prd` bổ sung từ PRD, và nêu tiêu chí phải là kết quả quan sát được chứ không phải khẳng định chung chung.
Nhờ vậy scaffold không còn placeholder nào cần thay ở bước này.

### 7. `skills/start-repo/PRINCIPLES.md`

Thêm principle ngắn "Bọc thay vì đập đi xây lại": app đang chạy là bằng chứng, không phải nợ kỹ thuật cần dọn trước khi bắt đầu; repo sản phẩm thêm lớp quyết định và chất lượng quanh nó mà không ép di chuyển code.

### 8. `README.md`

Cập nhật dòng `/start-repo` trong bảng bản đồ chuỗi và mục "Cấu trúc repo lớn": mô tả hai chế độ `new` và `restructure`, kèm một cây ví dụ cho `restructure` nhánh folder riêng với `app -> ../<app-repo>/`.
Giữ tiếng Việt, mỗi câu một dòng, theo [AGENTS.md:10](AGENTS.md#L10) và [AGENTS.md:21-22](AGENTS.md#L21-L22).

## Không đụng tới

- `.claude/skills/start-repo/SKILL.md` là pointer, không cần đổi.
- `skills/start-repo/agents/openai.yaml`, `ROADMAP-FORMAT.md`, các skill khác trong chuỗi.
- `link.sh` (chỉ chạy khi user cho phép rõ ràng).

## Verification

Chạy trong scratchpad, không đụng repo thật:

1. Dựng app repo giả: `mkdir -p <scratch>/fake-app/{src,notes/calls,docs/product}` rồi `git init` trong đó.
2. `restructure` nhánh folder riêng:
   `python3 scripts/scaffold.py <scratch>/new-product --init-git --no-knowledge-base --link app=<scratch>/fake-app --link prd=<scratch>/fake-app/docs/product`
   Kiểm tra: `app` và `prd` là symlink tương đối trỏ đúng đích; `client-note/`, `demos/`, `routines/`, `report/product/` là thư mục thật có README; không có `knowledge-base`; `git -C <scratch>/fake-app status --porcelain` phải trống.
3. `restructure` nhánh tại chỗ:
   `python3 scripts/scaffold.py <scratch>/fake-app --retrofit --app-dir src --link prd=docs/product`
   Kiểm tra: `src/` nguyên vẹn, `prd` là symlink tới `docs/product`, các vai trò còn lại tạo mới.
4. `new`: `python3 scripts/scaffold.py <scratch>/blank-product --init-git`
   Kiểm tra: có `.git`, có `app/README.md` và `app/knowledge-base/README.md`, đủ sáu đích top-level.
5. Idempotency: chạy lại từng lệnh trên lần hai, mọi thứ phải vào danh sách `Bỏ qua`, không ghi đè, không đổi symlink.
6. Trường hợp lỗi: `--link app=<đường dẫn không tồn tại>` phải thoát với thông báo rõ ràng, không tạo repo dở dang.
7. Đọc lại `SKILL.md` end-to-end kiểm tra phase 2 chỉ còn Q1, và grep sạch tàn dư:
   `grep -rn "PRODUCT_CRITERION\|question 4\|four questions\|adopt" skills/start-repo/`
