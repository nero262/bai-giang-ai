"""Cấu hình ứng dụng — đọc từ biến môi trường (12-factor)."""

from __future__ import annotations

from pathlib import Path
from functools import lru_cache
import os


# Project root = .../bai_giang
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings:
    """Cấu hình runtime. Có thể override qua biến môi trường."""

    # App metadata
    APP_NAME: str = os.getenv("APP_NAME", "Khóa AI 24 buổi")
    APP_DESCRIPTION: str = os.getenv(
        "APP_DESCRIPTION",
        "Nền tảng phục vụ bài giảng AI tương tác cho học sinh.",
    )
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Paths
    PROJECT_ROOT: Path = PROJECT_ROOT
    SLIDES_DIR: Path = PROJECT_ROOT / "slides"
    FRONTEND_DIR: Path = PROJECT_ROOT / "frontend"
    STATIC_DIR: Path = FRONTEND_DIR / "static"
    TEMPLATES_DIR: Path = FRONTEND_DIR / "templates"
    LESSONS_INDEX: Path = PROJECT_ROOT / "slides" / "lessons.json"

    # CORS — mở rộng khi cần
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton cấu hình."""
    return Settings()
