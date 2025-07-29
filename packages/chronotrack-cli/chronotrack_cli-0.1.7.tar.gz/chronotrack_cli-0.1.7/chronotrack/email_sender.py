import resend
import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_email_report(to_email: str, html_report_path: Path):
    with open(html_report_path, "r") as f:
        html_content = f.read()

    try:
        response = resend.Emails.send({
            "from": "ChronoTrack <reports@mahirandnabiha.icu>",  # You must verify this sender in Resend
            "to": [to_email],
            "subject": "📊 Your Weekly ChronoTrack Report",
            "html": html_content,
        })
        print(f"✅ Email sent to {to_email}")
        return response
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return None