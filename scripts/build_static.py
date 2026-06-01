"""Build trang tĩnh từ template + lessons.json + fragment, xuất ra dist/.

Mục tiêu: deploy lên GitHub Pages (project site, sub-path /<repo>/) mà KHÔNG cần
chạy FastAPI. Reuse đúng template và logic của backend, chỉ khác là ghép fragment
vào template lúc BUILD rồi ghi ra file thay vì render lúc request.

Cách dùng:
    python scripts/build_static.py            # xuất ra ./dist
    python scripts/build_static.py --out _site # xuất ra thư mục khác

Kết quả:
    dist/
      .nojekyll
      index.html                 ← trang chủ
      static/...                 ← copy từ frontend/static
      lesson/buoi_XX.html        ← mỗi bài giảng available

Đường dẫn dùng RELATIVE để chạy đúng dưới sub-path GitHub Pages.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from jinja2 import Environment, FileSystemLoader, select_autoescape  # noqa: E402

from app.lesson_repository import LessonRepository  # noqa: E402
from app.rendering import group_lessons_by_module  # noqa: E402
from app.slide_fragment import parse_fragment  # noqa: E402

SLIDES_DIR = ROOT / "slides"
TEMPLATES_DIR = ROOT / "frontend" / "templates"
STATIC_DIR = ROOT / "frontend" / "static"
APP_NAME = "Khóa AI 24 buổi"


def build(out_dir: Path) -> None:
    repo = LessonRepository(SLIDES_DIR / "lessons.json")
    lessons = repo.list_all()
    available = [l for l in lessons if l.available]

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
    )
    index_tpl = env.get_template("index.html")
    lesson_tpl = env.get_template("lesson.html")

    # Dọn & tạo lại thư mục output
    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "lesson").mkdir(parents=True)

    # .nojekyll — để GitHub Pages không bỏ qua file/thư mục bắt đầu bằng "_"
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")

    # Copy static assets
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, out_dir / "static")

    # ---- Trang chủ (ở gốc dist) ----
    index_html = index_tpl.render(
        app_name=APP_NAME,
        lessons=[l.model_dump() for l in lessons],
        total_available=len(available),
        total_lessons=len(lessons),
        static_base="static",
        home_link="index.html",
        lesson_urls={l.slug: f"lesson/{l.slug}.html" for l in available},
        show_api_links=False,
    )
    (out_dir / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  + index.html ({len(available)}/{len(lessons)} buổi mở)")

    # ---- Mỗi bài giảng (trong dist/lesson/) ----
    modules = group_lessons_by_module(lessons)
    # Link giữa các bài: cùng thư mục lesson/ nên chỉ cần <slug>.html
    lesson_urls = {l.slug: f"{l.slug}.html" for l in available}

    for lesson in available:
        file_path = SLIDES_DIR / lesson.file
        if not file_path.exists():
            print(f"  ! bỏ qua {lesson.slug}: thiếu file {lesson.file}")
            continue
        fragment = parse_fragment(file_path)
        html = lesson_tpl.render(
            current=lesson,
            modules=modules,
            total_lessons=len(lessons),
            slide_content=fragment.slide_content,
            lesson_style=fragment.lesson_style,
            lesson_script=fragment.lesson_script,
            notebook_config_json=fragment.notebook_config_json,
            home_link="../index.html",
            lesson_urls=lesson_urls,
        )
        (out_dir / "lesson" / f"{lesson.slug}.html").write_text(html, encoding="utf-8")
        n = fragment.slide_content.count("<section")
        print(f"  + lesson/{lesson.slug}.html ({n} slides)")

    print(f"\n✓ Build xong → {out_dir}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build static site cho GitHub Pages")
    ap.add_argument("--out", default="dist", help="Thư mục output (mặc định: dist)")
    args = ap.parse_args()
    out_dir = (ROOT / args.out) if not Path(args.out).is_absolute() else Path(args.out)
    build(out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
