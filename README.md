# Khóa AI 24 buổi — Bài Giảng

Nền tảng web phục vụ bài giảng AI tương tác cho học sinh lớp 8 và lớp 12.
Mỗi bài giảng là một file HTML độc lập (có slide, quiz, flashcard, drag-drop,
sổ tay cá nhân), được FastAPI phục vụ và liệt kê trên một trang chủ.

## Tính năng

- 24 bài giảng dạng slide HTML, mỗi bài là một file độc lập.
- Trang chủ động liệt kê các bài giảng từ `slides/lessons.json`.
- REST API (Swagger UI tại `/api/docs`).
- Sổ Tay Cá Nhân — lưu trạng thái câu trả lời vào `localStorage` của trình duyệt.
- Style "Modern Tech" (Blue + Slate) — phù hợp môi trường giáo dục/doanh nghiệp.
- Đóng gói Docker, một lệnh là chạy được.

## Cấu trúc thư mục

```
bai_giang/
├── README.md                  ← Tài liệu này
├── Makefile                   ← Lệnh nhanh: make dev / make up / make test
├── docker-compose.yml         ← Deploy 1 lệnh
├── .env.example               ← Mẫu biến môi trường
├── .gitignore  /  .dockerignore
│
├── backend/                   ← FastAPI app
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            ← Entry point, route web + API
│   │   ├── config.py          ← Cấu hình runtime
│   │   ├── models.py          ← Pydantic models
│   │   └── lesson_repository.py
│   ├── tests/
│   │   └── test_api.py        ← Pytest
│   ├── requirements.txt
│   └── pyproject.toml
│
├── frontend/                  ← UI cho trang chủ (Jinja2 + CSS)
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/style.css
│       ├── js/app.js
│       └── images/
│
├── slides/                    ← Nội dung bài giảng
│   ├── lessons.json           ← Index 24 buổi
│   └── buoi_01.html           ← Slide HTML từng buổi
│
├── deployment/
│   ├── docker/Dockerfile
│   └── nginx/bai_giang.conf   ← Reverse proxy (optional)
│
├── scripts/
│   ├── run_dev.sh
│   ├── run_test.sh
│   └── deploy.sh
│
├── prompts/                   ← Prompt để tự tạo bài giảng mới
│   ├── lesson_template_prompt.md
│   └── HUONG_DAN.md
│
└── docs/                      ← Tài liệu kỹ thuật bổ sung
```

## Yêu cầu

- Python 3.12+
- (Tùy chọn) Docker + Docker Compose

## Chạy nhanh

### Phương án A — Dev local

```bash
make install       # cài venv + dependencies
make dev           # khởi động dev server tại http://127.0.0.1:8000
```

Mở trình duyệt vào `http://127.0.0.1:8000`.

### Phương án B — Docker (production)

```bash
cp .env.example .env
make up            # docker compose up -d
make logs          # xem log realtime
make down          # dừng
```

Truy cập `http://localhost:8000`.

## Các URL chính

| URL | Mô tả |
|---|---|
| `/` | Trang chủ — danh sách 24 bài giảng |
| `/lesson/buoi_01` | Mở slide bài giảng Buổi 1 |
| `/api/docs` | Swagger UI |
| `/api/health` | Healthcheck JSON |
| `/api/lessons` | Danh sách bài giảng (JSON) |
| `/api/lessons/{slug}` | Chi tiết một bài |

## Thêm bài giảng mới

1. Tạo file HTML mới trong `slides/`, ví dụ `buoi_02.html`
   (tham khảo `prompts/lesson_template_prompt.md` để tạo bằng Claude/ChatGPT).
2. Mở `slides/lessons.json`, đổi `"available": false` thành `true` cho buổi tương ứng
   (hoặc thêm entry mới nếu vượt 24 buổi).
3. Restart server: `make restart` (Docker) hoặc Ctrl+C rồi `make dev` lại.

Xem chi tiết trong [prompts/HUONG_DAN.md](prompts/HUONG_DAN.md).

## Test

```bash
make test
```

Hoặc trực tiếp:

```bash
cd backend
. .venv/bin/activate
pytest
```

## Triển khai lên VPS

1. Cài Docker, Docker Compose lên VPS.
2. Copy thư mục `bai_giang/` lên server (ví dụ qua `scp -r` hoặc `git clone`).
3. `cp .env.example .env` và chỉnh nếu cần.
4. `docker compose up -d`.
5. (Tùy chọn) Cấu hình Nginx + Let's Encrypt — tham khảo `deployment/nginx/bai_giang.conf`.

## Cấu trúc một slide HTML

Mỗi file slide trong `slides/` là một HTML hoàn chỉnh, self-contained
(CSS + JS inline). Có thể mở trực tiếp file mà không cần backend.

Backend chỉ làm hai việc: (1) liệt kê các bài giảng, (2) phục vụ file HTML.

## License

Nội dung bài giảng và mã nguồn nội bộ — sử dụng cho mục đích đào tạo.
