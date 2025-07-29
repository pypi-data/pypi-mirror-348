from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def get_project_output_dir():
    """
    Returns the .chronotrack/output folder inside the current working directory.
    Creates it if it doesn't exist.
    """
    output_dir = Path.cwd() / ".chronotrack" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def generate(report):
    # Locate templates directory
    template_dir = Path(__file__).resolve().parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template("report.html.j2")

    # Render HTML
    html = template.render(report=report)

    # Save report to CWD/.chronotrack/output/
    output_path = get_project_output_dir() / "rendered_report.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return str(output_path)

