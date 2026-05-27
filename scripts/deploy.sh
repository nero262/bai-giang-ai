#!/usr/bin/env bash
# Deploy với Docker Compose
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

if [ ! -f ".env" ]; then
  echo "[setup] Không có .env — copy từ .env.example"
  cp .env.example .env
fi

echo "[deploy] Build image..."
docker compose build

echo "[deploy] Khởi động container..."
docker compose up -d

echo "[deploy] Đợi healthcheck..."
sleep 5
docker compose ps

echo "[deploy] Xong! Mở http://localhost:8000"
