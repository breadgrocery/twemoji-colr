from __future__ import annotations

import re

from tqdm import tqdm


NINJA_PROGRESS_RE = re.compile(r"\[(\d+)/(\d+)\]")


class ProgressReporter:
    def __init__(self, total_stages: int, enabled: bool = True) -> None:
        self.total_stages = total_stages
        self.current_stage = 0
        self.enabled = enabled
        self._stage_bar: tqdm | None = None
        self._download_bar: tqdm | None = None
        self._download_desc: str = ""
        self._task_bar: tqdm | None = None
        self._task_desc: str = ""

    def _ensure_stage_bar(self) -> None:
        if not self.enabled or self._stage_bar is not None:
            return
        self._stage_bar = tqdm(
            total=self.total_stages,
            desc="pipeline",
            unit="stage",
            dynamic_ncols=True,
        )

    def stage(self, message: str) -> None:
        if not self.enabled:
            return
        self.current_stage += 1
        self._ensure_stage_bar()
        assert self._stage_bar is not None
        self._stage_bar.set_description_str(f"stage: {message}")
        if self._stage_bar.n < self.total_stages:
            self._stage_bar.update(1)

    def bytes_progress(self, message: str, downloaded: int, total: int | None) -> None:
        if not self.enabled:
            return
        if self._download_bar is None or self._download_desc != message:
            if self._download_bar is not None:
                self._download_bar.close()
            self._download_bar = tqdm(
                total=total,
                desc=message,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                dynamic_ncols=True,
            )
            self._download_desc = message
        assert self._download_bar is not None
        if total is not None and self._download_bar.total != total:
            self._download_bar.total = total
        delta = downloaded - int(self._download_bar.n)
        if delta > 0:
            self._download_bar.update(delta)

    def task_progress(self, message: str, current: int, total: int) -> None:
        if not self.enabled:
            return
        if self._task_bar is None or self._task_desc != message or self._task_bar.total != total:
            if self._task_bar is not None:
                self._task_bar.close()
            self._task_bar = tqdm(
                total=total,
                desc=message,
                unit="step",
                dynamic_ncols=True,
            )
            self._task_desc = message
        assert self._task_bar is not None
        target = min(current, total)
        delta = target - int(self._task_bar.n)
        if delta > 0:
            self._task_bar.update(delta)

    def log(self, message: str) -> None:
        if not self.enabled:
            return
        tqdm.write(message)

    def done(self, message: str) -> None:
        if not self.enabled:
            return
        if self._download_bar is not None:
            self._download_bar.close()
            self._download_bar = None
            self._download_desc = ""
        if self._task_bar is not None:
            self._task_bar.close()
            self._task_bar = None
            self._task_desc = ""
        if self._stage_bar is not None:
            self._stage_bar.close()
            self._stage_bar = None
        tqdm.write(message)
