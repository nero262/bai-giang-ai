"""Parse một file slide fragment thành các phần để inject vào lesson.html template.

Fragment format (mỗi file slides/buoi_XX.html):

    <style>... lesson-specific CSS ...</style>          (tuỳ chọn)
    <script type="application/json" id="nb-questions">  (tuỳ chọn — câu hỏi Sổ Tay)
      { "1": {"title": "...", "q": "..."}, ... }
    </script>
    <section class="slide ..." data-slide="1" ...>...</section>
    <section class="slide ..." data-slide="2" ...>...</section>
    ...
    <script>... lesson-specific JS ...</script>          (tuỳ chọn)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


_RE_STYLE = re.compile(r"<style[^>]*>(.*?)</style>", re.DOTALL | re.IGNORECASE)
_RE_NB_JSON = re.compile(
    r'<script[^>]*type=["\']application/json["\'][^>]*id=["\']nb-questions["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)
_RE_NB_JSON_ALT = re.compile(
    r'<script[^>]*id=["\']nb-questions["\'][^>]*type=["\']application/json["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)
_RE_SECTIONS = re.compile(
    r'(<section\s+class=["\'][^"\']*\bslide\b[^"\']*["\'][^>]*>.*?</section>)',
    re.DOTALL | re.IGNORECASE,
)
_RE_INLINE_SCRIPT = re.compile(
    r"<script(?![^>]*\btype=)[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE
)


@dataclass
class SlideFragment:
    """Kết quả parse một file fragment."""

    lesson_style: str = ""
    lesson_script: str = ""
    slide_content: str = ""
    notebook_config: dict | None = None
    is_legacy: bool = False  # True nếu file vẫn là HTML đầy đủ (có <html>/<body>)

    @property
    def notebook_config_json(self) -> str:
        cfg = {"notebook_questions": self.notebook_config or {}}
        return json.dumps(cfg, ensure_ascii=False)


def parse_fragment(path: Path) -> SlideFragment:
    """Parse một slide file (fragment hoặc legacy) thành SlideFragment."""
    raw = path.read_text(encoding="utf-8")
    # Strip HTML comments — chúng có thể chứa <html>, <script>, <section> giả khiến
    # các regex bên dưới hiểu nhầm.
    text = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
    is_legacy = bool(
        re.search(r"<!DOCTYPE\s+html", text, re.IGNORECASE)
        or re.search(r"<body[\s>]", text, re.IGNORECASE)
    )

    if is_legacy:
        # Legacy: extract chỉ phần inside <div class="slides-container">
        m = re.search(
            r'<div[^>]*class=["\'][^"\']*\bslides-container\b[^"\']*["\'][^>]*>(.*?)</div>\s*<div[^>]*class=["\'][^"\']*\bnav-bar\b',
            text,
            re.DOTALL | re.IGNORECASE,
        )
        slide_content = m.group(1).strip() if m else ""
        # NB_QUESTIONS dạng JS object trong legacy
        nb = _extract_legacy_nb_questions(text)
        return SlideFragment(
            slide_content=slide_content,
            notebook_config=nb,
            is_legacy=True,
        )

    # Fragment mới
    style_match = _RE_STYLE.search(text)
    lesson_style = style_match.group(1).strip() if style_match else ""

    nb_match = _RE_NB_JSON.search(text) or _RE_NB_JSON_ALT.search(text)
    notebook_config: dict | None = None
    if nb_match:
        try:
            notebook_config = json.loads(nb_match.group(1))
        except json.JSONDecodeError:
            notebook_config = None

    sections = _RE_SECTIONS.findall(text)
    slide_content = "\n".join(sections)

    # Lesson-specific JS = bất kỳ <script> không có type=application/json
    scripts = _RE_INLINE_SCRIPT.findall(text)
    lesson_script = "\n".join(s.strip() for s in scripts if s.strip())

    return SlideFragment(
        lesson_style=lesson_style,
        lesson_script=lesson_script,
        slide_content=slide_content,
        notebook_config=notebook_config,
        is_legacy=False,
    )


def _extract_legacy_nb_questions(text: str) -> dict | None:
    """Cố gắng pull NB_QUESTIONS từ JS object trong legacy file."""
    m = re.search(r"const\s+NB_QUESTIONS\s*=\s*(\{.*?\});", text, re.DOTALL)
    if not m:
        return None
    raw = m.group(1)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None
