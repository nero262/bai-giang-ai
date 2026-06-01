# Prompt mẫu — Tạo bài giảng mới cho khóa AI 24 buổi

Dán nguyên prompt bên dưới vào Claude / ChatGPT / Gemini. Thay phần
`<<< ... >>>` bằng nội dung cụ thể của bài bạn muốn tạo.

> **Quan trọng — kiến trúc mới (06/2026):** mỗi file `slides/buoi_XX.html`
> KHÔNG còn là HTML hoàn chỉnh nữa. Nó là một **fragment**: chỉ chứa nội dung
> slide. Phần khung (sidebar, top-bar, slide engine, Sổ Tay overlay, nav prev/next,
> quiz/checklist/drag-drop handler) đã được template `frontend/templates/lesson.html`
> cung cấp tự động. Khi bài giảng mới thêm vào `lessons.json`, nó liên kết với
> template đó và xuất hiện trên cả sidebar lẫn URL `/lesson/buoi_XX`.

---

## PROMPT

Bạn là một **Senior Lesson Designer** chuyên tạo bài giảng AI tương tác cho học
sinh lớp 8 và lớp 12 ở Việt Nam. Hãy tạo cho tôi một **slide fragment HTML**
tuân theo đúng phong cách, cấu trúc và component đã được chuẩn hóa của khóa học.

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

### Format đầu ra — FRAGMENT (KHÔNG phải HTML đầy đủ)

File trả về **KHÔNG có** `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`, `<aside class="sidebar">`,
`<div class="top-bar">`, `<div class="nav-bar">`, `<div class="nb-overlay">`, không có
SlideEngine, không có handler quiz/checklist/drag-drop. Tất cả những thứ đó được
template `frontend/templates/lesson.html` cung cấp.

File chỉ chứa, theo đúng thứ tự:

1. **Header comment** ghi rõ buổi.
2. **Cấu hình Sổ Tay** dạng JSON nhúng (BẮT BUỘC nếu buổi có Sổ Tay):

   ```html
   <script type="application/json" id="nb-questions">
   {
     "1": {"title": "SỔ TAY #1 — Đầu buổi", "q": "Câu hỏi đầu buổi"},
     "2": {"title": "SỔ TAY #2 — ...", "q": "Câu hỏi giữa buổi"},
     "3": {"title": "SỔ TAY #3 — ...", "q": "..."},
     "4": {"title": "SỔ TAY #4 — Cuối buổi", "q": "Câu hỏi cuối buổi"}
   }
   </script>
   ```
   Key `"1"`, `"2"`, … phải khớp với `data-nb-id` của các `<textarea class="nb-input">`
   trong slide.

3. **(Tuỳ chọn) `<style>` cho CSS riêng của buổi.** Chỉ thêm nếu bài có
   layout đặc thù — phần lớn class chuẩn (qbox, card, quiz, fc, hl-box,
   steps, timeline, modmap, school-card, met-card, brand-card, school-flip,
   agent-flip, prompt-box, cl-item, draggable, bucket) đã có sẵn trong template.

4. **Các `<section class="slide ...">`** — nội dung từng slide. Slide ĐẦU TIÊN
   phải có thêm class `active`:

   ```html
   <section class="slide active slide-cover" data-slide="1" data-title="Chào mừng">
     <div class="cover-orb orb-1"></div><div class="cover-orb orb-2"></div><div class="cover-orb orb-3"></div>
     <div class="cover-content slide-body">
       <span class="eyebrow">BUỔI X · MODULE Y — TÊN MODULE</span>
       <h1 class="hero-title">Tiêu đề <span class="grad-text">nổi bật</span></h1>
       <p class="slide-subtitle">Mô tả ngắn buổi học.</p>
       <div class="cover-chips"><span class="cover-chip">Thời lượng</span><span class="cover-chip">Chủ đề</span></div>
     </div>
   </section>
   ```

5. **(Tuỳ chọn) `<script>` cho JS riêng của buổi.** Chỉ thêm nếu bài có
   tương tác đặc thù không nằm trong template (ví dụ animation custom).
   KHÔNG được redefine `SlideEngine`, `openNotebook`, `submitNotebook`,
   `initChecklist`, `initGame`, `restartGame` — chúng đã có trong template.

### Yêu cầu bắt buộc về thiết kế

1. **Palette:** Modern Tech — Blue (`#2563EB`) + Slate. Tránh tím/hồng.
   Dùng đúng các biến CSS đã chuẩn (`--primary`, `--surface-alt`,
   `--box-blue/yellow/purple/orange`, v.v.).
2. **Layout chỉ trong vùng slide:** mỗi slide có một `<div class="slide-body">`
   chứa `eyebrow`, `slide-title` (hoặc `hero-title`), `slide-subtitle`,
   rồi đến component nội dung.
3. **Typography:** font `Be Vietnam Pro`, mono `JetBrains Mono` đã load ở template.
4. **Component chuẩn (có sẵn CSS trong template):**
   - `.qbox.qbox-blue` — Trước giờ học (icon `?`)
   - `.qbox.qbox-yellow` — Hỏi bạn cặp (icon `!`)
   - `.qbox.qbox-purple` — Sổ Tay Cá Nhân (icon `#`, kèm `.nb-input-wrap` + `<textarea class="nb-input" data-nb-id="N">`)
   - `.qbox.qbox-orange` — Thử AI tại nhà (icon `+`)
   - `.card-grid` + `.card` — grid card đều chiều cao
   - `.quiz` với `data-correct="0"` và `data-explanation="..."` + các `.quiz-opt` có `data-index="0..3"` + 1 `<div class="quiz-fb"></div>`
   - `.fc` (flashcard) với `.fc-inner > .fc-front + .fc-back` — template tự gán click-to-flip
   - `.draggable[draggable="true"][data-type][data-label]` + `.bucket[data-bucket]` — template tự bind game
   - `.cl-item` checklist — template tự bind, tự lưu vào localStorage
   - `.steps`, `.timeline`, `.modmap`, `.school-flip`, `.agent-flip`, `.prompt-box`, `.hl-box.success/info/danger`, `.met-card`, `.brand-card`, `.docfig`
5. **Số lượng slide:** 25–45 tùy độ phức tạp. Tối thiểu phải có:
   - 1 slide cover mở đầu
   - Slide nội dung chính
   - Slide tương tác (quiz, drag-drop hoặc flashcard)
   - Slide sổ tay đầu buổi + cuối buổi (nếu có Sổ Tay)
   - 1 slide cover kết thúc
6. **Câu chữ:** xưng "em" với học sinh, "GV" với giáo viên. Câu ngắn, rõ.
   Dùng thống nhất "khóa" (không phải "khoá").

### Output

Trả về cho tôi:

1. **File fragment HTML** (bắt đầu bằng comment `<!-- Slide fragment cho Buổi X -->`,
   KHÔNG có `<!DOCTYPE>` hay `<html>`). Lưu thành `slides/buoi_XX.html`.
2. **Một block JSON** để thêm vào `slides/lessons.json`:

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

Sau khi lưu file + cập nhật `lessons.json` + restart server, URL `/lesson/buoi_XX`
sẽ tự động render bài mới bên trong template với sidebar đã có entry tương ứng.

Bắt đầu tạo bài giảng theo đúng yêu cầu trên.
