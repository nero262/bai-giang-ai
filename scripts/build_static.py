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

    # Copy thư mục ảnh của slide (vd: slides/buoi_02_images/) → dist/lesson/<tên>/
    # Slide HTML tham chiếu ảnh bằng đường dẫn TƯƠNG ĐỐI (vd "buoi_02_images/x.png"),
    # nên ảnh phải nằm cạnh file lesson/<slug>.html mới hiển thị trên GitHub Pages.
    for img_dir in sorted(SLIDES_DIR.glob("*_images")):
        if img_dir.is_dir():
            shutil.copytree(img_dir, out_dir / "lesson" / img_dir.name)
            n_img = sum(1 for _ in img_dir.iterdir())
            print(f"  + lesson/{img_dir.name}/ ({n_img} ảnh)")

    # Copy file game/standalone đi kèm slide (vd: slides/buoi_06_game.html) → dist/lesson/<tên>.html
    # Slide tham chiếu bằng đường dẫn TƯƠNG ĐỐI (vd "buoi_06_game.html"), nên file phải
    # nằm cạnh lesson/<slug>.html mới mở được trên GitHub Pages.
    for game_file in sorted(SLIDES_DIR.glob("buoi_*_game.html")):
        shutil.copy2(game_file, out_dir / "lesson" / game_file.name)
        print(f"  + lesson/{game_file.name}")

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

        # File là trang HTML standalone (vd game escape room) → copy thẳng, KHÔNG
        # nhúng vào template slide. Phải khớp logic của backend (main.py view_lesson):
        # fragment thường chỉ gồm <section class="slide"> nên không có <!doctype>/<html>.
        _head = file_path.read_text(encoding="utf-8", errors="ignore")[:800].lower()
        if "<!doctype html" in _head or "<html" in _head:
            shutil.copy2(file_path, out_dir / "lesson" / f"{lesson.slug}.html")
            print(f"  + lesson/{lesson.slug}.html (standalone, copy thẳng)")
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
