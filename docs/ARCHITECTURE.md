# Kiến trúc — Bài Giảng AI

## Thành phần

```
┌─────────────────────────────────────────────────────────┐
│                    Trình duyệt người học                 │
│  (Chrome / Edge / Firefox — render slide HTML + JS)      │
└──────────────┬──────────────────────────────────────────┘
               │ HTTP/S
               ▼
┌─────────────────────────────────────────────────────────┐
│              Nginx (optional, production)                │
│  - Reverse proxy + static cache + TLS termination        │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────┐
│                FastAPI (Uvicorn, port 8000)              │
│  - GET /             → templates/index.html (Jinja2)     │
│  - GET /lesson/{slug}→ FileResponse từ slides/           │
│  - GET /api/lessons  → JSON từ lessons.json              │
│  - GET /api/health   → JSON                              │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────┐
│             File system (read-only data)                 │
│  - slides/*.html       (nội dung bài giảng)             │
│  - slides/lessons.json (index)                           │
│  - frontend/static/*   (CSS, JS, ảnh)                    │
└─────────────────────────────────────────────────────────┘
```

## Quyết định kiến trúc chính

### 1. Không dùng database
Tại sao: nội dung là file HTML tĩnh, không có user/state phía server, không
cần audit log. JSON file là đủ và dễ chỉnh bằng tay.

Khi nào cần database: nếu sau này muốn lưu kết quả Sổ Tay/Quiz của học sinh
ở server (hiện tại lưu localStorage trình duyệt).

### 2. FastAPI thay vì Flask/Django
Tại sao: auto-generated Swagger UI, async-ready, type hints rõ ràng,
performance tốt mà footprint nhỏ.

### 3. Slide là HTML self-contained
Tại sao: mỗi bài có thể mở độc lập (giáo viên gửi file qua email, học sinh
mở offline), backend chỉ làm catalog + serve. Không có dependency phức tạp
giữa bài.

### 4. Docker Compose thay vì Kubernetes
Tại sao: scale nhỏ (1 lớp ~30 học sinh, lưu lượng thấp). K8s overhead lớn
hơn lợi ích.

## Mở rộng tương lai

| Tính năng | Bước cần làm |
|---|---|
| Lưu Sổ Tay phía server | Thêm SQLite + endpoint POST/GET `/api/notebook/{user_id}/{lesson_id}` |
| Đăng nhập học sinh | Thêm OAuth (Google Login) với `fastapi-users` |
| Theo dõi tiến độ | Lưu trạng thái checklist + completed quizzes vào DB |
| Live class (realtime) | Thêm WebSocket cho thông báo từ GV |
| Mobile app | Wrap web bằng Capacitor/Tauri |
