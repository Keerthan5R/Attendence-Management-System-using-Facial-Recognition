"""
app.py — Flask Web Dashboard for Attendance Records
======================================================
A modern web interface to browse, filter, and download attendance records.

Run:
    python app.py
    Open http://localhost:5000 in your browser.
"""

from flask import Flask, render_template_string, send_file, request, redirect, url_for
import os
import pandas as pd
import glob
from datetime import datetime

app = Flask(__name__)

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
ATTENDANCE_DIR = os.path.join(BASE_DIR, "Attendance")

# ─── HTML Template ────────────────────────────────────────────────────────────
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AMS Dashboard — Attendance Records</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', sans-serif;
      background: #0f0f1a;
      color: #f0f0f5;
      min-height: 100vh;
    }
    header {
      background: linear-gradient(135deg, #7c3aed, #06b6d4);
      padding: 28px 40px;
    }
    header h1 { font-size: 1.9rem; font-weight: 700; }
    header p  { font-size: 0.9rem; opacity: 0.85; margin-top: 4px; }
    .container { max-width: 1200px; margin: 0 auto; padding: 30px 20px; }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin-bottom: 30px;
    }
    .stat-card {
      background: #1e1e30;
      border-radius: 12px;
      padding: 20px;
      border-left: 4px solid #7c3aed;
      text-align: center;
    }
    .stat-card .val  { font-size: 2rem; font-weight: 700; color: #7c3aed; }
    .stat-card .lbl  { font-size: 0.85rem; color: #a0a0c0; margin-top: 4px; }
    .controls {
      display: flex;
      gap: 14px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 24px;
    }
    select, input[type=text] {
      background: #1e1e30;
      border: 1px solid #3a3a5c;
      color: #f0f0f5;
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 0.9rem;
      font-family: inherit;
    }
    .btn {
      padding: 10px 20px;
      border-radius: 8px;
      border: none;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
      transition: opacity 0.2s;
    }
    .btn:hover { opacity: 0.85; }
    .btn-primary  { background: #7c3aed; color: white; }
    .btn-success  { background: #22c55e; color: white; }
    .btn-outline  { background: transparent; border: 1px solid #7c3aed; color: #7c3aed; }
    table {
      width: 100%;
      border-collapse: collapse;
      background: #1e1e30;
      border-radius: 12px;
      overflow: hidden;
    }
    thead { background: #2a1a50; }
    th { padding: 14px 16px; text-align: left; font-weight: 600; font-size: 0.85rem; color: #c0a0ff; }
    td { padding: 13px 16px; font-size: 0.9rem; border-top: 1px solid #2a2a40; }
    tr:hover td { background: #252540; }
    .badge {
      display: inline-block;
      padding: 3px 12px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
    }
    .badge-present { background: #14532d; color: #4ade80; }
    .badge-absent  { background: #7f1d1d; color: #f87171; }
    .empty { text-align: center; padding: 60px; color: #666; }
    footer { text-align: center; padding: 20px; color: #555; font-size: 0.8rem; margin-top: 30px; }
  </style>
</head>
<body>
  <header>
    <h1>🎓 Attendance Management System</h1>
    <p>Facial Recognition Dashboard &nbsp;·&nbsp; Keerthan R &nbsp;·&nbsp; Gopalan College of Engineering</p>
  </header>

  <div class="container">
    <!-- Stats -->
    <div class="stats">
      <div class="stat-card">
        <div class="val">{{ total_records }}</div>
        <div class="lbl">Total Records</div>
      </div>
      <div class="stat-card">
        <div class="val">{{ total_students }}</div>
        <div class="lbl">Unique Students</div>
      </div>
      <div class="stat-card">
        <div class="val">{{ total_files }}</div>
        <div class="lbl">Session Files</div>
      </div>
    </div>

    <!-- Controls -->
    <form method="get" action="/">
      <div class="controls">
        <select name="file" id="file-select">
          <option value="">— All Sessions —</option>
          {% for f in files %}
          <option value="{{ f }}" {% if selected_file == f %}selected{% endif %}>{{ f }}</option>
          {% endfor %}
        </select>
        <input type="text" name="search" placeholder="🔍  Search name or enrollment..."
               value="{{ search }}" style="width:260px;">
        <button class="btn btn-primary" type="submit">Filter</button>
        {% if selected_file %}
        <a href="/download/{{ selected_file }}" class="btn btn-success">⬇ Download Excel</a>
        {% endif %}
        <a href="/" class="btn btn-outline">Reset</a>
      </div>
    </form>

    <!-- Table -->
    {% if records %}
    <table>
      <thead>
        <tr>
          <th>#</th>
          {% for col in columns %}
          <th>{{ col }}</th>
          {% endfor %}
        </tr>
      </thead>
      <tbody>
        {% for row in records %}
        <tr>
          <td>{{ loop.index }}</td>
          {% for val in row %}
          <td>
            {% if val == 'Present' %}
              <span class="badge badge-present">✅ Present</span>
            {% elif val == 'Absent' %}
              <span class="badge badge-absent">❌ Absent</span>
            {% else %}
              {{ val }}
            {% endif %}
          </td>
          {% endfor %}
        </tr>
        {% endfor %}
      </tbody>
    </table>
    {% else %}
    <div class="empty">
      <p>📭 No records found. Start marking attendance in AMS_Run.py.</p>
    </div>
    {% endif %}
  </div>

  <footer>
    Attendance Management System using Facial Recognition &nbsp;|&nbsp;
    TechSaksham — A Microsoft &amp; SAP Joint CSR Initiative
  </footer>
</body>
</html>
"""

# ─── Routes ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    files   = sorted(
        [f for f in os.listdir(ATTENDANCE_DIR) if f.endswith(".xlsx")],
        reverse=True
    ) if os.path.exists(ATTENDANCE_DIR) else []

    selected_file = request.args.get("file", "")
    search        = request.args.get("search", "").strip().lower()

    all_df = pd.DataFrame()

    if selected_file and selected_file in files:
        try:
            all_df = pd.read_excel(os.path.join(ATTENDANCE_DIR, selected_file))
        except Exception:
            all_df = pd.DataFrame()
    elif not selected_file and files:
        dfs = []
        for f in files:
            try:
                dfs.append(pd.read_excel(os.path.join(ATTENDANCE_DIR, f)))
            except Exception:
                pass
        if dfs:
            all_df = pd.concat(dfs, ignore_index=True)

    if search and not all_df.empty:
        mask = all_df.apply(
            lambda col: col.astype(str).str.lower().str.contains(search, na=False)
        ).any(axis=1)
        all_df = all_df[mask]

    records         = all_df.values.tolist() if not all_df.empty else []
    columns         = list(all_df.columns)   if not all_df.empty else []
    total_students  = all_df["Enrollment"].nunique() if "Enrollment" in all_df.columns else 0

    return render_template_string(
        TEMPLATE,
        files=files,
        selected_file=selected_file,
        search=search,
        records=records,
        columns=columns,
        total_records=len(records),
        total_students=total_students,
        total_files=len(files),
    )


@app.route("/download/<filename>")
def download(filename):
    filepath = os.path.join(ATTENDANCE_DIR, filename)
    if not os.path.exists(filepath):
        return "File not found", 404
    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    print("🌐 AMS Dashboard running at http://localhost:5000")
    app.run(debug=True, port=5000)
