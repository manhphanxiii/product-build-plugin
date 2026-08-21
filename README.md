# Product Building Agents

Đây là một bộ skill độc lập dẫn sản phẩm từ ý tưởng đến code đã qua cổng ship.
Chuỗi tạo ra folder `app/` chạy được thật và ghi mọi quyết định thành artifact theo cấu trúc repo lớn.
Mỗi bước chính dùng một context window riêng và để lại bằng chứng trong repo sản phẩm.

## Bản đồ chuỗi

| Bước | Lệnh | Kết quả |
|---|---|---|
| 0 | `/build:start-repo` | Hỏi repo sản phẩm, soi trước rồi mới đề xuất chỗ đặt (`new` hoặc `restructure`), dựng workspace quanh code mới hoặc app có sẵn, ghi cấu hình, tạo roadmap ban đầu, và hỏi có kích hoạt morning brief hàng ngày không |
| 1 | `/build:idea-to-product-concept` | Phân tích tư liệu, phỏng vấn và ghi `prd/concept.md` |
| 2 | `/build:prototype` | Chạy spike để chốt quyết định và ghi ADR |
| 3 | `/build:to-prd` | Ghi `prd/PRD.md`, `prd/architecture.md` và hoàn tất ADR |
| 4 | `/build:to-ticket` | Chia kế hoạch thành ticket vertical slice |
| 5 | `/build:implement` | Làm một ticket trong `app/`, review và commit |
| 6 | `/build:evals-gate` | Chạy eval và chặn ship nếu chưa đạt ngưỡng |
| Lặp lại | `/build:update` | Hỏi ngôn ngữ hội thoại rồi in báo cáo ba phần: cập nhật roadmap, current task, note |
| Nội bộ | `/build:review-code` | Review diff theo Spec và Standards, thường do `/build:implement` gọi |
| Nội bộ | `/build:lavish` | Tạo bề mặt HTML để review và annotate |

Chạy `/clear` giữa các bước chính và giữa mỗi ticket ở bước 5.
Sau bước 0, chạy `/build:update` để làm tươi tiến độ và biết đúng một lệnh tiếp theo.
Mỗi bước chính, kể cả `/build:update`, kết thúc bằng cách nêu tên lệnh tiếp theo và hỏi có muốn tiếp tục ngay không, không kết thúc im lặng.

## Chạy chuỗi từ đâu

Sau khi cài plugin, gọi lệnh từ bất kỳ đâu; không cần mở repo này.
Repo này chỉ là nguồn của bộ skill, không phải nơi chứa artifact, và không bao giờ là repo sản phẩm.
Mỗi skill tự giải `<root>` là repo sản phẩm: dùng đường dẫn bạn cung cấp, nếu không có thì lấy git root của thư mục hiện tại.
`<root>` chỉ hợp lệ khi tồn tại `<root>/prd/roadmap.md`, và repo bộ skill này không bao giờ là `<root>`.
Root không hợp lệ thì skill in đường dẫn đã giải, nêu lý do, rồi hỏi một câu về đường dẫn repo sản phẩm; nó không bao giờ tự tạo `prd/`, `app/` hay `demos/` trong repo bộ skill.
Mọi path trong skill không có tiền tố đều tính từ `<root>`, và mọi lệnh Git chạy dạng `git -C <root>`.
`AGENTS.md` của repo sản phẩm không được nạp tự động khi thư mục hiện tại nằm ở nơi khác, nên mỗi skill đọc `<root>/AGENTS.md` trước câu hỏi đầu tiên, gồm cả các dòng Conventions về ngôn ngữ và múi giờ.
`/build:update` là ngoại lệ: vì chạy lặp lại nhiều lần, nó luôn hỏi lại ngôn ngữ hội thoại cho mỗi lượt chạy có người, và chỉ đọc dòng Conventions khi chạy không tương tác.

## Cấu trúc repo lớn

Có hai chế độ khởi tạo.
`new` dùng khi sản phẩm chưa có dòng code nào và tạo toàn bộ layout trong repo sản phẩm mới.
`restructure` dùng khi app hoặc code đã tồn tại và bọc layout canonical quanh cấu trúc đó mà không di chuyển code.

Cây sau gồm cả bộ skill lẫn repo sản phẩm, để hai vùng nằm cạnh nhau trong cùng một hình và trả lời rõ câu hỏi bộ skill nằm đâu so với repo sản phẩm.
Bộ skill chỉ hiện dưới dạng một dòng gập lại; chi tiết bên trong nó nằm ở mục Cài đặt bên dưới.

Quy ước đánh dấu:

- Không đánh dấu: `/build:start-repo` tạo ngay.
- Đánh dấu `+`: chuỗi sinh dần ở các bước sau, kèm tên lệnh sở hữu.

```
<workspace>/                          thư mục chứa cả hai, ví dụ ~/Developer
├── product-building-agents/          bộ skill, ngang hàng với repo sản phẩm
│
└── <product-repo>/                   repo sản phẩm do /build:start-repo tạo hoặc bọc lại
    ├── AGENTS.md                     commands, conventions, definition of done
    ├── CLAUDE.md                     pointer mỏng về AGENTS.md
    ├── app/                          code production chạy thật
    │   └── knowledge-base/           kiến thức runtime, agent chỉ đọc
    ├── client-note/                  tiếng nói khách hàng nguyên văn, chỉ đọc
    ├── prd/
    │   ├── README.md                  nguồn thông tin ngoài: GitHub, Notion
    │   ├── roadmap.md                tiến độ sáu bước và out of scope
    │   ├── evals/checklist.md        ship checklist và quality bar riêng
    │   ├── concept.md              + /build:idea-to-product-concept
    │   ├── PRD.md                  + /build:to-prd
    │   ├── architecture.md         + /build:to-prd
    │   ├── adr/NNNN-<slug>.md      + /build:prototype và /build:to-prd
    │   ├── tickets/NN-<slug>.md    + /build:to-ticket
    │   └── evals/cases.md, results.md  + /build:evals-gate
    ├── demos/
    │   └── prototypes/<slug>/      + /build:prototype, throwaway
    ├── routines/                     định nghĩa công việc lặp
    │   └── update-roadmap.md       + /build:start-repo hoặc /build:update sau khi duyệt
    └── report/
        └── product/                  báo cáo có ngày từ routine
```

Với `restructure` ở nhánh folder riêng, app đang chạy giữ nguyên repo và được liên kết vào vai trò canonical như sau.

```
<workspace>/
├── product-building-agents/
├── <app-repo>/                       app có sẵn, giữ nguyên cấu trúc và .git
└── <product-repo>/                   repo sản phẩm mới, có .git riêng
    ├── AGENTS.md
    ├── app -> ../<app-repo>/
    ├── client-note/
    ├── prd/
    ├── demos/
    ├── routines/
    └── report/product/
```

Trong `restructure` tại chỗ, chính app repo là gốc sản phẩm và `AGENTS.md` ghi `app-dir` thật như `src/` hoặc `apps/web/`.
Trong nhánh folder riêng, repo sản phẩm và app repo có `.git` riêng.
Một bộ skill phục vụ nhiều repo sản phẩm; không copy bộ skill vào repo sản phẩm.
`client-note/` và `app/knowledge-base/` chỉ đọc đối với agent; app sở hữu và ghi nội dung runtime.
Khi `app/` là symlink, `/build:start-repo` không tạo `app/knowledge-base/` và để lại TODO cho `/build:to-prd` quyết định từ kiến trúc.
`/build:start-repo` không bao giờ ghi đè file đã tồn tại.
Write policy chi tiết nằm ở `skills/start-repo/REPO-LAYOUT.md`.

## Cài đặt

Bộ này cài dưới dạng plugin, và đó là đường cài duy nhất.
Mười skill đều nằm trong `skills/`, tức đúng thư mục Claude Code quét mặc định, nên `.claude-plugin/plugin.json` không cần liệt kê từng skill.

Nguồn chính thức là repo Git <https://github.com/manhphanxiii/product-build-plugin>.
Chạy trong Claude Code:

```
/plugin marketplace add manhphanxiii/product-build-plugin
/plugin install build@manhphanxiii
```

Nếu bản tóm tắt cài đặt báo `Run /reload-plugins to activate.` thì chạy lệnh đó.

Cài bằng nguồn Git, không cài bằng đường dẫn thư mục local.
Marketplace kiểu `directory` chỉ tồn tại trên đúng một máy, nên mọi session ở nơi khác - cloud session của Claude Code, máy thứ hai, đồng đội - sẽ báo `Unknown command: /build:update` vì không thấy plugin.
Repo đang để private, nên môi trường nào cần cài cũng phải có GitHub credential đọc được nó.

Plugin tên `build`, nên mọi skill đều có tiền tố `build:`: `/build:start-repo`, `/build:prototype`, `/build:update`.
Kiểm tra bằng `claude plugin details build`, phải thấy đủ mười skill.

Sau khi cài, chạy `/build:start-repo` và cung cấp đường dẫn repo sản phẩm; lệnh sẽ tạo folder và khởi tạo Git sau khi bạn duyệt đề xuất.
Không copy bộ skill vào repo sản phẩm.

`skills/lavish/` là skill của bên thứ ba, giấy phép MIT, tác giả Kun Chen, nguồn <https://github.com/kunchenguid/lavish-axi>.
Nó chỉ gồm một file `SKILL.md`; CLI thật được tải runtime qua `npx -y lavish-axi`, nên bước này cần mạng.
