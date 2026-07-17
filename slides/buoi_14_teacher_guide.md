# Hướng Dẫn Giảng Dạy & Timeline — Buổi 14

**Chủ đề:** Git & GitHub — Cỗ máy thời gian cho code (và AI làm trợ lý Git)
**Đối tượng:** Học sinh cấp 2-3 (đã học các buổi 1-13, quen dùng AI tạo sản phẩm và bước đầu đọc hiểu code).
**Mục tiêu cốt lõi:**
1. Hiểu Git như một **"cỗ máy thời gian / điểm lưu game (checkpoint)"** — không bao giờ mất code, kể cả khi AI viết đè lên bản đang chạy.
2. Phân biệt **Git (máy)** và **GitHub (đám mây)**; nắm vòng add → commit → push. **Biết tận dụng AI làm trợ lý Git** (giải thích, viết commit, chỉ đường, gỡ lỗi).
3. Tự tay tạo **1 repository công khai** có commit + README (kèm ảnh), **bật GitHub Pages để có link web sống**; biết tìm, đánh giá và tái dùng mã nguồn người khác **đúng license**.

> **SẢN PHẨM SHOW ĐƯỢC (APP-14.1):** cuối buổi mỗi em có **1 link web SỐNG (GitHub Pages)** — mở trên điện thoại là game/web chạy thật — cùng repo có commit rõ nghĩa + README có ảnh. Xuyên suốt buổi, em dùng **AI làm trợ lý Git**. Đây là viên gạch đầu tiên của Portfolio.

## CHUẨN BỊ TRƯỚC BUỔI HỌC (GV đọc kỹ)
> **Slide 2 trong bài chính là "Chuẩn bị trước buổi học"** — GV dùng nó để điểm danh nhanh 4 thứ dưới đây ngay đầu giờ.
- **Tài khoản GitHub:** nhắc HS đăng ký trước ở nhà bằng Gmail. HS **dưới 16 tuổi** cần đăng ký cùng phụ huynh — GV chuẩn bị **phương án dự phòng**: 1-2 tài khoản lớp dùng chung, hoặc dùng nút Upload trên web (không cần terminal).
- **Sản phẩm để đưa lên:** mỗi HS mang theo 1 game/web nhỏ (file HTML) đã làm (BTVN buổi 13, hoặc sản phẩm buổi 3, 4, 11).
- **Máy cài sẵn Git + IDE code:** máy đã cài **Git** và một **IDE/công cụ code** (Antigravity, Codex hoặc OpenCode — đã dùng từ buổi 11-12) để sửa code, commit, đẩy lên GitHub. (Bản cơ bản chỉ dùng nút Upload trên web thì chưa bắt buộc.)
- **Công cụ AI + Mạng:** có sẵn 1 công cụ AI (ChatGPT/Gemini/Claude) để làm "trợ lý Git"; máy tính + wifi cho phần thực hành.

---

## TIMELINE CHI TIẾT (120 PHÚT)

*Nguyên tắc: cứ ~10 phút lý thuyết là chèn 1 hoạt động (4 màu: xanh Quiz · vàng Thảo luận cặp · cam Thực hành máy · tím Sổ Tay). GV giới thiệu ý nghĩa 4 màu khi HS gặp hộp màu đầu tiên — bài đã bỏ slide chú thích màu riêng, thay bằng slide "Chuẩn bị".*

### 1. Khởi động & Kích hoạt "Nỗi đau" (00:00 - 00:12) — Slide 1-5
- **Slide 2 — Chuẩn bị:** điểm danh nhanh 4 thứ (tài khoản GitHub, sản phẩm HTML, máy có Git + IDE code, công cụ AI). Ai thiếu → dùng phương án dự phòng (tài khoản lớp / nút Upload).
- **Speaker Notes (TED-style, Slide 5):** *"Giơ tay: bao nhiêu bạn từng bảo AI 'sửa giúp một chỗ' trong file code, nó viết lại cả file — rồi muốn quay lại bản chạy ngon lúc nãy thì KHÔNG được nữa? Hay hôm nay làm ở máy này, mai mở máy khác thì code mất tiêu? Đó là nỗi đau khi chưa có Git. Hôm nay ta lắp cho code nút SAVE GAME — và biến chính AI thành trợ lý Git."*
- **Sổ Tay #1 (tím, Slide 4):** HS viết mình từng mất code chưa và đang lưu nhiều phiên bản file bằng cách nào.

### 2. Git = Cỗ máy thời gian (00:12 - 00:22) — Slide 6-7
- **Slide 6:** ngoài ẩn dụ "cỗ máy thời gian", có **định nghĩa rõ** — Git là *hệ thống quản lý phiên bản (version control)*: ghi lại mọi thay đổi, quay về bản cũ, nhiều người cùng làm không đè nhau. Nói ẩn dụ trước rồi chốt bằng định nghĩa.
- **Speaker Notes:** *"Git giống hệt checkpoint trong game. Mỗi commit là một mốc lưu. Chết màn sau? Load lại checkpoint gần nhất, không chơi lại từ đầu."*
- Dạy 3 danh từ lõi (**Slide 7**): Repository · Commit · Branch. Từ nào khó → hỏi AI (bộ prompt ở block 6).

### 3. Git ≠ GitHub + Vòng làm việc + Quiz (00:22 - 00:37) — Slide 8-10
- **Speaker Notes:** *"Git là cái máy trong laptop em (chạy offline được). GitHub là đám mây để đẩy điểm lưu lên, khoe, làm nhóm. Ví von cho dễ: Git như Microsoft Word lưu lịch sử chỉnh sửa trên máy; GitHub như Google Drive để lưu & chia sẻ online."*
- Vòng làm việc (**Slide 9**): sửa → add → commit → push. **Mini-Quiz (xanh, Slide 10):** commit tốt cần lời nhắn rõ.

### 4. Thảo luận cặp: Chấm commit message (00:37 - 00:46) — Slide 11
- **Hoạt động (vàng):** mỗi cặp phân loại 4 lời nhắn commit tốt/tệ và sửa 2 cái tệ.
- **Speaker Notes:** *"Lời nhắn tốt là món quà em gửi cho chính mình 3 tháng sau."* Lười nghĩ? Có thể nhờ AI viết thử (dẫn sang block 6).

### 5. Thao tác GitHub + Game kéo-thả (00:46 - 00:58) — Slide 12-13
- Lật thẻ 6 thao tác (**Slide 12**): push/pull/clone/fork/README/star.
- **Game phân loại lệnh (Slide 13):** kéo 6 việc vào 3 rổ (Lưu mốc · Đưa lên GitHub · Lấy về). Tự chấm điểm.

### 6. ⭐ TRỌNG TÂM: Tạo repo → README → AI trợ lý Git → Web sống (00:58 - 01:28) — Slide 14-18
- **Speaker Notes (đặt kỳ vọng):** *"30 phút tới em vừa đưa game lên GitHub, vừa có LINK WEB SỐNG, vừa học cách bắt AI làm trợ lý gỡ rối Git. Đây là phần vui nhất — không phải ngồi nghe lý thuyết mà tự tay làm."*
- **Tạo repo (Slide 14) + README (Slide 15):** repo Public, upload, commit; README có mô tả + 1 ảnh.
- **⭐ AI — trợ lý Git (Slide 16):** giới thiệu bộ prompt: (1) gia sư khái niệm bằng ẩn dụ game · (2) viết commit message · (3) chỉ đường thao tác trên github.com · (4) giải mã lỗi Git (+ viết README, sinh câu lệnh git). **Nhấn: luôn đọc lại & kiểm chứng — AI có thể sai.**
- **⭐ Khám phá Git cùng AI (cam, Slide 17):** HS tự thử ≥2 prompt cho repo/tình huống của mình (giải thích 1 từ khó bằng ẩn dụ game; viết commit message dùng thật). Ghi lại 1 điều AI vừa giúp.
- **GitHub Pages (Slide 18):** Settings → Pages → nhánh main /root → Save → ~1 phút có link `<tên>.github.io/<repo>/`. **Cho HS mở link trên điện thoại ngay tại lớp** — điểm nhấn cảm xúc. Kẹt bước nào → dùng prompt "chỉ đường thao tác". **Nhấn:** Pages **chỉ chạy web TĨNH** (HTML/CSS/JS); app "động" cần Vercel (buổi 15).
- *GV đi vòng hỗ trợ; khuyến khích HS hỏi AI trước khi hỏi GV để luyện phản xạ "trợ lý Git".*

### 7. Học từ thế giới: Tìm & tái dùng repo (01:28 - 01:40) — Slide 19-22
- **Speaker Notes:** *"GitHub có hàng trăm triệu dự án mở. Biết săn code hay và học từ nó, em tiến bộ nhanh gấp nhiều lần."*
- Cover (**Slide 19**) · Tìm & đánh giá nhanh 1 repo (**Slide 20**): Search → README → Stars/cập nhật → code & license · Fork vs Clone (**Slide 21**).
- **Thảo luận cặp (vàng, Slide 22):** mỗi bạn tìm 1 repo thú vị, kể bạn cặp: tên, làm gì, bao nhiêu sao, license mở không.

### 8. License & Ghi nguồn + Quiz (01:40 - 01:48) — Slide 23-24
- **Speaker Notes:** *"Code công khai KHÔNG có nghĩa được tự do copy — như ảnh trên mạng. Cái quyết định là file LICENSE."*
- Bảng License (**Slide 23**): MIT/Apache · GPL · không license. Kim chỉ nam: học ý tưởng luôn được; dùng code phải đúng license + ghi credit.
- **Mini-Quiz (xanh, Slide 24):** repo không có LICENSE thì được làm gì?

### 9. Hoàn tất sản phẩm APP-14.1 & Sổ Tay #2 (01:48 - 01:55) — Slide 25-26
- HS hoàn thiện repo: commit, README có ảnh, **bật GitHub Pages lấy link web sống**, tìm 1 repo tham khảo. Bí đâu → hỏi AI (bộ prompt Slide 16).
- **Sổ Tay #2 (tím, Slide 26):** dán link web sống + link repo + repo tham khảo. GV mở thử 1-2 web sống lên màn chiếu, khen sản phẩm.

### 10. Tổng kết & Dặn dò (01:55 - 02:00) — Slide 27-29
- Lướt **Checklist (Slide 27)** — HS tự tick (có mục "dùng AI làm trợ lý Git").
- **Sổ Tay #3 (tím, Slide 28):** Git giúp gì mà cách đặt tên v1/v2 không làm được? Prompt "trợ lý Git" nào hữu ích nhất?
- **BTVN chuẩn bị Buổi 15 (Slide 28):** gửi link web sống cho 3 người mở thử; chọn 1 app/web hay dùng, nghĩ nội dung đến từ đâu (máy em hay "máy chủ" ở xa?). Cảm ơn lớp.

---

## LƯU Ý SƯ PHẠM
- **AI là phần vui, không phải lý thuyết khô:** đẩy mạnh block 6 — cho HS tự tay bắt AI giải thích/gỡ lỗi Git. Khuyến khích "hỏi AI trước khi hỏi GV" để luyện kỹ năng trợ lý AI.
- **Luôn kiểm chứng:** nhắc HS AI có thể sai — đọc lại lời AI, thử chạy để chắc chắn (nối kỹ năng fact-check các buổi trước).
- **Bám sản phẩm:** mục tiêu số 1 là mỗi em có **1 link web sống (GitHub Pages)** để khoe. Thiếu giờ → ưu tiên block 6; rút gọn block 7-8 (tìm/tái dùng) thành đọc lướt.
- **Nối buổi sau:** GitHub Pages hôm nay lo web/game **tĩnh**; Buổi 15 (nửa sau) dùng **Vercel** để deploy app "động", cũng lấy code từ repo GitHub này.
