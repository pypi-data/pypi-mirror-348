import json
import csv
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import track
from rich import box

from chronotrack.utils import (
    format_pretty_time,
    is_active_session,
    is_paused_session,
    calculate_duration_minutes,
    start_break,
    end_break
)


LOG_FILE = Path("session_log.json")

def start_session(task: str, tag: str = "General"):
    start_time = datetime.now().isoformat()

    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    if data and is_active_session(data[-1]):
        last = data[-1]
        task = last.get("task", "Unnamed")
        print(f"⚠️ Cannot start new session — task '{task}' started at {format_pretty_time(last['start'])} is still active.")
        return

    entry = {
        "task": task,
        "tag": tag,
        "start": start_time
    }

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"🟢 Started: {task} | 🏷️  {tag} | ⏰ {format_pretty_time(start_time)}")




def stop_session():
    if not LOG_FILE.exists():
        print("⚠️ No session log found.")
        return

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    if not data or not is_active_session(data[-1]):
        print("⚠️ No active session to stop.")
        return

    session = data[-1]

    # Finalize break if paused
    if is_paused_session(session):
        end_break(session)

    # Always include breaks field, even if empty
    if "breaks" not in session:
        session["breaks"] = []

    session["total_breaks"] = len(session["breaks"])


    end_time = datetime.now()
    session["end"] = end_time.isoformat()

    break_time = sum(b.get("duration_minutes", 0) for b in session.get("breaks", [])) if "breaks" in session else 0
    session["duration_minutes"] = calculate_duration_minutes(session["start"], session["end"]) - break_time
    session["total_break_time"] = round(break_time, 2)


    note = Prompt.ask("📝 Add a note for this session (type '/' to skip)", default="/")
    session["note_added"] = note.strip() != "/"
    if session["note_added"]:
        session["note"] = note.strip()

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"🔴 Stopped: {session['task']} | ⏰ {session['duration_minutes']} min | ☕️ {round(break_time, 2)} min")





def log_sessions(time_range="today"):
    if not LOG_FILE.exists():
        print("📭 No session log found.")
        return

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    now = datetime.now()
    filtered = []

    for session in data:
        start_str = session.get("start")
        if not start_str:
            continue
        start_time = datetime.fromisoformat(start_str)

        # Filter based on time_range
        if time_range == "today":
            if start_time.date() != now.date():
                continue
        elif time_range == "yesterday":
            if start_time.date() != (now.date() - timedelta(days=1)):
                continue
        elif time_range == "week":
            if (now - start_time).days > 7:
                continue
        elif time_range == "all":
            pass
        else:
            print("❌ Invalid time range. Use: today, yesterday, week, or all")
            return

        filtered.append(session)

    if not filtered:
        print("📭 No tasks for selected range.")
        return

    title_map = {
        "today": "Today's Log",
        "yesterday": "Yesterday's Log",
        "week": "This Week's Log",
        "all": "All Time Log"
    }

    table = Table(title=f"📜 ChronoTrack – {title_map[time_range]}")

    table.add_column("Task", style="cyan", no_wrap=True)
    table.add_column("Tag", style="magenta")
    table.add_column("Start", style="green")
    table.add_column("End", style="red")
    table.add_column("Duration (min)", justify="right", style="yellow")

    for session in filtered:
        task = session["task"]
        tag = session.get("tag", "—")

        start_time = datetime.fromisoformat(session["start"])
        start_fmt = start_time.strftime("%I:%M %p")  # e.g., 09:45 AM

        end_str = session.get("end")
        if end_str:
            end_time = datetime.fromisoformat(end_str)
            end_fmt = end_time.strftime("%I:%M %p")
        else:
            end_fmt = "—"

        duration = str(session.get("duration_minutes", "—"))

        table.add_row(task, tag, start_fmt, end_fmt, duration)

    console = Console()
    console.print(table)










def export_data(format: str = "json"):
    if not LOG_FILE.exists():
        print("❌ No session log to export.")
        return

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    if not data:
        print("⚠️ Log file is empty.")
        return

    if format == "json":
        with open("export.json", "w") as f:
            json.dump(data, f, indent=4)
        print("✅ Exported as export.json")

    elif format == "csv":
        fieldnames = list(data[0].keys())  # Ensure consistent header order
        with open("export.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print("✅ Exported as export.csv")

    else:
        print("❌ Unsupported format. Use --format json or --format csv.")







def tags_view(tag_filter=None):
    if not LOG_FILE.exists():
        print("📭 No tasks logged yet.")
        return

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    tag_stats = defaultdict(lambda: {"count": 0, "duration": 0.0})

    for session in data:
        tag = session.get("tag", "Uncategorized")
        tag_stats[tag]["count"] += 1

        if "duration_minutes" in session:
            tag_stats[tag]["duration"] += session["duration_minutes"]

    if not tag_stats:
        print("📭 No tag data available.")
        return

    table = Table(title="🏷️ Tag Summary")

    table.add_column("Tag", style="cyan")
    table.add_column("Sessions", justify="right", style="magenta")
    table.add_column("Total Time (min)", justify="right", style="green")

    for tag, stats in tag_stats.items():
        if tag_filter and tag_filter != tag:
            continue
        table.add_row(tag, str(stats["count"]), f"{round(stats['duration'], 2)}")

    console = Console()
    console.print(table)






# chronotrack/tracker.py

def week_log():
    console = Console()

    if not LOG_FILE.exists():
        console.print("\n[bold red]No log file found.[/bold red]\n")
        return

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    now = datetime.now()
    week_ago = now - timedelta(days=6)  # Last 7 days inclusive

    filtered = [s for s in data if "start" in s and datetime.fromisoformat(s["start"]).date() >= week_ago.date()]

    if not filtered:
        console.print("\n[bold red]No tasks found in the last 7 days.[/bold red]\n")
        return

    if len(filtered) < 5:
        console.print("\n[bold yellow]⚠ Not enough tasks to compute full week stats (found < 5). Showing partial data.[/bold yellow]\n")

    console.print(f"\n[bold green]📆 Week Log: {week_ago.strftime('%a, %b %d')} — {now.strftime('%a, %b %d')}[/bold green]\n")

    console.print("[bold]Choose a report mode:[/bold]")
    console.print("[cyan]1.[/cyan] Heat map")
    console.print("[cyan]2.[/cyan] Overall summary")
    console.print("[cyan]3.[/cyan] Quantitative metrics")
    console.print("[cyan]4.[/cyan] Tag analysis")
    console.print("[cyan]5.[/cyan] All of the above")

    mode_choice = Prompt.ask("Enter 1-5", choices=["1", "2", "3", "4", "5"], default="2")

    if mode_choice == "1":
        _week_heatmap(console, filtered)
    elif mode_choice == "2":
        _week_overall(console, filtered)
    elif mode_choice == "3":
        _week_quant(console, filtered)
    elif mode_choice == "4":
        _week_tags(console, filtered)
    elif mode_choice == "5":
        console.rule("[bold magenta]🔥 Heat Map")
        _week_heatmap(console, filtered)
        console.rule("[bold magenta]🧾 Overall Summary")
        _week_overall(console, filtered)
        console.rule("[bold magenta]📈 Quantitative Metrics")
        _week_quant(console, filtered)
        console.rule("[bold magenta]🏷️ Tag Analysis")
        _week_tags(console, filtered)


def _week_overall(console, sessions):
    total_minutes = sum(s.get("duration_minutes", 0) for s in sessions if "duration_minutes" in s)
    total_hours = round(total_minutes / 60, 2)

    total_break_time = 0
    total_breaks = 0
    for s in sessions:
        for b in s.get("breaks", []):
            total_break_time += b.get("duration_minutes", 0)
        total_breaks += len(s.get("breaks", []))

    days = {datetime.fromisoformat(s["start"]).date() for s in sessions}
    average_per_day = round(total_hours / len(days), 2) if days else 0

    table = Table(title="🧾 Overall Summary", box=box.HEAVY)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="bold white")

    table.add_row("Total Sessions", str(len(sessions)))
    table.add_row("Total Hours", f"{total_hours} hrs")
    table.add_row("Average per Day", f"{average_per_day} hrs")
    table.add_row("Total Breaks", str(total_breaks))
    table.add_row("Total Break Time", f"{round(total_break_time, 2)} mins")

    console.print(table)

def _week_quant(console, sessions):
    durations = [s.get("duration_minutes") for s in sessions if "duration_minutes" in s]
    break_durations = [b.get("duration_minutes") for s in sessions for b in s.get("breaks", []) if "duration_minutes" in b]

    if len(durations) < 2:
        console.print("\n[italic yellow]Not enough complete sessions for statistical analysis.[/italic yellow]\n")
        return

    std_dev = round(statistics.stdev(durations), 2)
    longest = max(durations)
    shortest = min(durations)

    table = Table(title="📈 Quantitative Metrics", box=box.SIMPLE)
    table.add_column("Metric", style="magenta")
    table.add_column("Value", justify="right", style="white")

    table.add_row("Work Std Dev", f"{std_dev} mins")
    table.add_row("Longest Session", f"{longest} mins")
    table.add_row("Shortest Session", f"{shortest} mins")

    if break_durations:
        break_std = round(statistics.stdev(break_durations), 2) if len(break_durations) > 1 else 0.0
        avg_break = round(sum(break_durations) / len(break_durations), 2)
        table.add_row("Avg Break Duration", f"{avg_break} mins")
        table.add_row("Break Std Dev", f"{break_std} mins")
    else:
        table.add_row("Avg Break Duration", "0 mins")
        table.add_row("Break Std Dev", "0 mins")

    console.print(table)



def _week_tags(console, sessions):
    tag_totals = defaultdict(float)
    for s in sessions:
        tag = s.get("tag", "Unlabeled")
        if "duration_minutes" in s:
            tag_totals[tag] += s["duration_minutes"]

    if not tag_totals:
        console.print("[italic]No tag data to display.[/italic]")
        return

    table = Table(title="🏷️ Time by Tag", box=box.ROUNDED)
    table.add_column("Tag", style="cyan")
    table.add_column("Time (min)", justify="right", style="yellow")

    for tag, total in sorted(tag_totals.items(), key=lambda x: -x[1]):
        table.add_row(tag, f"{round(total, 2)}")

    console.print(table)


def _week_heatmap(console, sessions):
    # Build a grid: each day of the week and count of sessions
    heat = defaultdict(int)
    for s in sessions:
        date = datetime.fromisoformat(s["start"]).strftime("%a")
        heat[date] += 1

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    table = Table(title="🔥 Weekly Heat Map", box=box.MINIMAL_DOUBLE_HEAD)
    for day in days:
        table.add_column(day, justify="center")

    table.add_row(*[str(heat.get(day, 0)) for day in days])

    console.print(table)



def pause_session():
    if not LOG_FILE.exists():
        print("⚠️ No session log found.")
        return

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    if not data or not is_active_session(data[-1]):
        print("⚠️ No active session to pause.")
        return

    session = data[-1]

    if is_paused_session(session):
        print("⚠️ Session is already paused.")
        return

    start_break(session)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"⏸️ Paused task: {session['task']} at {format_pretty_time(session['breaks'][-1]['start'])}")


def resume_session():
    if not LOG_FILE.exists():
        print("⚠️ No session log found.")
        return

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    if not data or not is_active_session(data[-1]):
        print("⚠️ No active session to resume.")
        return

    session = data[-1]

    if not is_paused_session(session):
        print("⚠️ Session is not paused.")
        return

    end_break(session)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"▶️ Resumed task: {session['task']} at {format_pretty_time(session['breaks'][-1]['end'])}")
