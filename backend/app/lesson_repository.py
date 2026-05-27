"""Đọc/quản lý danh sách bài giảng từ file lessons.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from .config import get_settings
from .models import Lesson


class LessonRepository:
    """Đọc danh sách bài giảng từ file JSON (đơn giản, không cần DB)."""

    def __init__(self, index_path: Optional[Path] = None) -> None:
        self.settings = get_settings()
        self.index_path = index_path or self.settings.LESSONS_INDEX

    def _load(self) -> List[Lesson]:
        if not self.index_path.exists():
            return []
        with self.index_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Lesson(**item) for item in raw]

    def list_all(self) -> List[Lesson]:
        """Trả toàn bộ danh sách bài học (đã sort theo id)."""
        return sorted(self._load(), key=lambda x: x.id)

    def get_by_slug(self, slug: str) -> Optional[Lesson]:
        for lesson in self._load():
            if lesson.slug == slug:
                return lesson
        return None

    def get_by_id(self, lesson_id: int) -> Optional[Lesson]:
        for lesson in self._load():
            if lesson.id == lesson_id:
                return lesson
        return None

    def count_available(self) -> int:
        return sum(1 for l in self._load() if l.available)
