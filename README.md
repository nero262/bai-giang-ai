# Khóa AI 24 buổi — Bài Giảng

Nền tảng web phục vụ bài giảng AI tương tác cho học sinh lớp 8 và lớp 12.
Mỗi bài giảng là một **slide fragment** (chỉ chứa nội dung slide); phần khung
dùng chung — sidebar, thanh điều hướng, slide-engine, Sổ Tay, quiz, drag-drop —
do một template duy nhất cung cấp. Có thể chạy theo **2 cách**: server FastAPI
(render lúc request) hoặc **trang tĩnh** build sẵn cho GitHub Pages.

## Tính năng

- 24 bài giảng; mỗi buổi là một fragment trong `slides/`, tự liên kết vào template chung.
- Trang chủ + sidebar sinh động từ `slides/lessons.json` (single source of truth).
- Sidebar có **dropdown từng module** — click để xổ/thu danh sách bài.
- Sổ Tay Cá Nhân, quiz chấm điểm, checklist, drag-drop, flashcard — toàn bộ client-side
  (lưu `localStorage`), chạy được cả trên bản tĩnh lẫn server.
- **Chạy 2 chế độ:** FastAPI (có REST API + Swagger `/api/docs`) **hoặc** trang tĩnh
  (build → GitHub Pages, không cần server).
- Style "Modern Tech" (Blue + Slate). Đóng gói Docker cho bản server.

## Cấu trúc thư mục

```
bai_giang/
├── README.md                  ← Tài liệu này
├── Makefile                   ← make dev / build-static / test / up
├── docker-compose.yml         ← Deploy bản server bằng 1 lệnh
├── render.yaml                ← Blueprint deploy lên Render.com (bản server)
├── .env.example               ← Mẫu biến môi trường
├── .gitignore  /  .dockerignore
│
├── .github/workflows/
│   └── deploy-pages.yml        ← CI: build trang tĩnh + deploy GitHub Pages
│
├── backend/                   ← FastAPI app (bản server)
│   ├── app/
│   │   ├── main.py            ← Entry point: route web (/ , /lesson/{slug}) + API
│   │   ├── config.py          ← Cấu hình runtime (đường dẫn, CORS…)
│   │   ├── models.py          ← Pydantic models (Lesson, …)
│   │   ├── lesson_repository.py ← Đọc lessons.json
│   │   ├── rendering.py        ← Gom lesson theo module (dùng chung server + build)
│   │   └── slide_fragment.py   ← Parse fragment: tách style/slides/Sổ Tay/script
│   ├── tests/test_api.py
│   ├── requirements.txt
│   └── pyproject.toml
│
├── frontend/                  ← UI dùng chung (Jinja2 + CSS)
│   ├── templates/
│   │   ├── index.html         ← Template trang chủ
│   │   └── lesson.html         ← Template trang bài giảng (khung dùng chung)
│   └── static/
│       ├── css/style.css       ← CSS trang chủ
│       ├── js/app.js
│       └── images/
│
├── slides/                    ← Nội dung bài giảng (fragment)
│   ├── lessons.json           ← Index 24 buổi (id, slug, module, available…)
│   └── buoi_01.html …          ← Fragment từng buổi (KHÔNG còn <html>/khung)
│
├── deployment/
│   ├── docker/Dockerfile
│   └── nginx/bai_giang.conf
│
├── scripts/
│   ├── build_static.py         ← Build trang tĩnh → dist/ (GitHub Pages)
│   ├── migrate_slide_to_fragment.py ← Chuyển slide HTML cũ → fragment
│   ├── run_dev.sh / run_test.sh / deploy.sh
│
├── prompts/                   ← Prompt + hướng dẫn tạo bài giảng mới
│   ├── lesson_template_prompt.md
│   └── HUONG_DAN.md
│
└── docs/                      ← Tài liệu kỹ thuật (ARCHITECTURE, SELF_REVIEW)
```

> **dist/** (kết quả build tĩnh) được `.gitignore` — không commit; GitHub Actions
> tự sinh khi deploy.

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

### Phương án C — Trang tĩnh (GitHub Pages, không cần server)

Toàn bộ nội dung là tĩnh (template + `lessons.json` + slide fragment). Một bước
build ghép chúng thành HTML hoàn chỉnh, đẩy lên GitHub Pages — không cần FastAPI.

```bash
make build-static     # render → dist/
make serve-static     # build rồi xem thử tại http://127.0.0.1:8080
```

`dist/` gồm `index.html`, `lesson/buoi_XX.html`, `static/`. Dùng đường dẫn tương đối
nên chạy đúng cả khi đặt dưới sub-path GitHub Pages (`username.github.io/<repo>/`).

**Tự động deploy:** workflow [.github/workflows/deploy-pages.yml](.github/workflows/deploy-pages.yml)
build + publish mỗi lần push lên `main`. Bật một lần: **Settings → Pages →
Build and deployment → Source = "GitHub Actions"**.

> Sổ Tay, quiz, checklist, drag-drop, dropdown module đều là JS client-side nên
> chạy đầy đủ trên bản tĩnh. Chỉ REST API (`/api/*`, Swagger) là riêng của bản server.

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

1. Tạo **fragment** mới trong `slides/`, ví dụ `buoi_02.html`
   (tham khảo [prompts/lesson_template_prompt.md](prompts/lesson_template_prompt.md)
   để tạo bằng Claude/ChatGPT). Fragment chỉ chứa các `<section class="slide">`,
   cấu hình Sổ Tay (`<script id="nb-questions">`) và CSS/JS riêng nếu cần —
   **không** có `<html>`/sidebar/khung.
2. Mở `slides/lessons.json`, đổi `"available": false` → `true` cho buổi tương ứng.
3. Bài mới **tự** xuất hiện trên trang chủ + sidebar và liên kết vào template:
   - Bản server: restart (`make restart` hoặc `make dev`) rồi mở `/lesson/buoi_02`.
   - Bản tĩnh: `make build-static` (hoặc push lên `main` để CI tự build).

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

## Cấu trúc một slide (fragment)

Mỗi file trong `slides/` là một **fragment** — KHÔNG còn là HTML hoàn chỉnh.
Nó chỉ gồm, theo thứ tự:

```html
<!-- comment ghi rõ buổi -->
<script type="application/json" id="nb-questions">{ "1": {...}, ... }</script>  <!-- câu hỏi Sổ Tay (tuỳ chọn) -->
<style> /* CSS riêng của buổi (tuỳ chọn) */ </style>
<section class="slide active slide-cover" data-slide="1" ...> ... </section>
<section class="slide" data-slide="2" ...> ... </section>
...
<script> /* JS riêng của buổi (tuỳ chọn) */ </script>
```

Khung dùng chung (sidebar có dropdown module, top-bar, slide-engine, Sổ Tay overlay,
handler quiz/checklist/drag-drop/flashcard) nằm trong
[frontend/templates/lesson.html](frontend/templates/lesson.html).

**Hai chế độ ghép fragment vào khung:**
- **Server:** `backend/app/slide_fragment.py` parse fragment → `main.py` render
  `lesson.html` lúc request (`/lesson/{slug}`).
- **Tĩnh:** `scripts/build_static.py` làm đúng việc đó lúc build → ghi ra
  `dist/lesson/buoi_XX.html`.

Cùng một template phục vụ cả hai; khác biệt chỉ là đường dẫn link (server dùng
tuyệt đối `/lesson/...`, tĩnh dùng tương đối để chạy dưới sub-path GitHub Pages).
Chi tiết kiến trúc: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## License

Nội dung bài giảng và mã nguồn nội bộ — sử dụng cho mục đích đào tạo.
