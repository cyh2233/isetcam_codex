# mypy: ignore-errors
"""List available display calibration files."""

from __future__ import annotations

from pathlib import Path

from ..data_path import data_path


_DEF_DIR = "data"


def display_list() -> list[str]:
    """Return available display calibration names.

    The names correspond to ``.mat`` files under ``data/displays`` in the
    ISETCam repository.  The returned list is sorted alphabetically and the
    ``.mat`` extension is stripped.
    """
    disp_dir = data_path("displays")
    names: list[str] = []
    if disp_dir.exists():
        for f in disp_dir.glob("*.mat"):
            names.append(Path(f).stem)
    return sorted(names)


__all__ = ["display_list"]
