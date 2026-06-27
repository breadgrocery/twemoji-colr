from __future__ import annotations

from pathlib import Path

import typer

from .pipeline import BuildOptions, DEFAULT_OUTPUT_DIR, DEFAULT_REPOSITORY, DEFAULT_WORK_DIR, build_font


app = typer.Typer(add_completion=False, help="Build a Twemoji glyf_colr_0 font")


@app.command()
def run(
    repository: str = typer.Option(
        DEFAULT_REPOSITORY,
        "--repo",
        help="Twemoji repository in owner/name format.",
    ),
    tag: str = typer.Option(
        "",
        "--tag",
        help="Twemoji tag to build. Defaults to latest tag.",
    ),
    output_dir: Path = typer.Option(
        DEFAULT_OUTPUT_DIR,
        "--output",
        help="Output directory for generated font files.",
    ),
    work_dir: Path = typer.Option(
        DEFAULT_WORK_DIR,
        "--workdir",
        help="Working directory for download and build cache.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force rebuild even when output already exists.",
        is_flag=True,
    ),
) -> None:
    options = BuildOptions(
        repository=repository,
        tag=tag,
        output_dir=output_dir,
        work_dir=work_dir,
        force=force,
    )
    build_font(options)


def main() -> None:
    app()
