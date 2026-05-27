# Self-Review — Software Engineer Perspective

Đánh giá repo `bai_giang/` từ góc nhìn của một software engineer trước khi
bàn giao. Mục tiêu: phát hiện rủi ro, đề xuất cải thiện cụ thể.

## ✅ Đã làm tốt

### Cấu trúc
- Tách bạch rõ `backend/`, `frontend/`, `slides/`, `deployment/`,
  `scripts/`, `prompts/`, `docs/` — dễ điều hướng.
- `lessons.json` là single source of truth cho danh sách bài → đổi nội dung
  không cần đổi code.
- Slide là HTML self-contained → có thể distribute offline.

### Backend
- FastAPI + Pydantic models có type hints rõ ràng.
- Tách `LessonRepository` ra khỏi route handler → dễ mock khi test.
- Singleton `Settings` qua `lru_cache` — chuẩn 12-factor.
- Endpoint phân tách giữa Web (`/`, `/lesson/...`) và REST (`/api/...`).
- Healthcheck endpoint sẵn cho orchestrator.
- 5/5 unit tests pass.

### DevOps
- Multi-stage Dockerfile (builder + runtime) → image gọn.
- Non-root user trong container → bảo mật.
- HEALTHCHECK trong Dockerfile + docker-compose.
- `.dockerignore` ngăn `__pycache__`, `.venv` lọt vào image.
- Slides mount read-only volume → có thể cập nhật mà không rebuild.

### DX (Developer Experience)
- Một `Makefile` với 8 lệnh phổ biến + help auto-generated.
- Scripts shell có shebang + `set -euo pipefail` → fail-fast.
- README có quickstart 3 dòng cho cả 2 phương án (dev/docker).
- `.env.example` không chứa secret thật.

## ⚠️ Hạn chế hiện tại — cần biết

### 1. Không có persistent state cho học sinh
- **Hiện tại:** Sổ Tay & Checklist lưu trong `localStorage` của trình duyệt.
  Nếu học sinh đổi thiết bị / xóa cache → mất hết.
- **Khi nào cần fix:** khi nhà trường muốn xem dữ liệu cảm xúc/reflection
  của học sinh để cải tiến giáo án.
- **Cách fix:** thêm SQLite + endpoint POST `/api/notebook` + đăng nhập
  đơn giản (cookie hoặc magic link qua Zalo).

### 2. Không có rate-limit / auth
- **Hiện tại:** API public hoàn toàn. Ai cũng GET được.
- **Rủi ro:** nếu deploy public, một con bot có thể nuốt băng thông.
- **Cách fix:** đặt sau Nginx có `limit_req_zone`, hoặc dùng
  `slowapi` middleware cho FastAPI.

### 3. Không có CI/CD
- **Hiện tại:** test phải chạy manual. Không có gate trước khi merge.
- **Cách fix:** thêm `.github/workflows/ci.yml` chạy `pytest` + lint
  trên mỗi PR.

### 4. Không có logging có cấu trúc
- **Hiện tại:** dùng print của Uvicorn — text plain, khó query.
- **Cách fix:** dùng `structlog` hoặc `loguru`, ship logs ra stdout
  dưới dạng JSON.

### 5. Frontend trang chủ đơn giản
- **Hiện tại:** chỉ liệt kê + bấm vào mở. Không có search, không có lọc
  theo module.
- **Cách fix:** thêm input search + filter chip → JS đã có hook để mở rộng.

### 6. Slide HTML có CSS+JS inline ~100KB / bài
- **Trade-off:** chấp nhận để mỗi bài self-contained và mở offline được.
- **Khi 24 bài đầy đủ:** ~2.4 MB tổng — vẫn nhẹ với web hiện đại.

## 🐛 Issues đã phát hiện và sửa trong quá trình review

| Issue | Nguyên nhân | Cách sửa | Trạng thái |
|---|---|---|---|
| File `slides/buoi_01.html` bị truncate (mất đoạn JS cuối + `</body></html>`) | Encoding/IO khi copy file có ký tự tiếng Việt qua mount filesystem | Khôi phục đoạn cuối từ file gốc bằng `sed + cat` | ✅ Đã sửa |
| `slide` cũ dùng `position: absolute + visibility: hidden` cùng `opacity:0` → user agent screen-reader vẫn announce content slide ẩn | Layout cũ | Đổi sang `display: none` cho slide không active | ✅ Đã sửa |
| Palette tím-hồng không phù hợp môi trường Viettel/giáo dục formal | Design ban đầu | Đổi sang Modern Tech Blue + Slate | ✅ Đã sửa |
| Lỗi chính tả: "khoá" vs "khóa" lẫn lộn | Văn bản gốc | Thống nhất "khóa" qua `replace_all` | ✅ Đã sửa |
| "Khoa học sinh" trong sidebar brand → tối nghĩa | Văn bản gốc | Đổi thành "Dành cho học sinh" | ✅ Đã sửa |

## 📋 Recommendations để mainainability tốt hơn

### Ngắn hạn (làm ngay khi có thời gian)
1. **Thêm CI** — file `.github/workflows/ci.yml` chạy `pytest` + black/ruff.
2. **Thêm lint config** — `ruff.toml` để format Python nhất quán.
3. **Thêm `pre-commit`** — chạy lint trước commit để giảm noise PR.

### Trung hạn (khi có người dùng thật)
1. Lưu trữ Sổ Tay server-side (xem mục Hạn chế #1).
2. Thêm analytics nhẹ (Plausible/Umami) để biết bài nào được dùng nhiều.
3. Cache headers cho static assets (Nginx config đã có sẵn).

### Dài hạn (khi mở rộng)
1. Tách `lessons.json` ra DB nếu cần collaborative editing.
2. Thêm role giáo viên (xem dashboard kết quả lớp).
3. PWA — học sinh cài lên màn hình chính mobile.

## Lệnh smoke-test cuối cùng

```bash
# Local dev
make install && make test && make dev
# Sau đó mở http://localhost:8000

# Docker
make up && curl -sS http://localhost:8000/api/health
```

## Kết luận

Repo đã đạt **chuẩn MVP production-ready**: chạy được bằng 1 lệnh, có test,
có healthcheck, có Docker. Code clean, có docstring tiếng Việt, type hints
đầy đủ. Đủ tốt để bàn giao cho team kế tiếp tiếp quản và mở rộng.
