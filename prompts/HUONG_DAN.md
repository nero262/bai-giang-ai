# Hướng dẫn — Tạo và bổ sung bài giảng mới

Tài liệu này hướng dẫn từng bước để tạo một bài giảng mới và thêm vào repo,
phù hợp cả với người không code.

## Tổng quan workflow

```
[1] Chuẩn bị nội dung → [2] Dùng Claude/ChatGPT tạo fragment → [3] Lưu vào slides/
                                                             ↓
[6] Verify trên trình duyệt ← [5] Build tĩnh / restart server ← [4] Cập nhật lessons.json
```

## Bước 1 — Chuẩn bị nội dung

Trước khi bấm prompt, hãy có sẵn:

- Số thứ tự bài: `Buổi 2`, `Buổi 3`, …
- Tiêu đề bài giảng (ngắn gọn, ≤ 10 chữ).
- Mục tiêu cuối buổi: 3–5 điều học sinh phải có/làm được.
- Nội dung lý thuyết: bạn có thể paste từ sách, từ notes, hoặc viết dàn ý.
- Bài tập tương tác: muốn có quiz? drag-drop? flashcard?
- Bài tập về nhà cho buổi tiếp theo.

## Bước 2 — Dùng AI để tạo fragment

1. Mở [`lesson_template_prompt.md`](./lesson_template_prompt.md).
2. Copy toàn bộ nội dung của file.
3. Mở Claude (claude.ai), ChatGPT, hoặc Gemini.
4. Dán prompt vào, thay thế các phần `<<< ... >>>` bằng nội dung của bạn.
5. AI sẽ trả về:
   - Một **fragment** (chỉ chứa `<section class="slide">`, cấu hình Sổ Tay
     `<script id="nb-questions">`, và css/js riêng nếu cần — **không** có
     `<html>`, sidebar hay slide-engine; những thứ đó nằm trong template chung).
   - Một block JSON cho `lessons.json`.

**Mẹo:** Nếu AI cắt giữa chừng (truncated), nhắn lại
*"Hãy tiếp tục từ dòng cuối cùng, không lặp lại"*.

## Bước 3 — Lưu fragment

Lưu fragment AI trả về vào thư mục `slides/`, đặt tên theo quy ước:

```
slides/buoi_02.html
slides/buoi_03.html
...
```

Tên file phải khớp với `slug` (`buoi_02` → `buoi_02.html`).

> Nếu lỡ tạo theo định dạng cũ (HTML đầy đủ), chạy
> `python scripts/migrate_slide_to_fragment.py slides/buoi_02.html` để chuyển
> sang fragment (tự backup bản gốc).

## Bước 4 — Cập nhật lessons.json

Mở `slides/lessons.json`. Tìm bài tương ứng và sửa `"available": false`
thành `"available": true`, đồng thời cập nhật `description` và `tags`:

```diff
 {
   "id": 2,
   "slug": "buoi_02",
   "title": "Prompt Engineering — RCTFE",
   ...
-  "available": false,
+  "available": true,
-  "description": "Khung RCTFE...",
+  "description": "Học framework RCTFE để hỏi AI hiệu quả. Có 5 case study.",
   "tags": ["prompt", "rctfe"]
 }
```

Nếu là bài hoàn toàn mới (vượt 24 buổi), copy một entry và sửa.

## Bước 5 — Build / Restart

**Bản tĩnh (GitHub Pages):**

```bash
make serve-static   # build → dist/ rồi xem thử tại http://127.0.0.1:8080
# hoặc chỉ build: make build-static
```

**Bản server (FastAPI):**

```bash
# Dev local: Ctrl+C terminal đang chạy `make dev`, rồi:
make dev
# Docker:
make restart
```

> Đẩy lên `main` thì GitHub Actions tự build + deploy bản tĩnh — không cần làm tay.

## Bước 6 — Verify

1. Mở trang chủ (`http://127.0.0.1:8080` bản tĩnh, hoặc `http://localhost:8000`
   bản server) — bài mới phải xuất hiện và bấm mở được.
2. Click "Mở bài giảng" để vào slide.
3. Kiểm tra:
   - Slide hiển thị đúng, không lệch layout.
   - Sidebar: module của bài mở sẵn, các module khác thu gọn (dropdown).
   - Nút prev/next + phím mũi tên hoạt động.
   - Quiz/Drag-drop/flashcard chạy được.
   - Sổ Tay hiện đúng câu hỏi (từ `nb-questions`) và lưu vào `localStorage`
     (DevTools → Application → Local Storage).

## Checklist trước khi commit

- [ ] Fragment nằm đúng trong `slides/`, **không** có `<html>`/sidebar/slide-engine.
- [ ] Tên file khớp `slug` trong `lessons.json`; `"available": true`.
- [ ] Có `<script id="nb-questions">` nếu bài dùng Sổ Tay; key khớp `data-nb-id`.
- [ ] `make build-static` chạy không lỗi và bài hiện trên trang chủ.
- [ ] Mở bài: slide trượt được, quiz/drag-drop/Sổ Tay hoạt động.
- [ ] Resize cửa sổ — slide co giãn mượt; không có lỗi `Console`.
- [ ] Câu chữ rà soát đúng chính tả tiếng Việt (xưng "em").

## Lỗi thường gặp

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| 404 / bài không mở (server) | `slug` không khớp tên file | Đổi `file` trong lessons.json hoặc đổi tên file |
| Bài không xuất hiện trên trang chủ | `"available": false` | Sửa thành `true` rồi build/restart lại |
| Trang trắng khi mở fragment trực tiếp | Fragment cần khung của template | Mở qua `/lesson/...` (server) hoặc bản build `dist/` — đừng mở thẳng file trong `slides/` |
| Slide không hiện | Quên class `slide` / thiếu `active` ở slide đầu | `<section class="slide active ...">` cho slide 1 |
| Sổ Tay trống | Thiếu `<script id="nb-questions">` hoặc key lệch `data-nb-id` | Khớp key JSON với `data-nb-id` của `<textarea>` |
| Sổ Tay không lưu | — | `STORAGE_KEY` tự sinh theo số buổi (`BAI_GIANG_B<id>_*`), không cần khai báo |

## Mẹo cho người mới

- **Test prompt trước trên 1 buổi nhỏ** để hiệu chỉnh, sau đó áp dụng hàng loạt.
- **Lưu prompt đã chỉnh** vào file riêng để dùng lại — đỡ phải edit lại
  template gốc mỗi lần.
- **So sánh fragment mới với `buoi_05.html`** — đây là fragment gọn nhất, chuẩn
  định dạng mới. (`buoi_01.html` là chuẩn vàng về phong cách nội dung.)
- Các class component (qbox, card, quiz, fc, hl-box, steps, timeline, met-card,
  school-flip, draggable/bucket, prompt-box…) **đã có sẵn** trong template chung —
  cứ dùng, không cần khai báo CSS lại.
- Nếu cần slide có **video YouTube embed**, dùng class `.video-frame > iframe`.
