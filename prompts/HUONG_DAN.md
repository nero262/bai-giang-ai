# Hướng dẫn — Tạo và bổ sung bài giảng mới

Tài liệu này hướng dẫn từng bước để tạo một bài giảng mới và thêm vào repo,
phù hợp cả với người không code.

## Tổng quan workflow

```
[1] Chuẩn bị nội dung → [2] Dùng Claude/ChatGPT tạo HTML → [3] Lưu vào slides/
                                                          ↓
[6] Verify trên trình duyệt ← [5] Restart server ← [4] Cập nhật lessons.json
```

## Bước 1 — Chuẩn bị nội dung

Trước khi bấm prompt, hãy có sẵn:

- Số thứ tự bài: `Buổi 2`, `Buổi 3`, …
- Tiêu đề bài giảng (ngắn gọn, ≤ 10 chữ).
- Mục tiêu cuối buổi: 3–5 điều học sinh phải có/làm được.
- Nội dung lý thuyết: bạn có thể paste từ sách, từ notes, hoặc viết dàn ý.
- Bài tập tương tác: muốn có quiz? drag-drop? flashcard?
- Bài tập về nhà cho buổi tiếp theo.

## Bước 2 — Dùng AI để tạo HTML

1. Mở [`lesson_template_prompt.md`](./lesson_template_prompt.md).
2. Copy toàn bộ nội dung của file.
3. Mở Claude (claude.ai), ChatGPT, hoặc Gemini.
4. Dán prompt vào, thay thế các phần `<<< ... >>>` bằng nội dung của bạn.
5. AI sẽ trả về:
   - Một file HTML hoàn chỉnh.
   - Một block JSON cho `lessons.json`.

**Mẹo:** Nếu AI cắt giữa chừng (truncated), nhắn lại
*"Hãy tiếp tục từ dòng cuối cùng, không lặp lại"*.

## Bước 3 — Lưu file HTML

Lưu file HTML AI trả về vào thư mục `slides/`, đặt tên theo
quy ước:

```
slides/buoi_02.html
slides/buoi_03.html
...
```

Tên file phải khớp với `slug` (`buoi_02` → `buoi_02.html`).

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

## Bước 5 — Restart server

```bash
# Nếu đang dev local
Ctrl+C trên terminal đang chạy `make dev`, rồi:
make dev

# Nếu chạy Docker
make restart
```

## Bước 6 — Verify

1. Mở `http://localhost:8000` — bài mới phải xuất hiện và bấm mở được.
2. Click "Mở bài giảng" để vào slide.
3. Kiểm tra:
   - Slide hiển thị đúng, không lệch layout.
   - Nút prev/next hoạt động.
   - Quiz/Drag-drop chạy được.
   - Sổ Tay lưu được vào `localStorage` (mở DevTools → Application → Local Storage).

## Checklist trước khi commit

- [ ] File HTML nằm đúng trong `slides/`.
- [ ] Tên file khớp `slug` trong `lessons.json`.
- [ ] `"available": true`.
- [ ] Mở bài giảng trên Chrome, Firefox, Edge đều hiển thị tốt.
- [ ] Resize cửa sổ — slide co giãn mượt.
- [ ] Không có lỗi `Console` trong DevTools.
- [ ] Câu chữ rà soát đúng chính tả tiếng Việt.

## Lỗi thường gặp

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| 404 khi mở bài | `slug` không khớp tên file | Đổi `file` hoặc đổi tên file |
| Bài không xuất hiện trên trang chủ | `"available": false` | Sửa thành `true` |
| Slide không trượt qua | Lỗi JS — quên copy đoạn `<script>` | Mở DevTools console xem lỗi |
| Sổ Tay không lưu | `STORAGE_KEY` trùng với bài khác | Đổi key (`BAI_GIANG_B2_NOTEBOOK`...) |
| Layout vỡ trên di động | Quên `viewport` meta | Đảm bảo dòng `<meta name="viewport"...>` |

## Mẹo cho người mới

- **Test prompt trước trên 1 buổi nhỏ** để hiệu chỉnh, sau đó áp dụng hàng loạt.
- **Lưu prompt đã chỉnh** vào file riêng để dùng lại — đỡ phải edit lại
  template gốc mỗi lần.
- **So sánh bài mới với `buoi_01.html`** — đây là chuẩn vàng cho phong cách.
- Nếu cần slide có **video YouTube embed**, dùng class `.video-frame > iframe`
  (đã có sẵn trong CSS của bài mẫu).
