# =====================================================================
# Bài Giảng AI — Makefile
# Lệnh nhanh cho dev & deploy
# Dùng: make help
# =====================================================================
.PHONY: help install dev test build build-static serve-static up down logs restart clean

help: ## Hiện danh sách lệnh
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "} {printf "  %-12s %s\n", $$1, $$2}'

install: ## Cài dependencies (Python venv + pip)
	cd backend && python3 -m venv .venv && \
		. .venv/bin/activate && pip install -r requirements.txt

dev: ## Chạy dev server (hot-reload, port 8000)
	@bash scripts/run_dev.sh

test: ## Chạy unit tests
	@bash scripts/run_test.sh

build: ## Build Docker image
	docker compose build

build-static: ## Build bản tĩnh cho GitHub Pages → dist/
	python3 scripts/build_static.py --out dist

serve-static: build-static ## Build rồi xem thử bản tĩnh tại http://127.0.0.1:8080
	@echo "→ http://127.0.0.1:8080"
	@cd dist && python3 -m http.server 8080

up: ## Khởi động container (production)
	docker compose up -d
	@echo "→ http://localhost:8000"

down: ## Dừng container
	docker compose down

logs: ## Xem logs realtime
	docker compose logs -f app

restart: ## Restart container
	docker compose restart app

clean: ## Dọn cache, __pycache__, .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
