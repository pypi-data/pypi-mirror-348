# generate_report.py

from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def generate(report):
    # Automatically find the path to the `templates` folder
    template_dir = Path(__file__).resolve().parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report.html.j2")


    html = template.render(report=report)
    output_path = Path(__file__).resolve().parent.parent / "output" / "rendered_report.html"
    output_path.parent.mkdir(exist_ok=True)  # Make sure output/ exists

    with open(output_path, "w") as f:
        f.write(html)

    return str(output_path)
