/**
 * Sổ Tay Cá Nhân — Google Apps Script Web App
 * ---------------------------------------------------------------
 * Nhận POST từ frontend (GitHub Pages), append/update 1 hàng vào
 * Google Sheet "responses". Giáo viên mở Sheet → File → Download → .xlsx
 * khi cần lưu offline.
 *
 * SETUP (xem README.md cùng thư mục):
 *   1. Tạo Google Sheet mới, đổi tên sheet đầu thành "responses".
 *   2. Copy Sheet ID từ URL: docs.google.com/spreadsheets/d/<SHEET_ID>/edit
 *   3. Vào script.google.com → New project → dán file này vào.
 *   4. Thay SHEET_ID bên dưới.
 *   5. Deploy → New deployment → Type: Web app
 *        - Execute as: Me
 *        - Who has access: Anyone
 *      → copy URL https://script.google.com/macros/s/.../exec
 *   6. Dán URL đó vào <meta name="notebook-endpoint" content="..."> trong lesson.html
 */

// ====== CẤU HÌNH ======
const SHEET_ID   = 'PASTE_SHEET_ID_HERE';
const SHEET_NAME = 'responses';

// Cột cố định (đứng trước cặp Q/A động)
const FIXED_HEADERS = [
  'timestamp_server', 'submitted_at_client',
  'lesson_id', 'lesson_slug',
  'student_name', 'student_class',
  'client_id'
];
const TAIL_HEADERS = ['user_agent'];

// ====== ENTRYPOINT ======
function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return jsonOut({ ok: false, error: 'EMPTY_BODY' });
    }
    const data = JSON.parse(e.postData.contents);

    // Validate cơ bản
    if (!data.client_id) return jsonOut({ ok: false, error: 'MISSING_CLIENT_ID' });
    if (!data.lesson_id) return jsonOut({ ok: false, error: 'MISSING_LESSON_ID' });
    if (!data.student_name || !String(data.student_name).trim()) {
      return jsonOut({ ok: false, error: 'MISSING_STUDENT_NAME' });
    }

    const sheet = openOrCreateSheet();

    // Build cặp câu hỏi/đáp án theo thứ tự key của questions
    const questions = data.questions || {};
    const answers   = data.answers || {};
    const qKeys     = Object.keys(questions).sort((a, b) => Number(a) - Number(b));

    const qaHeaders = [];
    const qaValues  = [];
    qKeys.forEach(k => {
      const info = questions[k] || {};
      qaHeaders.push('q' + k + '_title', 'q' + k + '_question', 'q' + k + '_answer');
      qaValues.push(
        String(info.title || ''),
        String(info.q || ''),
        String(answers[k] || '')
      );
    });

    // Đảm bảo header row đầy đủ (mở rộng nếu lesson sau có nhiều câu hơn)
    ensureHeaders(sheet, qaHeaders);

    // Build hàng theo đúng thứ tự cột hiện tại của sheet
    const headerRow = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    const row = buildRow(headerRow, {
      timestamp_server:    new Date().toISOString(),
      submitted_at_client: String(data.submitted_at || ''),
      lesson_id:           Number(data.lesson_id) || data.lesson_id,
      lesson_slug:         String(data.lesson_slug || ''),
      student_name:        String(data.student_name).trim().slice(0, 120),
      student_class:       String(data.student_class || '').trim().slice(0, 40),
      client_id:           String(data.client_id),
      user_agent:          String(data.user_agent || '').slice(0, 300)
    }, qKeys, questions, answers);

    // Idempotent: nếu (client_id, lesson_id) đã có thì UPDATE
    const existingRow = findExistingRow(sheet, headerRow, data.client_id, data.lesson_id);
    if (existingRow > 0) {
      sheet.getRange(existingRow, 1, 1, row.length).setValues([row]);
      return jsonOut({ ok: true, action: 'update', row: existingRow });
    } else {
      sheet.appendRow(row);
      return jsonOut({ ok: true, action: 'insert', row: sheet.getLastRow() });
    }
  } catch (err) {
    return jsonOut({ ok: false, error: String(err && err.message || err) });
  }
}

// Cho phép check health bằng GET (mở URL trong trình duyệt).
function doGet() {
  return jsonOut({ ok: true, service: 'so-tay-phan-hoi', sheet: SHEET_NAME });
}

// ====== HELPERS ======
function jsonOut(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function openOrCreateSheet() {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    const initial = FIXED_HEADERS.concat(TAIL_HEADERS);
    sheet.getRange(1, 1, 1, initial.length).setValues([initial]);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, initial.length).setFontWeight('bold').setBackground('#EEF2FF');
  }
  return sheet;
}

function ensureHeaders(sheet, qaHeaders) {
  const lastCol = sheet.getLastColumn();
  const current = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
  const missing = qaHeaders.filter(h => current.indexOf(h) === -1);
  if (!missing.length) return;

  // Chèn qa headers ngay TRƯỚC tail headers (user_agent ở cuối)
  const tailStart = current.indexOf(TAIL_HEADERS[0]);
  if (tailStart === -1) {
    // user_agent chưa có → append tất cả vào cuối
    sheet.getRange(1, lastCol + 1, 1, missing.length + TAIL_HEADERS.length)
         .setValues([missing.concat(TAIL_HEADERS)])
         .setFontWeight('bold').setBackground('#EEF2FF');
    return;
  }
  // Insert columns trước tail
  sheet.insertColumnsBefore(tailStart + 1, missing.length);
  sheet.getRange(1, tailStart + 1, 1, missing.length)
       .setValues([missing])
       .setFontWeight('bold').setBackground('#EEF2FF');
}

function buildRow(headerRow, fixed, qKeys, questions, answers) {
  return headerRow.map(h => {
    if (Object.prototype.hasOwnProperty.call(fixed, h)) return fixed[h];
    // qN_title / qN_question / qN_answer
    const m = /^q(\d+)_(title|question|answer)$/.exec(h);
    if (m) {
      const k = m[1];
      const kind = m[2];
      const info = questions[k] || {};
      if (kind === 'title')    return String(info.title || '');
      if (kind === 'question') return String(info.q || '');
      if (kind === 'answer')   return String(answers[k] || '');
    }
    return '';
  });
}

function findExistingRow(sheet, headerRow, clientId, lessonId) {
  const cidCol = headerRow.indexOf('client_id') + 1;
  const lidCol = headerRow.indexOf('lesson_id') + 1;
  if (cidCol < 1 || lidCol < 1) return -1;
  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return -1;
  const range = sheet.getRange(2, 1, lastRow - 1, sheet.getLastColumn()).getValues();
  for (let i = 0; i < range.length; i++) {
    if (String(range[i][cidCol - 1]) === String(clientId)
        && String(range[i][lidCol - 1]) === String(lessonId)) {
      return i + 2; // +2 vì row index 1-based và bỏ header
    }
  }
  return -1;
}
