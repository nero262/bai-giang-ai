"""Test cơ bản cho các API endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    """/api/health phải trả về 200 và status=ok."""
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "slides_available" in data


def test_list_lessons() -> None:
    """/api/lessons trả danh sách có ít nhất 1 bài."""
    r = client.get("/api/lessons")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] >= 1
    assert isinstance(data["items"], list)


def test_get_lesson_existing() -> None:
    """Lấy được buổi 1."""
    r = client.get("/api/lessons/buoi_01")
    assert r.status_code == 200
    assert r.json()["slug"] == "buoi_01"


def test_get_lesson_404() -> None:
    """Slug không tồn tại trả 404."""
    r = client.get("/api/lessons/khong_co_buoi_nay")
    assert r.status_code == 404


def test_view_lesson_serves_html() -> None:
    """/lesson/buoi_01 phải serve HTML."""
    r = client.get("/lesson/buoi_01")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
