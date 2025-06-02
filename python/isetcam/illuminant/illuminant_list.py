# mypy: ignore-errors
"""List available illuminant spectral data files."""

from __future__ import annotations

from pathlib import Path

from ..data_path import data_path


def illuminant_list() -> list[str]:
    """Return available illuminant names.

    The names correspond to ``.mat`` files under ``data/lights`` in the
    ISETCam repository. The returned list is sorted alphabetically and the
    ``.mat`` extension is stripped.
    """
    illum_dir = data_path("lights")
    names: list[str] = []
    if illum_dir.exists():
        for f in illum_dir.iterdir():
            if f.suffix == ".mat":
                names.append(f.stem)
            elif f.suffix == ".b64" and f.name.endswith(".mat.b64"):
                names.append(Path(f.name[:-4]).stem)
    return sorted(names)


__all__ = ["illuminant_list"]
