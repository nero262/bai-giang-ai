"""FastAPI entrypoint — phục vụ slide HTML + REST API."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from .config import get_settings
from .lesson_repository import LessonRepository
from .models import HealthStatus, Lesson, LessonList
from .slide_fragment import parse_fragment


# Màu chấm sidebar cho từng module (giống style cũ trong các slide).
MODULE_COLORS: dict[str, str] = {
    "M1": "#10B981",
    "M2": "#3B82F6",
    "M3": "#F59E0B",
    "M4": "#F97316",
    "M5": "#A855F7",
    "M6": "#10B981",
}


def _group_lessons_by_module(lessons: list[Lesson]) -> dict[str, dict]:
    """Gom lessons theo module, giữ thứ tự xuất hiện. Trả dict[module_code -> {name, color, lessons}]."""
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


settings = get_settings()
repo = LessonRepository()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static + templates
if settings.STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# Mount slides static — học sinh truy cập trực tiếp file HTML qua /slides/<file>
if settings.SLIDES_DIR.exists():
    app.mount(
        "/slides-static",
        StaticFiles(directory=settings.SLIDES_DIR),
        name="slides-static",
    )

templates = (
    Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
    if settings.TEMPLATES_DIR.exists()
    else None
)


# ============================================================
# WEB ROUTES (HTML)
# ============================================================

@app.get("/", response_class=HTMLResponse, tags=["Web"])
async def home(request: Request) -> HTMLResponse:
    """Trang chủ — danh sách bài giảng."""
    if templates is None:
        return HTMLResponse(
            "<h1>Khóa AI 24 buổi</h1><p>Frontend templates chưa được cấu hình.</p>"
        )
    lessons = repo.list_all()
    # Convert Pydantic models → plain dicts cho Jinja2 groupby tương thích
    lessons_data = [l.model_dump() for l in lessons]
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "app_name": settings.APP_NAME,
            "lessons": lessons_data,
            "total_available": repo.count_available(),
            "total_lessons": len(lessons_data),
        },
    )


@app.get("/lesson/{slug}", response_class=HTMLResponse, tags=["Web"])
async def view_lesson(request: Request, slug: str):
    """Mở slide bài giảng theo slug — render lesson.html template với fragment được inject."""
    lesson = repo.get_by_slug(slug)
    if lesson is None:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy bài học: {slug}")
    if not lesson.available:
        raise HTTPException(status_code=404, detail="Bài học sắp ra mắt")

    file_path = settings.SLIDES_DIR / lesson.file
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"File slide không tồn tại: {lesson.file}",
        )

    # Template chưa cấu hình → fallback serve file thẳng (giữ cho dev không backend)
    if templates is None:
        return FileResponse(file_path, media_type="text/html")

    fragment = parse_fragment(file_path)
    all_lessons = repo.list_all()

    return templates.TemplateResponse(
        request,
        "lesson.html",
        {
            "current": lesson,
            "modules": _group_lessons_by_module(all_lessons),
            "total_lessons": len(all_lessons),
            "slide_content": fragment.slide_content,
            "lesson_style": fragment.lesson_style,
            "lesson_script": fragment.lesson_script,
            "notebook_config_json": fragment.notebook_config_json,
        },
    )


# ============================================================
# REST API
# ============================================================

@app.get("/api/health", response_model=HealthStatus, tags=["System"])
async def health() -> HealthStatus:
    """Healthcheck — phục vụ Docker / load balancer."""
    return HealthStatus(
        status="ok",
        version=settings.APP_VERSION,
        slides_available=repo.count_available(),
    )


@app.get("/api/lessons", response_model=LessonList, tags=["Lessons"])
async def list_lessons() -> LessonList:
    """Danh sách toàn bộ bài giảng."""
    items = repo.list_all()
    return LessonList(total=len(items), items=items)


@app.get("/api/lessons/{slug}", response_model=Lesson, tags=["Lessons"])
async def get_lesson(slug: str) -> Lesson:
    """Chi tiết một bài giảng."""
    lesson = repo.get_by_slug(slug)
    if lesson is None:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy: {slug}")
    return lesson


# ============================================================
# Local entrypoint
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
