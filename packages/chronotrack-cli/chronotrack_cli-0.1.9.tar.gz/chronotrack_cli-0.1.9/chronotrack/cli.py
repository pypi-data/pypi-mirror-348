import typer
import click
import webbrowser
from chronotrack.email_sender import send_email_report
from chronotrack.report_data import ReportBuilder
from chronotrack.generate_report import generate
from chronotrack.tracker import (
    start_session, stop_session, log_sessions,
    export_data, tags_view, week_log, resume_session, pause_session
)


app = typer.Typer(help="🕒 ChronoTrack — A simple CLI-based time tracker for developers and creators.")

# ---------------------------- Commands ----------------------------

@app.command()
def start(
    task: str = typer.Argument(..., help="Task name or description (in quotes if multi-word)"),
    tag: str = typer.Argument("General", help="Tag to categorize the task (default: General)")
):
    """
    🟢 Start tracking a new task.
    """
    start_session(task, tag)


@app.command()
def stop():
    """
    🔴 Stop the most recent active task.
    """
    stop_session()


@app.command()
def log(
    time_range: str = typer.Argument("today", help="Time window: today, yesterday, week, or all")
):
    """
    📜 Show a log of tracked tasks.
    """
    log_sessions(time_range)


@app.command()
def export(
    format: str = typer.Argument("json", help="Export format: json or csv")
):
    """
    💾 Export your task log to a file.
    """
    export_data(format)


@app.command()
def tags(
    tag_filter: str = typer.Argument(None, help="(Optional) View stats for a specific tag only")
):
    """
    🏷️  View tag-based summaries.
    """
    tags_view(tag_filter)


@app.command()
def week():
    """
    📊 View a 7-day summary of your work.
    """
    week_log()



@app.command()
def pause():
    """⏸️  Pause the active task to take a break."""
    pause_session()




@app.command()
def play():
    """▶️  Resume the task after a break."""
    resume_session()



import typer
import click
import webbrowser
from chronotrack.email_sender import send_email_report
from chronotrack.report_data import ReportBuilder
from chronotrack.generate_report import generate
from chronotrack.tracker import (
    start_session, stop_session, log_sessions,
    export_data, tags_view, week_log, resume_session, pause_session
)


app = typer.Typer(help="🕒 ChronoTrack — A simple CLI-based time tracker for developers and creators.")

# ---------------------------- Commands ----------------------------

@app.command()
def start(
    task: str = typer.Argument(..., help="Task name or description (in quotes if multi-word)"),
    tag: str = typer.Argument("General", help="Tag to categorize the task (default: General)")
):
    """
    🟢 Start tracking a new task.
    """
    start_session(task, tag)


@app.command()
def stop():
    """
    🔴 Stop the most recent active task.
    """
    stop_session()


@app.command()
def log(
    time_range: str = typer.Argument("today", help="Time window: today, yesterday, week, or all")
):
    """
    📜 Show a log of tracked tasks.
    """
    log_sessions(time_range)


@app.command()
def export(
    format: str = typer.Argument("json", help="Export format: json or csv")
):
    """
    💾 Export your task log to a file.
    """
    export_data(format)


@app.command()
def tags(
    tag_filter: str = typer.Argument(None, help="(Optional) View stats for a specific tag only")
):
    """
    🏷️  View tag-based summaries.
    """
    tags_view(tag_filter)


@app.command()
def week():
    """
    📊 View a 7-day summary of your work.
    """
    week_log()



@app.command()
def pause():
    """⏸️  Pause the active task to take a break."""
    pause_session()




@app.command()
def play():
    """▶️  Resume the task after a break."""
    resume_session()



@click.group()
def cli():
    pass




@app.command()
def report(preview: bool = typer.Option(False, "--preview", help="Preview the report in browser."),
           email: str = typer.Option(None, "--email", help="Email to send report to.")):
    """📑 Generate weekly report (with preview and/or email)."""
    builder = ReportBuilder()
    report_data = builder.build_full_report()
    html_path = generate(report_data)

    if preview:
        webbrowser.open(f"file://{html_path}")

    if email:
        send_email_report(email, html_path)





import typer
from datetime import datetime, timedelta
import json
from pathlib import Path
import time
import threading
from chronotrack.report_data import ReportBuilder
from chronotrack.generate_report import generate
from chronotrack.email_sender import send_email_report

SETTINGS_FILE = Path("user_preferences.json")



# Helper: Save user preferences
def save_preferences(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Helper: Load preferences (if any)
def load_preferences():
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return None


from pathlib import Path
from datetime import datetime
import typer
import os
import json

from chronotrack.utils import save_preferences


@app.command()
def setup_email_schedule():
    """⚙️ Setup auto-reporting frequency and email."""
    typer.echo("\n📧 Let's set up your email report schedule!")

    # Step 1: Get user inputs
    email = typer.prompt("📨 Enter the recipient email address")
    name = typer.prompt("🙋‍♂️ Enter your name")
    sender_domain = typer.prompt("🌐 Enter your verified sender domain (e.g., reports@yourdomain.com)")

    typer.echo("\n📅 How often should we send the report?")
    typer.echo("Options: daily, weekly, every 2 days, every 3 days, etc.")
    frequency = typer.prompt("Enter frequency (e.g., daily, 2, 3, weekly)").lower().strip()

    # Step 2: Convert frequency to number of days
    if frequency == "daily":
        days = 1
    elif frequency == "weekly":
        days = 7
    elif frequency.isdigit():
        days = int(frequency)
    else:
        typer.echo("❌ Invalid input. Please enter 'daily', 'weekly', or a number of days.")
        raise typer.Exit()

    # Step 3: Ask for API key
    api_key = typer.prompt("🔑 Enter your Resend API key (from your Resend dashboard)")

    # Step 4: Save to CWD/.chronotrack/.env
    env_path = Path.cwd() / ".chronotrack" / ".env"
    env_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    if env_path.exists():
        with open(env_path, "r") as f:
            lines = f.readlines()
        # Remove old values if they exist
        lines = [
            line for line in lines
            if not line.startswith("RESEND_API_KEY=")
            and not line.startswith("DOMAIN_NAME=")
        ]

    lines.append(f"RESEND_API_KEY={api_key}\n")
    lines.append(f"DOMAIN_NAME={sender_domain}\n")

    with open(env_path, "w") as f:
        f.writelines(lines)

    typer.echo(f"🔐 API key and domain saved to {env_path}")

    # Step 5: Save user preferences (name, email, days, last sent)
    preferences = {
        "name": name,
        "email": email,
        "days": days,
        "last_sent": datetime.now().isoformat()
    }

    save_preferences(preferences)

    typer.echo(f"\n✅ Reports will be sent every {days} day(s) to {email}")



# Background worker that checks if it's time to send a report
def report_scheduler():
    while True:
        prefs = load_preferences()
        if prefs:
            last_sent = datetime.fromisoformat(prefs["last_sent"])
            interval = timedelta(days=prefs["days"])
            now = datetime.now()

            if now - last_sent >= interval:
                typer.echo("\n📤 Time to send scheduled report!")
                builder = ReportBuilder()
                report_data = builder.build_full_report()
                html_path = generate(report_data)
                try:
                    send_email_report(prefs["email"], html_path)
                    prefs["last_sent"] = datetime.now().isoformat()
                    save_preferences(prefs)
                    typer.echo(f"✅ Report sent to {prefs['email']}")
                except Exception as e:
                    typer.echo(f"❌ Failed to send report: {e}")

        time.sleep(3600)  # Check every hour


@app.command()
def launch_scheduler():
    """🚀 Launch background scheduler (run this to keep reports going)."""
    typer.echo("\n🌀 Starting background scheduler to auto-send reports...")
    threading.Thread(target=report_scheduler, daemon=True).start()
    typer.echo("⏳ Running... Press Ctrl+C to stop.")
    while True:
        time.sleep(1)










# ------------------------------------------------------------------

if __name__ == "__main__":
    app()
