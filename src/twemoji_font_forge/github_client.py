from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path

from .progress import ProgressReporter


GITHUB_API = "https://api.github.com"
GITHUB_TOKEN_ENV_VARS = ("TWEMOJI_GITHUB_TOKEN", "GITHUB_TOKEN", "GH_TOKEN")


def github_token() -> str | None:
    for env_name in GITHUB_TOKEN_ENV_VARS:
        value = os.environ.get(env_name)
        if value:
            return value
    return None


def request_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "twemoji_font_forge",
    }
    token = github_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def request_json(url: str) -> object:
    request = urllib.request.Request(url, headers=request_headers())
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def latest_tag(repository: str) -> str:
    data = request_json(f"{GITHUB_API}/repos/{repository}/tags?per_page=1")
    if not isinstance(data, list) or not data:
        raise RuntimeError(f"No tags found for {repository}")
    first = data[0]
    if not isinstance(first, dict) or "name" not in first:
        raise RuntimeError(f"Unexpected tag payload for {repository}")
    return str(first["name"])


def download_source_archive(
    repository: str,
    tag: str,
    destination: Path,
    progress: ProgressReporter,
) -> Path:
    archive_url = f"https://github.com/{repository}/archive/refs/tags/{tag}.zip"
    archive_path = destination / f"{tag}.zip"

    request = urllib.request.Request(archive_url, headers=request_headers())
    with urllib.request.urlopen(request) as response, archive_path.open("wb") as output:
        total = response.headers.get("Content-Length")
        total_bytes = int(total) if total and total.isdigit() else None
        downloaded = 0
        last_update = time.monotonic()
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            output.write(chunk)
            downloaded += len(chunk)
            now = time.monotonic()
            if now - last_update > 0.1:
                progress.bytes_progress("Downloading Twemoji archive", downloaded, total_bytes)
                last_update = now
        progress.bytes_progress("Downloading Twemoji archive", downloaded, total_bytes)

    return archive_path
