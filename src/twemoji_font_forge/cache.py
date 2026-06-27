from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

from .progress import ProgressReporter


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as input_file:
        while True:
            chunk = input_file.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def sha256_file(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".sha256")


def verify_or_write_sha256(path: Path) -> bool:
    checksum_path = sha256_file(path)
    actual = sha256(path)
    if checksum_path.exists():
        expected = checksum_path.read_text(encoding="utf-8").strip()
        if expected != actual:
            return False
    checksum_path.write_text(actual + "\n", encoding="utf-8")
    return True


def extract_svg_dir(archive_path: Path, destination: Path, progress: ProgressReporter) -> Path:
    for path in destination.iterdir():
        if not path.is_dir():
            continue
        candidate = path / "assets" / "svg"
        if candidate.exists():
            progress.log(f"Using cached extracted source: {candidate}")
            return candidate

    with zipfile.ZipFile(archive_path) as archive:
        archive.extractall(destination)

    extracted_roots = [path for path in destination.iterdir() if path.is_dir()]
    for root in extracted_roots:
        svg_dir = root / "assets" / "svg"
        if svg_dir.exists():
            return svg_dir

    raise RuntimeError("Unexpected Twemoji archive layout: missing assets/svg")


def ensure_svg_dir_has_files(svg_dir: Path) -> None:
    if not any(svg_dir.glob("*.svg")):
        raise RuntimeError(f"No SVG files found in {svg_dir}")
