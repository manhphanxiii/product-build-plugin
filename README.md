# Product Build Plugin

Đây là một bộ skill độc lập dẫn sản phẩm từ ý tưởng đến code đã qua cổng ship.
Chuỗi tạo ra app chạy được thật trong vai trò canonical `app/` và ghi mọi quyết định thành artifact theo cấu trúc repo lớn.
Mỗi bước chính dùng một context window riêng và để lại bằng chứng trong repo sản phẩm.

## Bản đồ chuỗi

Bảng dùng cú pháp canonical của Claude Code.
Trên Codex universal plugin, đọc `/build:<skill>` thành `$build:<skill>`; với fallback standalone, đọc thành `$<skill>`; và đọc `/clear` thành mở conversation mới.

| Bước | Lệnh | Kết quả |
|---|---|---|
| 1 | `/build:start-repo` | Hỏi và soi repo sản phẩm, dựng một plan đầy đủ để duyệt một lần, rồi chạy liền mạch việc tạo workspace, ghi cấu hình, tạo roadmap, publish GitHub khi chưa có remote và kích hoạt morning brief theo lựa chọn đã duyệt |
| 2 | `/build:idea-to-product-concept` | Phân tích tư liệu, phỏng vấn và ghi `prd/concept.md` với workflow, story map và các điểm HITL |
| 3 | `/build:prototype` | Chạy spike để chốt quyết định và ghi ADR |
| 4 | `/build:to-prd` | Ghi `prd/PRD.md`, `prd/architecture.md` và hoàn tất ADR |
| 5 | `/build:to-ticket` | Chia kế hoạch thành ticket vertical slice |
| 6 | `/build:implement` | Làm một ticket trong `app/`, review và commit |
| 7 | `/build:evals-gate` | Chạy eval và chặn ship nếu chưa đạt ngưỡng |
| Lặp lại | `/build:update` | Hỏi ngôn ngữ hội thoại rồi in báo cáo ba phần: cập nhật roadmap, current task, note |
| Nội bộ | `/build:review-code` | Review diff theo Spec và Standards, thường do `/build:implement` gọi |
| Nội bộ | `/build:lavish` | Bề mặt review mặc định khi browser nhìn thấy local server; Artifact hoặc Markdown là fallback theo capability hiện có |

Chạy `/clear` giữa các bước chính và giữa mỗi ticket ở bước 6.
Sau bước 1, chạy `/build:update` để làm tươi tiến độ và biết đúng một lệnh tiếp theo.
Mỗi bước chính, kể cả `/build:update`, kết thúc bằng cách nêu tên lệnh tiếp theo và hỏi có muốn tiếp tục ngay không, không kết thúc im lặng.

## Cổng plan

`/build:start-repo` có một cổng plan duy nhất trước mọi thao tác ghi.
Skill gom toàn bộ kết quả khảo sát, role mapping, lệnh scaffold, file sẽ tạo, phương án GitHub và cơ chế morning brief vào một plan để người dùng sửa và duyệt một lần.
Sau khi plan được duyệt, các phase thực thi chạy liền mạch; chỉ chốt quét secret trước khi stage và câu hỏi bàn giao cuối cùng mới có thể dừng luồng.
Cổng dùng cùng probe bề mặt Lavish, Artifact, rồi Markdown như cổng review tài liệu.
Plan mode của host có thể chặn bước render hoặc local server của Lavish; khi đó skill báo bề mặt thay thế và hạ xuống Artifact hoặc Markdown mà vẫn giữ nguyên cổng duyệt trước write.

## Cổng review tài liệu

Sáu skill có cổng review dựng bản nháp đầy đủ, đưa lên bề mặt review và chỉ ghi artifact sau khi người dùng duyệt.
Tùy skill, artifact đã duyệt nằm trong `prd/`, `demos/prototypes/`, `routines/` hoặc `report/product/`; demo được thăng cấp có thể nằm tại `demos/<name>/`.
Lavish là bề mặt mặc định khi CLI chạy được và browser mở được local server.
Khi Lavish không dùng được, cổng chọn Artifact nếu cả Artifact tool lẫn `artifact-design` có mặt.
Nếu hai bề mặt đó đều không dùng được, bản nháp được in bằng Markdown trong hội thoại để duyệt.
Một Codex Cloud task do người dùng khởi tạo vẫn là tương tác qua nhiều lượt: run đầu dừng trước khi ghi file, và follow-up duyệt mới cho phép ghi.
Chỉ automation thật sự không có người duyệt mới bỏ qua cổng để routine không bị treo.

## Chạy chuỗi từ đâu

Sau khi cài plugin trên host đang dùng, gọi lệnh từ bất kỳ đâu; không cần mở repo này.
Repo này chỉ là nguồn của bộ skill, không phải nơi chứa artifact, và không bao giờ là repo sản phẩm.
Mỗi skill tự giải `<root>` là repo sản phẩm: dùng đường dẫn bạn cung cấp, nếu không có thì lấy git root của thư mục hiện tại.
`<root>` chỉ hợp lệ khi tồn tại `<root>/prd/roadmap.md`, và repo bộ skill này không bao giờ là `<root>`.
Root không hợp lệ thì skill in đường dẫn đã giải, nêu lý do, rồi hỏi một câu về đường dẫn repo sản phẩm; nó không bao giờ tự tạo `prd/`, `app/` hay `demos/` trong repo bộ skill.
Mọi path trong skill không có tiền tố đều tính từ `<root>`, và mọi lệnh Git chạy dạng `git -C <root>`.
`AGENTS.md` của repo sản phẩm không được nạp tự động khi thư mục hiện tại nằm ở nơi khác, nên các skill downstream đọc `<root>/AGENTS.md` sau khi xác nhận root và trước câu hỏi sản phẩm hoặc lần ghi đầu tiên.
`/build:start-repo` là ngoại lệ vì nó tạo hoặc hoàn thiện file này trong lúc khởi tạo.
`/build:update` hỏi lại ngôn ngữ hội thoại trước khi resolve root trong mỗi lượt chạy có người; khi chạy không tương tác, nó đọc ngôn ngữ và múi giờ từ Conventions trong `<root>/AGENTS.md`.

## Cấu trúc repo lớn

Có hai chế độ khởi tạo.
`new` dùng khi sản phẩm chưa có dòng code nào và tạo toàn bộ layout trong repo sản phẩm mới.
`restructure` dùng khi app hoặc code đã tồn tại và bọc layout canonical quanh cấu trúc đó mà không di chuyển code.
Trong chế độ `new` trên cloud session, publish repo lên GitHub là cách duy nhất để workspace sống sót sau khi session kết thúc, đồng thời là điều kiện để dùng `/schedule`.

Cây sau gồm cả bộ skill lẫn repo sản phẩm, để hai vùng nằm cạnh nhau trong cùng một hình và trả lời rõ câu hỏi bộ skill nằm đâu so với repo sản phẩm.
Bộ skill chỉ hiện dưới dạng một dòng gập lại; chi tiết bên trong nó nằm ở mục Cài đặt bên dưới.

Quy ước đánh dấu:

- Không đánh dấu: `/build:start-repo` tạo ngay.
- Đánh dấu `+`: chuỗi sinh dần ở các bước sau, kèm tên lệnh sở hữu.

Scaffold tạo README mô tả cho các destination mới và seed `prd/README.md` từ template; cây dưới đây lược bỏ các file đó để dễ đọc.

```
<workspace>/                          thư mục chứa cả hai, ví dụ ~/Developer
├── product-build-plugin/             bộ skill, ngang hàng với repo sản phẩm
│
└── <product-repo>/                   repo sản phẩm do /build:start-repo tạo hoặc bọc lại
    ├── AGENTS.md                     commands, conventions, definition of done
    ├── CLAUDE.md                     pointer mỏng về AGENTS.md
    ├── .claude/settings.json         khai báo marketplace để session khác thấy `/build:*`
    ├── app/                          code production chạy thật
    │   └── knowledge-base/           kiến thức runtime, agent chỉ đọc
    ├── client-note/                  tiếng nói khách hàng nguyên văn, chỉ đọc
    ├── prd/
    │   ├── README.md                 nguồn thông tin ngoài: GitHub, Notion
    │   ├── roadmap.md                tiến độ bảy bước và out of scope
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
    │   ├── weekly-ops-review.md      routine review vận hành hàng tuần
    │   ├── pr-auto-review.md         routine tự động review pull request
    │   └── update-roadmap.md       + /build:start-repo hoặc /build:update sau khi duyệt
    └── report/
        └── product/                  báo cáo có ngày từ routine
```

Với `restructure` ở nhánh folder riêng, app đang chạy giữ nguyên repo và được liên kết vào vai trò canonical như sau.

```
<workspace>/
├── product-build-plugin/
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

Trong `restructure` tại chỗ, `start-repo` có thể ghi `app-dir` thật như `src/` hoặc `apps/web/` vào `AGENTS.md` và không tạo `app/` mới.
Đây chưa phải luồng end-to-end hoàn chỉnh: `implement` hiện chỉ ghi production code dưới `<root>/app/`, nên không chạy bước 6 trên layout này nếu `<root>/app/` không tồn tại.
Trong nhánh folder riêng, repo sản phẩm và app repo có `.git` riêng.
Một bộ skill phục vụ nhiều repo sản phẩm; không copy bộ skill vào repo sản phẩm.
`client-note/` và `app/knowledge-base/` chỉ đọc đối với agent; app sở hữu và ghi nội dung runtime.
Khi `app/` là symlink, `/build:start-repo` không tạo `app/knowledge-base/` và để lại TODO cho `/build:to-prd` quyết định từ kiến trúc.
Scaffold của `/build:start-repo` không ghi đè file đã tồn tại.
Workflow chỉ patch, thu gọn hoặc migrate file hiện hữu khi thay đổi cụ thể đã được trình bày và người dùng duyệt.
Write policy chi tiết nằm ở `skills/start-repo/REPO-LAYOUT.md`.

## Cài đặt

Nguồn chính thức là repo public <https://github.com/manhphanxiii/product-build-plugin>.
Claude Code plugin là distribution production hiện có.
Codex universal plugin đang ở giai đoạn chuẩn bị manifest, validation, smoke test và publication; standalone installer là fallback cho development và pre-publication cloud testing.
Mười skill nằm trong `skills/`; Claude tự discover thư mục này, còn manifest Codex khai báo `"skills": "./skills/"`.

### Claude Code

Chạy trong Claude Code:

```
/plugin marketplace add manhphanxiii/product-build-plugin
/plugin install build@manhphanxiii
```

Nếu bản tóm tắt cài đặt báo `Run /reload-plugins to activate.` thì chạy lệnh đó.

Cài bằng nguồn Git, không cài bằng đường dẫn thư mục local.
Marketplace kiểu `directory` chỉ tồn tại trên đúng một máy, nên mọi session ở nơi khác - cloud session của Claude Code, máy thứ hai, đồng đội - sẽ báo `Unknown command: /build:update` vì không thấy plugin.

Plugin tên `build`, nên mọi skill đều có tiền tố `build:`: `/build:start-repo`, `/build:prototype`, `/build:update`.
Kiểm tra bằng `claude plugin details build`, phải thấy đủ mười skill.

### Codex universal plugin đang chuẩn bị publication

Manifest nằm tại `.codex-plugin/plugin.json` và dùng cùng tên, version, mô tả, tác giả, repository, license với manifest Claude.
Trong giai đoạn local development, đưa checkout vào personal marketplace bằng `$plugin-creator`, validate plugin, cài lại bằng `codex plugin add build@<marketplace>`, rồi mở conversation mới để test.
Không sửa tay personal `marketplace.json` hoặc `config.toml` trong update loop.

Codex universal chưa được README này tuyên bố là production-ready.
Sau khi plugin được duyệt trong universal directory và vượt qua smoke test, cài `build` từ plugin directory của Codex.
Các selector production dự kiến là `$build:start-repo`, `$build:prototype`, `$build:update`; smoke test release phải xác nhận namespace này trước khi công bố hỗ trợ.

### Codex Cloud fallback trước publication

Fallback standalone chỉ dùng khi universal plugin chưa được publish hoặc workspace chưa surfacing plugin.
Nó từ chối tạo skill trùng khi phát hiện universal plugin đã cài, preflight toàn bộ collision, và không ghi đè entry không thuộc installer.

Setup script cho release `v2.4.0`, sau khi tag này được publish:

```bash
git clone --branch v2.4.0 --depth 1 https://github.com/manhphanxiii/product-build-plugin.git "$HOME/.agents/product-build-plugin"
bash "$HOME/.agents/product-build-plugin/scripts/install-codex.sh" --ref v2.4.0
```

Maintenance script giữ nguyên release đã pin và fail rõ nếu source không còn khớp:

```bash
git -C "$HOME/.agents/product-build-plugin" fetch --tags origin
git -C "$HOME/.agents/product-build-plugin" checkout --detach v2.4.0
bash "$HOME/.agents/product-build-plugin/scripts/install-codex.sh" --ref v2.4.0
```

Codex Cloud chạy setup trước agent với internet access.
Lệnh `export` trong setup shell không persist sang agent; đặt biến cần persist trong environment settings hoặc shell startup file.
Container cache có thể resume với maintenance script, nên không kéo `main` và không tự đổi release channel.

### Fallback local và kiểm tra

Từ checkout hiện tại, cài symlink standalone:

```bash
bash scripts/install-codex.sh --dry-run
bash scripts/install-codex.sh
```

Dùng `--copy` khi symlink không phù hợp, và dùng `--uninstall` để gỡ đúng các entry installer quản lý.
Sau khi cài fallback, mở `/skills` hoặc gõ `$` và xác nhận đủ mười skill không namespace.
Không cài fallback cùng universal plugin trong cùng profile.

Trước release, chạy:

```bash
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

Ma trận release bắt buộc:

| Host | Smoke test | Tiêu chí pass |
|---|---|---|
| Claude Code | Cài từ Git marketplace và chạy `claude plugin details build` | Đủ mười skill |
| Claude Code | `/build:start-repo` rồi `/build:update` trên scratch product repo | Plan gate chặn mọi write tới khi duyệt, scaffold dùng `<skill_dir>` và chọn đúng review surface |
| Codex CLI plugin | Cài `build@<marketplace>` và mở conversation mới | Đủ mười skill dưới namespace `build`, explicit và implicit policy đúng |
| Codex CLI fallback | Chạy installer bằng HOME test hoặc `--dest` tạm | Symlink, copy, collision, rerun, stale cleanup và uninstall đều pass |
| Codex Cloud | Chạy `$build:update` trong environment có plugin | Markdown review dừng trước write và follow-up approval mới ghi |
| Cả hai | Chạy checker, unit tests và plugin validator | Tất cả exit 0 |

Release chỉ được công bố sau khi toàn bộ ma trận pass.
Tag phải khớp version trong cả hai manifest; submit cùng artifact đã smoke test vào universal directory.
Nếu smoke test sau publish thất bại, quay lại plugin version đã pass gần nhất và giữ README ở trạng thái chưa hỗ trợ version lỗi.

Sau khi cài trên host tương ứng, chạy `/build:start-repo` hoặc `$build:start-repo` và cung cấp đường dẫn repo sản phẩm; lệnh chỉ scaffold sau khi bạn duyệt đề xuất.
Không copy bộ skill vào repo sản phẩm.

`skills/lavish/` là skill của bên thứ ba, giấy phép MIT, tác giả Kun Chen, nguồn <https://github.com/kunchenguid/lavish-axi>.
`SKILL.md` là nội dung vendored duy nhất; `agents/openai.yaml` chỉ thêm metadata giao diện của plugin.
CLI thật được tải runtime qua `npx -y lavish-axi`, nên bước này cần mạng.
