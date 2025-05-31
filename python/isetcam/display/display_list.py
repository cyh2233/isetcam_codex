"""List available display calibration files."""

from __future__ import annotations

from pathlib import Path

from ..iset_root_path import iset_root_path


_DEF_DIR = "data"


def display_list() -> list[str]:
    """Return available display calibration names.

    The names correspond to ``.mat`` files under ``data/displays`` in the
    ISETCam repository.  The returned list is sorted alphabetically and the
    ``.mat`` extension is stripped.
    """
    root = iset_root_path()
    disp_dir = root / _DEF_DIR / "displays"
    names: list[str] = []
    if disp_dir.exists():
        for f in disp_dir.glob("*.mat"):
            names.append(Path(f).stem)
    return sorted(names)


__all__ = ["display_list"]
