from pathlib import Path
from jinja2 import FileSystemLoader, Environment, select_autoescape

from .entities import Period, Organization


jinja_env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "tpls"),
    autoescape=select_autoescape()
)
index_template = jinja_env.get_template("index.html")


def render_html_organization(organization: Organization, period: Period) -> str:
    return index_template.render(organization=organization, period=period)


def render_cli_organization(organization: Organization, period: Period) -> str:
    buff = [
        "",
        f"Organization: {organization.name}",
        f"Period: {period}",
    ]
    for project in organization.projects:
        buff.append("")
        buff.append(f"Project: {project.name} (id={project.id})")
        buff.append("=" * 88)
        for activity in project.activities:
            buff.append(f"{activity.user.name} :: {activity.duration}")
            buff.append("-" * 88)
    return "\n".join(buff)
