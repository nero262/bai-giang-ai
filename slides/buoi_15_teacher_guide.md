# Hướng Dẫn Giảng Dạy & Timeline — Buổi 15

**Chủ đề:** Xây dựng và triển khai website động  
**Đối tượng:** Học sinh cấp 2-3 (đã học buổi 1-14; đã biết vibe-code web tĩnh cơ bản và có repo/GitHub Pages ở buổi 14).

**Mục tiêu cốt lõi:**
1. Hiểu vì sao một sản phẩm có **nhiều người cùng tương tác** cần **backend** để giữ **trạng thái chung**.
2. Phân biệt được **Frontend** (thứ người chơi nhìn thấy) và **Backend** (thứ xử lý ở server) qua một game thật.
3. Tự tay tạo và deploy **1 game mini có FE + BE** lên **Vercel** để cả lớp cùng vào chơi.

> **SẢN PHẨM SHOW ĐƯỢC (APP-15.1):** game **"Cả lớp đánh boss"**. Học sinh nhập tên, vào trận, thấy thanh máu boss, danh sách người chơi, log hành động và bấm tấn công. Cả lớp cùng nhìn chung một boss vì backend đang giữ trạng thái chung. Game được deploy lên **Vercel** có link `.vercel.app`.

## CHUẨN BỊ TRƯỚC BUỔI HỌC
- **Máy + wifi (bắt buộc):** để code, push GitHub, và deploy Vercel.
- **Tài khoản GitHub:** đã dùng ở buổi 14.
- **Công cụ vibe-code:** Bolt / Cursor / OpenCode / chatbot AI quen dùng.
- **Khuyến nghị kỹ thuật:** ưu tiên tạo project theo kiểu **Next.js + API route** vì deploy Vercel dễ nhất cho người mới.
- **GV chuẩn bị trước:** 1 bản demo game boss thật đơn giản để mở cho lớp xem đầu giờ nếu cần.

---

## TIMELINE CHI TIẾT (120 PHÚT)

*Nguyên tắc: giảm lý thuyết, tăng thời gian build sản phẩm. Lý thuyết chỉ giữ những gì trực tiếp phục vụ việc hiểu FE/BE và deploy.*

### 1. Khởi động bằng "nỗi đau" (00:00 - 00:12) — Slide 1-5
- **Speaker Notes (TED-style):** *"Nếu mỗi bạn tự mở một game HTML trên máy mình thì mỗi bạn sẽ đánh một con boss riêng. Nhưng game online thì khác: cả lớp cùng nhìn thấy 1 con boss, cùng đánh, cùng thấy máu tụt. Vậy ai đang giữ máu boss chung cho cả lớp?"*
- **Sổ Tay #1 (tím, Slide 4):** HS viết dự đoán: backend/server đang giữ gì để cả lớp cùng chơi được.
- **Mục tiêu cần chốt ngay đầu buổi:** hôm nay không chỉ "nghe về web động", mà sẽ tự làm 1 game nhiều người chơi có backend thật.

### 2. Phân biệt web tĩnh vs web có backend (00:12 - 00:25) — Slide 6-7
- **Slide 6:** chốt 1 ý cực quan trọng: web tĩnh chỉ chạy trong máy em; game nhiều người chơi cần nơi giữ trạng thái chung.
- **Slide 7:** kéo-thả ví dụ để HS phân loại nhanh.
- **Speaker Notes:** *"Portfolio hay game rắn HTML rất tốt, nhưng chúng không đủ để cả lớp chơi chung. Chỉ khi có backend, cả lớp mới nhìn chung một trận."*

### 3. Giải phẫu game hôm nay: FE, BE, state chung (00:25 - 00:40) — Slide 8-10
- **Slide 8:** giải thích 3 phần của game hôm nay:
  - **Frontend:** ô nhập tên, nút đánh, thanh máu, log.
  - **Backend:** nhận lệnh, tính sát thương, cập nhật trạng thái.
  - **State chung:** máu boss, người chơi, log.
- **Slide 9:** đi qua luồng `join -> attack -> state`.
- **Speaker Notes:** *"Backend hôm nay giống trọng tài trận đấu: ai vào, ai đánh, trừ bao nhiêu máu, tất cả nó quyết định và giữ chung."*
- **Slide 10:** lật thẻ thuật ngữ nhanh, không sa đà lý thuyết.

### 4. Nhắc nhanh chỗ đứng của GitHub Pages và giới thiệu Vercel (00:40 - 00:52) — Slide 11-13
- **Slide 11:** ôn 1 phút: Pages chỉ chạy web tĩnh.
- **Slide 12:** vì sao hôm nay chọn Vercel: nối GitHub, hỗ trợ Next.js + API route, miễn phí.
- **Slide 13:** 4 bước deploy repo lên Vercel.
- **Speaker Notes:** *"Buổi 14 em học cách đưa file tĩnh lên mạng. Hôm nay em học cách đưa luôn phần 'trọng tài trận đấu' lên mạng."*

### 5. AI trợ lý code + deploy (00:52 - 01:00) — Slide 14-15
- **Slide 14:** nhắc nhẹ env variable, nhưng chỉ giới thiệu, không dạy sâu.
- **Slide 15:** cho HS thấy AI có thể giúp 4 việc: sinh code game, giải thích FE/BE, đọc lỗi build, chỉ đường deploy.
- **Chốt:** AI sinh code nhanh, nhưng sản phẩm phải đạt 3 dấu hiệu:
  - nhập tên được
  - bấm đánh boss được
  - 2 máy/2 tab thấy chung 1 máu boss

### ☕ GIẢI LAO / CHECKPOINT (01:00 - 01:10)
- Nếu lớp chậm, GV có thể dùng 10 phút này làm checkpoint thay vì nghỉ trọn:
  - ai đã có project
  - ai đã có API route
  - ai còn vướng tạo repo / Next.js

### 6. ⭐ THỰC HÀNH TRỌNG TÂM: Vibe-code game boss (01:10 - 01:40) — Slide 16
- **Prompt mẫu:** dùng prompt trong slide để yêu cầu AI tạo game `Cả lớp đánh boss` bằng **Next.js (App Router)** với 3 API route:
  - `POST /api/join`
  - `POST /api/attack`
  - `GET /api/state`
- **Trạng thái tối thiểu backend giữ:**
  - `bossHp`
  - `bossMaxHp`
  - `players`
  - `logs`
- **Speaker Notes (đặt kỳ vọng):** *"Nếu làm xong phần này, em đã thực sự bước từ web tĩnh sang web có backend."*
- **GV đi vòng hỗ trợ theo thứ tự ưu tiên:**
  1. App có chạy local không
  2. API route có hoạt động không
  3. 2 tab có cùng thấy boss thay đổi không

### 7. Đẩy lên GitHub rồi deploy Vercel (01:40 - 01:52) — Slide 13 + 16 + 17
- HS push code lên GitHub.
- Import repo vào Vercel.
- Nhận link `.vercel.app`.
- Mỗi em hoặc mỗi nhóm mở thử trên 2 máy / 2 điện thoại / 2 tab.
- **Sổ Tay #2 (tím, Slide 17):** ghi link game và chỉ ra FE / BE / state chung.

### 8. Chơi chéo + tổng kết (01:52 - 02:00) — Slide 18-22
- **Slide 18:** đổi máy cho bạn cặp hoặc mở game của nhau.
- **Slide 19:** quiz chốt vì sao Pages không đủ cho game này.
- **Slide 20:** checklist tự tick.
- **Slide 21:** Sổ Tay #3: so sánh web tĩnh buổi 14 với game có backend hôm nay.
- **Slide 22:** kết lại bằng việc giữ link để khoe và nối sang buổi 16 về an toàn thông tin.

---

## PROMPT CHUẨN CHO HỌC SINH

> Tạo một web app game mini bằng Next.js (App Router) để deploy lên Vercel.
>
> Ý tưởng: "Cả lớp đánh boss".
>
> Yêu cầu:
> - Có màn hình đầu cho nhập tên người chơi rồi bấm "Vào trận".
> - Sau khi vào trận, hiện 1 con boss, thanh máu boss, danh sách người chơi đang tham gia, log 8 hành động gần nhất, và nút "Tấn công".
> - Frontend phải gọi backend bằng API route.
> - Tạo 3 API route:
>   1. POST /api/join: nhận tên người chơi và thêm vào danh sách người chơi nếu chưa có.
>   2. POST /api/attack: nhận tên người chơi, random sát thương từ 5 đến 20, trừ máu boss, ghi log kiểu "An đánh 12 máu".
>   3. GET /api/state: trả về bossHp, bossMaxHp, players, logs.
> - Lưu trạng thái chung tạm thời trong bộ nhớ server bằng biến toàn cục đơn giản. Chưa cần database.
> - Frontend polling /api/state mỗi 2 giây để mọi người thấy boss cập nhật.
> - Khi boss về 0 máu thì hiện thông báo "Cả lớp chiến thắng!".
> - Giao diện dễ nhìn, vui, hợp học sinh, có cảm giác game.
> - Ghi chú rõ trong code: đâu là frontend, đâu là backend.
> - Đảm bảo chạy local được và phù hợp deploy lên Vercel.

## LƯU Ý SƯ PHẠM
- **Giảm tham kiến thức:** buổi này không cần dạy sâu DNS, HTTP, JSON, database thật.
- **Bám một sản phẩm duy nhất:** cả buổi chỉ xoay quanh game boss. Nhờ vậy học sinh không bị tản mạch.
- **Chấp nhận bản tối giản:** chưa cần đăng nhập thật, chưa cần websocket, chưa cần database.
- **Polling là đủ:** 2 giây/lần đủ để HS thấy "state chung", không cần công nghệ realtime phức tạp.
- **Nếu lớp chậm:** GV có thể phát sẵn một project khung Next.js, HS chỉ tập trung sửa giao diện và route.
- **Nối buổi 16:** khi game đã lên internet, tự nhiên nói sang secret, tài khoản, repo công khai, env variable và an toàn thông tin.
