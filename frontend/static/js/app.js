/**
 * Bài Giảng AI — Frontend JS
 * Tính năng: lọc bài học theo module, search nhanh.
 */
(function () {
  'use strict';

  // Hook: ấn phím / để focus vào ô search (nếu có) — placeholder cho tương lai.
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
      const search = document.getElementById('lessonSearch');
      if (search) {
        e.preventDefault();
        search.focus();
      }
    }
  });

  // Cập nhật thông tin tự động nếu API health thay đổi
  async function refreshStatus() {
    try {
      const r = await fetch('/api/health');
      if (!r.ok) return;
      const data = await r.json();
      console.info('[Bài Giảng] API version:', data.version);
    } catch (err) {
      // Ngừng im lặng — không bắt buộc
    }
  }

  document.addEventListener('DOMContentLoaded', refreshStatus);
})();
