"""Pydantic models cho API."""

from __future__ import annotations

from typing import Optional, List
from pydantic import BaseModel, Field


class Lesson(BaseModel):
    """Một bài giảng trong khóa."""

    id: int = Field(..., description="Số thứ tự bài học (1..N)")
    slug: str = Field(..., description="Mã định danh URL-safe, ví dụ: buoi_01")
    title: str = Field(..., description="Tiêu đề bài giảng")
    module: str = Field(..., description="Mã module, ví dụ: M1")
    module_name: str = Field(..., description="Tên module")
    duration_min: int = Field(120, description="Thời lượng (phút)")
    file: str = Field(..., description="Tên file HTML trong thư mục slides/")
    available: bool = Field(True, description="Đã có nội dung hay chưa")
    description: Optional[str] = Field(None, description="Mô tả ngắn")
    tags: List[str] = Field(default_factory=list, description="Từ khóa")


class LessonList(BaseModel):
    """Danh sách bài giảng."""

    total: int
    items: List[Lesson]


class HealthStatus(BaseModel):
    """Trạng thái dịch vụ."""

    status: str = "ok"
    version: str
    slides_available: int
