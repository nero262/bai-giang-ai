"""Convert một file slide HTML đầy đủ thành fragment cho lesson.html template.

Cách dùng:
    python scripts/migrate_slide_to_fragment.py slides/buoi_01.html slides/buoi_06.html slides/buoi_07.html

Mỗi file sẽ được:
1. Đọc.
2. Backup sang <file>.legacy_<ts>.html.
3. Ghi lại dưới format fragment (chỉ chứa style+slides+nb-questions+optional lesson script).

Cấu trúc fragment đầu ra:
    <!-- header comment -->
    <style>...lesson-specific CSS gốc...</style>         (giữ nguyên để an toàn)
    <script type="application/json" id="nb-questions">{...}</script>
    <section class="slide ...">...</section> (× N)

Lesson-specific JS bị loại bỏ — toàn bộ slide engine / notebook / quiz / checklist /
drag-drop / flashcard-flip đều đã chuyển vào template `frontend/templates/lesson.html`.
Nếu phát hiện JS lạ (ngoài các function đã biết), script sẽ ghi nó vào
`<script>...</script>` ở cuối fragment để admin xem xét thủ công.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Tất cả tên function/biến mà template đã định nghĩa — không cần giữ trong fragment.
SHARED_JS_TOKENS = (
    "STORAGE_KEY", "CL_KEY",
    "loadNotebook", "saveNotebook", "loadChecklist", "saveChecklist",
    "SlideEngine", "slideEngine", "toggleSidebar",
    "NB_QUESTIONS", "initNotebookInputs", "openNotebook", "closeNotebook",
    "submitNotebook", "clearNotebook",
    "initChecklist", "updateClProgress",
    "gameDroppedCount", "gameTotal", "gameCorrect",
    "initGame", "handleDrop", "restartGame",
    "DOMContentLoaded",
    "classList.toggle('flipped')",  # generic flip in template
)


def extract_style(text: str) -> str:
    m = re.search(r"<style[^>]*>(.*?)</style>", text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def extract_slides(text: str) -> str:
    """Lấy mọi <section class=\"slide ...\">...</section>."""
    sections = re.findall(
        r'<section\s+class=["\'][^"\']*\bslide\b[^"\']*["\'][^>]*>.*?</section>',
        text,
        re.DOTALL | re.IGNORECASE,
    )
    return "\n\n".join(s.strip() for s in sections)


def extract_nb_questions(text: str) -> dict | None:
    m = re.search(r"const\s+NB_QUESTIONS\s*=\s*(\{.*?\});", text, re.DOTALL)
    if not m:
        return None
    raw = m.group(1)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def extract_lesson_specific_js(text: str) -> str:
    """Lấy <script>...</script>, sau đó bỏ tất cả function đã có trong template chung."""
    m = re.search(r"<script[^>]*>(.*?)</script>\s*</body>", text, re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    js = m.group(1)
    # Strip NB_QUESTIONS dòng (đã extract riêng)
    js = re.sub(r"const\s+NB_QUESTIONS\s*=\s*\{.*?\};", "", js, flags=re.DOTALL)

    # Tìm các block còn lại không nằm trong SHARED_JS_TOKENS
    leftover_lines = []
    for chunk in re.split(r"\n\s*\n", js):
        chunk_stripped = chunk.strip()
        if not chunk_stripped:
            continue
        if any(tok in chunk_stripped for tok in SHARED_JS_TOKENS):
            continue
        leftover_lines.append(chunk_stripped)
    return "\n\n".join(leftover_lines).strip()


def migrate(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "<html" not in text.lower():
        print(f"  → {path.name}: đã là fragment, bỏ qua.")
        return

    style = extract_style(text)
    slides = extract_slides(text)
    nb = extract_nb_questions(text)
    extra_js = extract_lesson_specific_js(text)

    # Lesson id từ tên file: buoi_07 → 7
    m = re.search(r"buoi_(\d+)", path.name)
    lesson_id = int(m.group(1)) if m else 0

    # Backup
    ts = time.strftime("%Y%m%d_%H%M%S")
    backup = path.with_suffix(f".legacy_{ts}.html")
    backup.write_text(text, encoding="utf-8")

    # Build fragment
    out = []
    out.append(
        f"<!--\n"
        f"  Slide fragment cho Buổi {lesson_id}.\n"
        f"  Chrome (sidebar/top-bar/slide-engine/notebook/quiz) đến từ\n"
        f"  frontend/templates/lesson.html. File này chỉ chứa nội dung slide,\n"
        f"  CSS riêng (nếu có), và cấu hình Sổ Tay.\n"
        f"-->"
    )
    if style:
        out.append("\n<style>\n" + style + "\n</style>")
    if nb:
        nb_json = json.dumps(nb, ensure_ascii=False, indent=2)
        out.append(
            '\n<script type="application/json" id="nb-questions">\n'
            + nb_json
            + "\n</script>"
        )
    out.append("\n" + slides)
    if extra_js:
        out.append("\n<script>\n" + extra_js + "\n</script>")

    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"  ✓ {path.name}: backup → {backup.name}, fragment {len(slides.split('</section>'))-1} slides")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python migrate_slide_to_fragment.py slides/buoi_XX.html [...]")
        return 1
    for arg in sys.argv[1:]:
        p = (ROOT / arg) if not Path(arg).is_absolute() else Path(arg)
        if not p.exists():
            print(f"  ✗ {p}: not found")
            continue
        migrate(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
