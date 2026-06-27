from __future__ import annotations

from importlib import resources
from string import Template

def _load_template(file_name: str) -> Template:
    package_root = resources.files("twemoji_font_forge")
    template_file = package_root.joinpath("templates", file_name)
    return Template(template_file.read_text(encoding="utf-8"))


def render_nanoemoji_toml(output_file_posix: str, version: str) -> str:
    parts = version.split(".")
    version_major = int(parts[0]) if len(parts) > 0 else 1
    version_minor = int(parts[1]) if len(parts) > 1 else 0
    return _load_template("nanoemoji.toml.tpl").substitute(
        output_file=output_file_posix,
        version_major=version_major,
        version_minor=version_minor,
    )


def render_preview_html(font_file_name: str, ranges_json: str, sequences_json: str) -> str:
    return _load_template("preview.html.tpl").substitute(
        font_file_name=font_file_name,
        ranges_json=ranges_json,
        sequences_json=sequences_json,
    )
