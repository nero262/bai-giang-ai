#!/usr/bin/env bash
# Chạy backend FastAPI ở chế độ dev (hot-reload)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}/backend"

# Tạo venv nếu chưa có
if [ ! -d ".venv" ]; then
  echo "[setup] Tạo virtualenv..."
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "[setup] Cài dependencies..."
pip install -q -r requirements.txt

echo "[run] Khởi động FastAPI tại http://127.0.0.1:8000"
echo "[run]   API docs: http://127.0.0.1:8000/api/docs"
DEBUG=true uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
