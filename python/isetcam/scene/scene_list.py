# mypy: ignore-errors
"""List available sample scenes."""

from __future__ import annotations

from pathlib import Path

from ..data_path import data_path


# We search both for MATLAB ``.mat`` files and common image formats.
_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".exr"}
_MATLAB_EXTS = {".mat", ".m"}


def scene_list() -> list[str]:
    """Return available sample scene names.

    The names correspond to files located under ``data/scenes`` in the
    ISETCam repository. Both ``.mat`` files and common image formats are
    included. The returned list is sorted alphabetically and the file
    extensions are stripped.
    """
    sc_dir = data_path("scenes")
    names: list[str] = []
    if sc_dir.exists():
        for f in sc_dir.iterdir():
            if not f.is_file():
                continue
            suffix = f.suffix.lower()
            if suffix in _MATLAB_EXTS or suffix in _IMAGE_EXTS:
                names.append(Path(f).stem)
    return sorted(names)


__all__ = ["scene_list"]
