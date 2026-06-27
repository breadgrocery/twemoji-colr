from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .cache import ensure_svg_dir_has_files, extract_svg_dir, verify_or_write_sha256
from .github_client import download_source_archive, latest_tag
from .nanoemoji_adapter import run_nanoemoji, write_nanoemoji_config
from .preview import generate_preview_html
from .progress import ProgressReporter


DEFAULT_REPOSITORY = "jdecked/twemoji"
DEFAULT_OUTPUT_DIR = Path("dist")
DEFAULT_WORK_DIR = Path(".build")


@dataclass(frozen=True)
class BuildOptions:
    repository: str = DEFAULT_REPOSITORY
    tag: str = ""
    output_dir: Path = DEFAULT_OUTPUT_DIR
    work_dir: Path = DEFAULT_WORK_DIR
    force: bool = False


def build_font(options: BuildOptions) -> Path:
    progress = ProgressReporter(total_stages=8, enabled=True)

    output_dir = options.output_dir.resolve()
    work_dir = options.work_dir.resolve()

    progress.stage("Resolving Twemoji tag")
    resolved_tag = options.tag or latest_tag(options.repository)

    progress.stage(f"Preparing workspace for {resolved_tag}")
    output_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)
    build_root = work_dir / resolved_tag
    build_root.mkdir(parents=True, exist_ok=True)

    tagged_output_dir = output_dir / resolved_tag
    tagged_output_dir.mkdir(parents=True, exist_ok=True)
    output_file = tagged_output_dir / "Twemoji.ttf"
    preview_file = output_file.with_name("preview.html")

    progress.stage("Checking existing output")
    if output_file.exists() and not options.force:
        if not preview_file.exists():
            progress.stage("Generating preview HTML")
            generate_preview_html(output_file)
        progress.done(f"Output already exists, skipping build: {output_file}")
        return output_file

    progress.stage("Fetching Twemoji source archive")
    cached_archive = build_root / f"{resolved_tag}.zip"
    if cached_archive.exists() and verify_or_write_sha256(cached_archive):
        progress.log(f"Using cached archive: {cached_archive}")
        archive_path = cached_archive
    else:
        if cached_archive.exists():
            progress.log(f"Cached archive checksum mismatch, redownloading: {cached_archive}")
        archive_path = download_source_archive(options.repository, resolved_tag, build_root, progress)
        if not verify_or_write_sha256(archive_path):
            raise RuntimeError(f"SHA256 verification failed for downloaded archive: {archive_path}")

    progress.stage("Preparing extracted source")
    svg_dir = extract_svg_dir(archive_path, build_root, progress)
    ensure_svg_dir_has_files(svg_dir)

    progress.stage("Generating nanoemoji config")
    source_root = svg_dir.parent.parent
    font_version = resolved_tag.lstrip("v")
    config_file = write_nanoemoji_config(source_root, output_file, font_version)

    progress.stage("Building font with nanoemoji")
    run_nanoemoji(config_file, progress, build_root)

    progress.stage("Generating preview HTML")
    generate_preview_html(output_file)

    progress.done(f"Build complete: {output_file}")
    return output_file
