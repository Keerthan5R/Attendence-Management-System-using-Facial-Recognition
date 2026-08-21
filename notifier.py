"""
notifier.py — Email Notification Module
=========================================
Sends an email alert when a student's attendance is marked.
Credentials are loaded from a .env file (never hardcoded).

Setup:
    1. Copy .env.example to .env
    2. Fill in your Gmail address and App Password
       (Enable 2FA on Gmail, then generate an App Password)
    3. Set NOTIFY_RECIPIENT to the email that should receive alerts

Usage (from AMS_Run.py):
    from notifier import send_attendance_email
    send_attendance_email("John", "Mathematics", "2024-12-07", "09:30:00")
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

SMTP_HOST  = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT  = int(os.getenv("SMTP_PORT", 587))
SENDER     = os.getenv("NOTIFY_SENDER", "")
PASSWORD   = os.getenv("NOTIFY_PASSWORD", "")
RECIPIENT  = os.getenv("NOTIFY_RECIPIENT", "")


def send_attendance_email(
    student_name: str,
    subject: str,
    date: str,
    time_val: str
) -> bool:
    """
    Send an email notification when attendance is marked.

    Args:
        student_name: Full name of the student.
        subject:      Subject/class for which attendance is marked.
        date:         Date string (YYYY-MM-DD).
        time_val:     Time string (HH:MM:SS).

    Returns:
        True if email was sent successfully, False otherwise.
    """
    if not all([SENDER, PASSWORD, RECIPIENT]):
        print("[NOTIFY] Email credentials not configured. Skipping notification.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"✅ Attendance Marked — {student_name} | {subject}"
    msg["From"]    = SENDER
    msg["To"]      = RECIPIENT

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:20px;">
      <div style="max-width:500px; margin:auto; background:white; border-radius:10px;
                  padding:30px; box-shadow:0 2px 10px rgba(0,0,0,0.1);">
        <h2 style="color:#7c3aed; margin-bottom:4px;">🎓 Attendance Notification</h2>
        <p style="color:#666; font-size:13px; margin-top:0;">
          Attendance Management System — Facial Recognition
        </p>
        <hr style="border:1px solid #e8e8e8;">
        <table style="width:100%; font-size:15px; color:#333;">
          <tr><td><strong>👤 Student</strong></td><td>{student_name}</td></tr>
          <tr><td><strong>📚 Subject</strong></td><td>{subject}</td></tr>
          <tr><td><strong>📅 Date</strong></td><td>{date}</td></tr>
          <tr><td><strong>⏰ Time</strong></td><td>{time_val}</td></tr>
          <tr><td><strong>✅ Status</strong></td><td style="color:#22c55e;">Present</td></tr>
        </table>
        <hr style="border:1px solid #e8e8e8;">
        <p style="font-size:12px; color:#999; text-align:center;">
          Automated notification from AMS — Gopalan College of Engineering
        </p>
      </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, RECIPIENT, msg.as_string())
        print(f"[NOTIFY] Email sent to {RECIPIENT} for {student_name}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("[NOTIFY] SMTP Auth failed — check NOTIFY_SENDER and NOTIFY_PASSWORD in .env")
    except Exception as e:
        print(f"[NOTIFY] Email failed: {e}")
    return False


if __name__ == "__main__":
    # Quick test
    ok = send_attendance_email("Keerthan R", "Mathematics", "2024-12-07", "09:30:00")
    print("✅ Test email sent!" if ok else "❌ Test email failed.")
