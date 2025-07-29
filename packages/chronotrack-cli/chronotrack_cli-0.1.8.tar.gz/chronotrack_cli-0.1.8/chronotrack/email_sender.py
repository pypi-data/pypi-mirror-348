import resend
import os
from dotenv import load_dotenv
from pathlib import Path



#  Load .env from priority order:
# 1. CWD/.chronotrack/.env
# 2. ~HOME/.chronotrack/.env (fallback)
# -----------------------------
project_env = Path.cwd() / ".chronotrack" / ".env"
home_env = Path.home() / ".chronotrack" / ".env"

if project_env.exists():
    load_dotenv(dotenv_path=project_env)
elif home_env.exists():
    load_dotenv(dotenv_path=home_env)

# Set API key from loaded env
resend.api_key = os.getenv("RESEND_API_KEY")

# -----------------------------
# 📍 Determine which .chronotrack folder to use
# (Always use CWD for logs and prefs!)
# -----------------------------
def get_project_data_dir():
    """
    Returns the `.chronotrack` folder in the current project (CWD).
    Creates it if it doesn't exist.
    """
    project_dir = Path.cwd() / ".chronotrack"
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


PREFS_FILE = get_project_data_dir() / "user_preferences.json"



def get_user_name():
    if PREFS_FILE.exists():
        try:
            with open(PREFS_FILE, "r") as f:
                prefs = json.load(f)
                return prefs.get("name", "ChronoTrack User")
        except Exception:
            pass
    return "ChronoTrack User"




def send_email_report(to_email: str, html_report_path: Path):
    """
    Sends the rendered ChronoTrack report to the user's email.
    Requires RESEND_API_KEY to be set in environment.
    """
    if not resend.api_key:
        print("❌ RESEND_API_KEY not set. Please check your environment.")
        return

    if not Path(html_report_path).exists():
        print(f"❌ Report file not found at {html_report_path}")
        return

    with open(html_report_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    user_name = get_user_name()

    try:
        response = resend.Emails.send({
            "from": "ChronoTrack <reports@mahirandnabiha.icu>",  # Must be a verified sender domain
            "to": [to_email],
            "subject": f"📊 Your Weekly ChronoTrack Report for {user_name}",
            "html": html_content,
        })
        print(f"✅ Email sent to {to_email}")
        return response
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return None
