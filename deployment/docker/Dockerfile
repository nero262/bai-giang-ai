# =====================================================================
# Bài Giảng AI — Production Dockerfile
# Base: Python 3.12 slim — nhỏ, đủ dùng cho FastAPI
# =====================================================================
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Cài đặt dependencies hệ thống tối thiểu
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------- Builder ----------
FROM base AS builder
WORKDIR /install
COPY backend/requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

# ---------- Runtime ----------
FROM base AS runtime

# Tạo user không phải root cho bảo mật
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app/bai_giang

# Copy thư viện từ builder
COPY --from=builder --chown=app:app /root/.local /home/app/.local
ENV PATH=/home/app/.local/bin:$PATH

# Copy source code
COPY --chown=app:app backend ./backend
COPY --chown=app:app frontend ./frontend
COPY --chown=app:app slides ./slides

WORKDIR /home/app/bai_giang/backend

# Healthcheck cho container orchestration
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -fsS http://localhost:8000/api/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
