# report_data.py

import json, os
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

class ReportBuilder:
    def __init__(self, json_path=None):
        # Automatically reference the session_log.json one level outside /chronotrack
        if json_path is None:
            project_root = Path(__file__).resolve().parent.parent
            json_path = project_root / "session_log.json"
        self.path = json_path
        self.sessions = self.load_sessions()
        self.now = datetime.now()

    def load_sessions(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def get_week_range(self):
        end = self.now
        start = end - timedelta(days=6)
        return start, end


    def filter_sessions_this_week(self):
        start, end = self.get_week_range()
        return [
            s for s in self.sessions
            if "start" in s and start.date() <= datetime.fromisoformat(s["start"]).date() <= end.date()
        ]

    def build_tag_stats(self, sessions):
        stats = defaultdict(float)
        for s in sessions:
            if "duration_minutes" in s:
                stats[s.get("tag", "Unlabeled")] += s["duration_minutes"] / 60.0
        return dict(sorted(stats.items(), key=lambda x: -x[1]))

    def build_daily_heatmap(self, sessions):
        heatmap = {day: [0]*24 for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
        for s in sessions:
            if "start" not in s or "end" not in s:
                continue
            try:
                start = datetime.fromisoformat(s["start"])
                end = datetime.fromisoformat(s["end"])
                cur = start
                while cur < end:
                    day = cur.strftime("%A")
                    heatmap[day][cur.hour] += 1
                    cur += timedelta(minutes=15)
            except Exception:
                continue  # Avoid crash from malformed timestamps
        return heatmap

    def find_most_focused_day(self, sessions):
        totals = defaultdict(float)
        for s in sessions:
            if "start" not in s or "duration_minutes" not in s:
                continue
            day = datetime.fromisoformat(s["start"]).strftime("%A")
            totals[day] += s["duration_minutes"]
        if not totals:
            return "N/A"
        top_day, mins = max(totals.items(), key=lambda x: x[1], default=("None", 0))
        return f"{top_day} ({int(mins // 60)}h {int(mins % 60)}m)"

    def find_longest_session(self, sessions):
        complete_sessions = [s for s in sessions if "duration_minutes" in s]
        if not complete_sessions:
            return {"task": "-", "duration": "-"}
        s = max(complete_sessions, key=lambda s: s["duration_minutes"])
        mins = int(s["duration_minutes"])
        return {
            "task": s.get("task", "Unnamed Task"),
            "duration": f"{mins // 60}h {mins % 60}m"
        }

    def calculate_break_focus_ratio(self, sessions):
        total_break = sum(s.get("total_break_time", 0.0) for s in sessions if "duration_minutes" in s)
        total_focus = sum(s["duration_minutes"] for s in sessions if "duration_minutes" in s)
        return round(total_break / total_focus, 2) if total_focus else 0

    def collect_top_notes(self, sessions):
        notes = []
        for s in sessions:
            if s.get("note"):
                notes.append({
                    "tag": s.get("tag", "Untagged"),
                    "note": s["note"],
                    "sentiment": "neutral"
                })
        return notes[:5]

    def build_full_report(self):
        sessions = self.filter_sessions_this_week()
        start, end = self.get_week_range()
        return {
            "user": "Mahir Anan",
            "week_range": f"{start.strftime('%b %d')} – {end.strftime('%b %d, %Y')}",
            "total_hours": round(
                sum(s["duration_minutes"] for s in sessions if "duration_minutes" in s) / 60.0, 2
            ),
            "tag_stats": self.build_tag_stats(sessions),
            "daily_heatmap": self.build_daily_heatmap(sessions),
            "most_focused_day": self.find_most_focused_day(sessions),
            "longest_session": self.find_longest_session(sessions),
            "break_focus_ratio": self.calculate_break_focus_ratio(sessions),
            "top_notes": self.collect_top_notes(sessions),
            "ai_insight": "Your focus this week leaned toward backend work. Consider diversifying."
        }
