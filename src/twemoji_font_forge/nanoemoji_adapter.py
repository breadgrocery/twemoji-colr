from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from .progress import NINJA_PROGRESS_RE, ProgressReporter
from .templates import render_nanoemoji_toml


def write_nanoemoji_config(source_root: Path, output_file: Path, version: str) -> Path:
    config_file = source_root / "nanoemoji.toml"
    content = render_nanoemoji_toml(output_file.as_posix(), version)
    config_file.write_text(content, encoding="utf-8")
    return config_file


def run_nanoemoji(config_file: Path, progress: ProgressReporter, work_root: Path) -> None:
    env = os.environ.copy()
    python_dir = Path(sys.executable).resolve().parent
    path_entries = [python_dir / "Scripts", python_dir]
    existing_path = env.get("PATH", "")
    env["PATH"] = os.pathsep.join(
        [str(path) for path in path_entries if path.exists()] + [existing_path]
    )

    command = [
        sys.executable,
        "-m",
        "nanoemoji.nanoemoji",
        str(config_file),
    ]
    process = subprocess.Popen(
        command,
        cwd=str(work_root),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    assert process.stdout is not None
    for line in process.stdout:
        stripped = line.strip()
        match = NINJA_PROGRESS_RE.search(stripped)
        if match:
            current = int(match.group(1))
            total = int(match.group(2))
            progress.task_progress("Running nanoemoji build", current, total)
        elif stripped:
            progress.log(stripped)

    return_code = process.wait()
    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, command)
