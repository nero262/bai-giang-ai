# Sổ Tay Cá Nhân — Setup Google Apps Script

Hướng dẫn 1 lần (~10 phút) để frontend GitHub Pages tự gửi phản hồi Sổ Tay vào Google Sheet → tải Excel.

## Tại sao Apps Script?

Site host trên GitHub Pages chỉ chạy được code phía client. Apps Script là backend miễn phí, gắn liền Google Sheet — giáo viên xem trực tiếp như Excel online, và bấm `File → Download → Microsoft Excel (.xlsx)` khi cần lưu offline.

## Các bước

### 1. Tạo Google Sheet đích

1. Mở [sheets.google.com](https://sheets.google.com), tạo Sheet mới, đặt tên (vd `So_Tay_Phan_Hoi_AI_24_Buoi`).
2. Đổi tên sheet đầu (tab dưới cùng) thành **`responses`** (đúng chính tả, không khoảng trắng).
3. Copy **Sheet ID** từ URL:
   ```
   https://docs.google.com/spreadsheets/d/1f_TO_N7BZHqADFyEoYF8s9ThRH1VfMcDsVQ7340k5Fw/edit
   ```

### 2. Tạo Apps Script Web App

1. Mở [script.google.com](https://script.google.com) → **New project**.
2. Xoá toàn bộ nội dung file `Code.gs` mặc định.
3. Dán toàn bộ nội dung file `deployment/apps_script/Code.gs` (cùng repo này) vào.
4. Tìm dòng `const SHEET_ID = 'PASTE_SHEET_ID_HERE';` → thay bằng Sheet ID ở bước 1.
5. Bấm **Save** (Ctrl+S), đặt tên project (vd `SoTayWebhook`).

### 3. Deploy thành Web App

1. **Deploy → New deployment**.
2. Bấm icon bánh răng (⚙) cạnh "Select type" → chọn **Web app**.
3. Cấu hình:
   - **Description**: `So Tay v1`
   - **Execute as**: `Me (email của bạn)`
   - **Who has access**: **Anyone** (bắt buộc — phải public thì học sinh mới gửi được)
4. Bấm **Deploy** → lần đầu sẽ hỏi cấp quyền:
   - Bấm **Authorize access** → chọn tài khoản Google của bạn → **Advanced** → **Go to (project name) (unsafe)** → **Allow**.
5. Copy **Web app URL** dạng:
   ```
   https://script.google.com/macros/s/AKfycb.../exec
   ```

### 4. Test nhanh

Mở URL trên trong trình duyệt — nếu thấy `{"ok":true,"service":"so-tay-phan-hoi","sheet":"responses"}` là OK.

### 5. Dán URL vào frontend

Mở `frontend/templates/lesson.html`, tìm dòng:

```html
<meta name="notebook-endpoint" content="">
```

Sửa thành:

```html
<meta name="notebook-endpoint" content="https://script.google.com/macros/s/AKfycb.../exec">
```

Commit + push → GitHub Pages tự build → xong.

### 6. Test end-to-end

1. Mở trang lesson buổi 1 trên GitHub Pages.
2. Bấm **Sổ Tay Cá Nhân** → nhập tên + lớp + ít nhất 1 câu trả lời.
3. Bấm **Lưu & Xác nhận** → status hiện `✓ Đã gửi Sổ Tay tới giáo viên`.
4. Mở lại Google Sheet → có 1 hàng mới với đầy đủ thông tin.

## Cập nhật code Apps Script sau này

Sau khi sửa `Code.gs`:

- Cách 1 (giữ URL cũ): **Deploy → Manage deployments → bấm bút chì cạnh deployment hiện tại → Version: New version → Deploy**. URL không đổi → không cần cập nhật frontend.
- Cách 2: **New deployment** → URL mới → phải sửa lại `meta name="notebook-endpoint"`.

## Tải file Excel

1. Mở Google Sheet `So_Tay_Phan_Hoi_AI_24_Buoi`.
2. **File → Download → Microsoft Excel (.xlsx)**.
3. File có đầy đủ tất cả các cột (động theo số câu hỏi mỗi buổi).

## Lọc theo buổi

Trong Sheet:
- Cột `lesson_id` lọc theo số buổi (1, 2, 3, …).
- Cột `lesson_slug` lọc theo slug (`buoi_01`, `buoi_03`, …).
- Cột `client_id`: cùng học sinh trên cùng thiết bị → cùng UUID, dùng để chống duplicate.

Để tạo dashboard pivot tự động: **Insert → Pivot table → Data range = `responses!A:Z`**, group theo `lesson_id`.

## Bảo mật & vận hành

- **URL Apps Script lộ trong HTML** (xem được qua View Source) → có thể bị abuse gửi rác.
  - Validate ở Apps Script đã reject các submission thiếu `client_id` / `lesson_id` / `student_name`.
  - Nếu thấy rác nhiều, **Deploy → Manage deployments → Archive** deployment cũ, tạo mới → URL khác. Cập nhật lại `meta` trong `lesson.html`.
- **Quota Apps Script** (free): 20,000 lượt gọi/ngày, 6 phút/exec → quá dư cho một lớp.
- **Backup**: Sheet auto-save vào Google Drive; định kỳ tải `.xlsx` lưu offline.

## Khắc phục sự cố

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Status hiện `✗ Gửi không thành công (TypeError: Failed to fetch)` | URL sai hoặc deployment chưa public | Kiểm tra `meta name="notebook-endpoint"`, deployment phải "Anyone" |
| Status hiện `✗ ... (HTTP_401/403)` | Deployment đặt "Anyone with Google account" thay vì "Anyone" | Redeploy với "Anyone" |
| Sheet không hiện hàng mới | SHEET_ID sai hoặc sheet không tên `responses` | Sửa `SHEET_ID` trong `Code.gs`, đảm bảo tab tên `responses` |
| Hiện cảnh báo `Chưa cấu hình server` | `meta` để trống | Dán URL Apps Script vào `meta name="notebook-endpoint"` |
| Học sinh báo gửi nhưng Sheet trùng | Cùng học sinh sửa rồi gửi lại | Bình thường — code UPDATE thay vì INSERT theo (client_id, lesson_id) |
