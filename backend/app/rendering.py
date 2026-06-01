"""Logic render dùng chung cho cả server (FastAPI) lẫn static build script.

Tách riêng khỏi main.py để scripts/build_static.py import được mà không kéo theo
FastAPI/uvicorn.
"""

from __future__ import annotations

from typing import List

from .models import Lesson


# Màu chấm sidebar cho từng module (đồng bộ với style các slide).
MODULE_COLORS: dict[str, str] = {
    "M1": "#10B981",
    "M2": "#3B82F6",
    "M3": "#F59E0B",
    "M4": "#F97316",
    "M5": "#A855F7",
    "M6": "#10B981",
}


def group_lessons_by_module(lessons: List[Lesson]) -> dict[str, dict]:
    """Gom lessons theo module, giữ thứ tự xuất hiện.

    Trả dict[module_code -> {name, color, lessons}].
    """
    modules: dict[str, dict] = {}
    for l in lessons:
        bucket = modules.setdefault(
            l.module,
            {
                "name": l.module_name,
                "color": MODULE_COLORS.get(l.module, "#2563EB"),
                "lessons": [],
            },
        )
        bucket["lessons"].append(l)
    return modules
