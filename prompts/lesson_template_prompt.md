# Prompt mẫu — Tạo bài giảng mới cho khóa AI 24 buổi

Dán nguyên prompt bên dưới vào Claude / ChatGPT / Gemini. Thay phần
`<<< ... >>>` bằng nội dung cụ thể của bài bạn muốn tạo.

---

## PROMPT

Bạn là một **Senior Lesson Designer** chuyên tạo bài giảng AI tương tác cho học
sinh lớp 8 và lớp 12 ở Việt Nam. Hãy tạo cho tôi một bài giảng HTML hoàn chỉnh,
self-contained (CSS + JS inline trong một file), tuân theo đúng phong cách,
cấu trúc và component đã được chuẩn hóa của khóa học.

### Thông tin bài giảng cần tạo

- **Số buổi:** `<<< Ví dụ: Buổi 2 >>>`
- **Tiêu đề bài giảng:** `<<< Ví dụ: Prompt Engineering — RCTFE >>>`
- **Module:** `<<< Ví dụ: M1 · Nền tảng AI >>>`
- **Thời lượng:** `<<< Ví dụ: 120 phút >>>`
- **Mục tiêu học tập (output em phải có cuối buổi):**
  1. `<<< Output 1 >>>`
  2. `<<< Output 2 >>>`
  3. `<<< Output 3 >>>`
- **Khái niệm cốt lõi cần dạy:** `<<< Liệt kê các khái niệm chính >>>`
- **Nội dung lý thuyết (tóm tắt):** `<<< Paste nội dung gốc, sách giáo khoa,
  hoặc dàn ý chi tiết ở đây >>>`
- **Hoạt động tương tác mong muốn** (chọn ít nhất 3): cover slide, qbox 4 màu
  (blue/yellow/purple/orange), card-grid, drag-drop game, compare table,
  flashcard, timeline, quiz có chấm điểm, checklist, sổ tay cá nhân, prompt-box.

### Yêu cầu bắt buộc về thiết kế

1. **Palette:** Modern Tech — Blue (`#2563EB`) + Slate. Tránh tím/hồng.
   Dùng đúng các biến CSS đã chuẩn (`--primary`, `--surface-alt`,
   `--box-blue/yellow/purple/orange`, v.v.).
2. **Layout:** Responsive fluid — slide co giãn theo cửa sổ trình duyệt.
   - Sidebar trái 280px liệt kê 24 buổi (bài hiện tại có `.active`,
     bài chưa có `.disabled`).
   - Top bar có badge `BUỔI X / 24`, nút "Sổ Tay Cá Nhân", nút "In".
   - Mỗi slide là một `<section class="slide" data-slide="N" data-title="...">`.
   - Phải có `.slide-cover` ở slide đầu và slide cuối.
3. **Typography:** font `Be Vietnam Pro`, mono `JetBrains Mono`. Hero title dùng
   `clamp(2rem, 5vw, 4rem)`. Letter-spacing và line-height theo file mẫu.
4. **Component chuẩn:**
   - `.qbox.qbox-blue` — Trước giờ học (icon `?`)
   - `.qbox.qbox-yellow` — Hỏi bạn cặp (icon `!`)
   - `.qbox.qbox-purple` — Sổ Tay Cá Nhân (icon `#`)
   - `.qbox.qbox-orange` — Thử AI tại nhà (icon `+`)
5. **JavaScript:**
   - `SlideEngine` — điều hướng prev/next bằng nút, phím mũi tên, swipe.
   - Quiz có data-correct và data-explanation, hiển thị feedback.
   - Sổ Tay lưu vào `localStorage` (key prefix `BAI_GIANG_BX_NOTEBOOK`,
     X là số buổi).
   - Checklist tick được, lưu trạng thái.
6. **Số lượng slide:** từ 25–45 tùy độ phức tạp. Tối thiểu phải có:
   - 1 slide cover mở đầu
   - 1 slide giới thiệu 4 loại câu hỏi (nếu là buổi đầu module)
   - Slide nội dung chính
   - Slide tương tác (quiz, drag-drop hoặc flashcard)
   - Slide sổ tay đầu buổi + cuối buổi
   - 1 slide cover kết thúc
7. **Câu chữ:** xưng "em" với học sinh, "GV" với giáo viên. Câu ngắn,
   rõ, không dùng tiếng lóng. Tránh trộn lẫn "khoá" và "khóa" — dùng
   thống nhất "khóa".

### Yêu cầu kỹ thuật

- Toàn bộ HTML phải là **MỘT FILE DUY NHẤT**, không reference external CSS/JS
  ngoài Google Fonts.
- File phải mở được bằng cách double-click (không cần server).
- Đảm bảo accessibility: alt text cho icon, `aria-label` cho nút điều hướng,
  focus-visible outline.
- Đặt tên class theo BEM-lite như file mẫu (`.qbox`, `.qbox-blue`, `.cl-item`,
  v.v.) để tương thích với các bài khác.

### Output

Trả về cho tôi:

1. File HTML hoàn chỉnh (bắt đầu bằng `<!DOCTYPE html>`, kết thúc bằng
   `</html>`).
2. Một block JSON ngắn để thêm vào `slides/lessons.json`:

   ```json
   {
     "id": <<<số>>>,
     "slug": "buoi_XX",
     "title": "<<<title>>>",
     "module": "<<<M1>>>",
     "module_name": "<<<Nền tảng AI>>>",
     "duration_min": 120,
     "file": "buoi_XX.html",
     "available": true,
     "description": "<<<mô tả ngắn 1–2 câu>>>",
     "tags": ["tag1", "tag2"]
   }
   ```

Bắt đầu tạo bài giảng theo đúng yêu cầu trên.
