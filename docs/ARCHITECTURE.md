# Kiến trúc — Bài Giảng AI

Hệ thống tách **nội dung** (slide fragment + `lessons.json`) khỏi **khung trình bày**
(một template Jinja2 dùng chung). Việc ghép hai phần lại có thể chạy ở **2 chế độ**
từ cùng một bộ template:

- **Server (FastAPI):** ghép lúc request — có thêm REST API.
- **Tĩnh (GitHub Pages):** ghép lúc build → HTML thuần, không cần server.

## Luồng dữ liệu

```
   slides/lessons.json ─┐         frontend/templates/
   (index 24 buổi)      │           ├── index.html   (trang chủ)
                        │           └── lesson.html   (KHUNG dùng chung:
   slides/buoi_XX.html ─┤                              sidebar+dropdown, top-bar,
   (fragment: slides,   │                              slide-engine, Sổ Tay,
    Sổ Tay, css/js)     │                              quiz/checklist/drag-drop)
                        ▼
        ┌────────────────────────────────────┐
        │  slide_fragment.parse_fragment()    │  tách fragment thành:
        │  rendering.group_lessons_by_module()│  style / slides / nb-questions / script
        └───────────────┬────────────────────┘
            ┌────────────┴─────────────┐
            ▼                          ▼
  ┌───────────────────┐      ┌──────────────────────────┐
  │ CHẾ ĐỘ SERVER     │      │ CHẾ ĐỘ TĨNH               │
  │ backend/app/main  │      │ scripts/build_static.py   │
  │ render lúc request│      │ render lúc build → dist/  │
  │ → /lesson/{slug}  │      │ → dist/lesson/buoi_XX.html│
  │ + REST API        │      │ (đường dẫn tương đối)     │
  └─────────┬─────────┘      └────────────┬─────────────┘
            ▼                             ▼
   Uvicorn / Render.com         GitHub Pages (Actions deploy)
```

## Thành phần

| File | Vai trò |
|---|---|
| `slides/lessons.json` | Single source of truth: id, slug, module, `available`, mô tả, tags |
| `slides/buoi_XX.html` | **Fragment** một buổi: `<section class="slide">` + `<script id="nb-questions">` + css/js riêng |
| `frontend/templates/lesson.html` | Khung dùng chung cho mọi bài (sidebar có dropdown module, slide-engine, Sổ Tay, handler quiz/game) |
| `frontend/templates/index.html` | Trang chủ — list bài theo module, vòng tiến độ |
| `backend/app/slide_fragment.py` | Parse fragment → `{style, slides, nb-questions, script}` |
| `backend/app/rendering.py` | `group_lessons_by_module()` + `MODULE_COLORS` (dùng chung server & build) |
| `backend/app/main.py` | Route web (`/`, `/lesson/{slug}`) + REST API; render template lúc request |
| `scripts/build_static.py` | Render đúng template đó lúc build → `dist/` cho GitHub Pages |
| `.github/workflows/deploy-pages.yml` | CI: build `dist/` + publish GitHub Pages mỗi lần push `main` |

### Tham số hoá đường dẫn (1 template, 2 chế độ)

`lesson.html` và `index.html` nhận các biến đường dẫn từ context:

| Biến | Server | Tĩnh (index) | Tĩnh (lesson) |
|---|---|---|---|
| `home_link` | `/` | `index.html` | `../index.html` |
| `static_base` | `/static` | `static` | (không dùng) |
| `lesson_urls[slug]` | `/lesson/{slug}` | `lesson/{slug}.html` | `{slug}.html` |
| `show_api_links` | `true` | `false` | `false` |

Nhờ vậy bản tĩnh dùng đường dẫn **tương đối** → chạy đúng cả dưới sub-path
`username.github.io/<repo>/`.

## Quyết định kiến trúc chính

### 1. Tách fragment khỏi khung
Trước đây mỗi slide là một HTML hoàn chỉnh ~2000 dòng, lặp lại toàn bộ CSS + JS
engine. Khi sửa khung phải sửa từng file. Giờ khung sống một chỗ (`lesson.html`),
fragment chỉ còn nội dung → thêm bài mới gọn, sửa khung một lần áp dụng mọi bài.

### 2. Không dùng database
Nội dung là file tĩnh; trạng thái học sinh (Sổ Tay, quiz, checklist) lưu
`localStorage` trình duyệt. JSON file đủ làm index và dễ sửa tay. Cần DB nếu sau
này muốn lưu kết quả phía server.

### 3. Hai chế độ deploy song song
- **Tĩnh / GitHub Pages:** miễn phí, không cần server, hợp để phát hành rộng.
  Mất REST API (`/api/*`).
- **Server / FastAPI (Render, Docker):** giữ REST API + Swagger, render động.

Cùng template + cùng dữ liệu nên không lệch nội dung giữa hai bản.

### 4. FastAPI thay vì Flask/Django
Swagger UI tự sinh, async-ready, type hints rõ, footprint nhỏ.

## Mở rộng tương lai

| Tính năng | Bước cần làm |
|---|---|
| Lưu Sổ Tay phía server | Thêm SQLite + endpoint POST/GET `/api/notebook/{user_id}/{lesson_id}` (chỉ bản server) |
| Đăng nhập học sinh | OAuth (Google) với `fastapi-users` |
| Theo dõi tiến độ | Lưu checklist + quiz đã xong vào DB |
| Tìm kiếm bài trên trang chủ | Thêm ô search lọc client-side trong `app.js` (chạy cả bản tĩnh) |
| Mobile app | Wrap web bằng Capacitor/Tauri |
