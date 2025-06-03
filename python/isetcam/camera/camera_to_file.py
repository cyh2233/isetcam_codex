# mypy: ignore-errors
"""Utilities for saving :class:`Camera` objects to disk."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from scipy.io import savemat

from .camera_class import Camera
from .camera_clear_data import camera_clear_data


def camera_to_file(camera: Camera, path: str | Path) -> None:
    """Save ``camera`` to ``path`` as a MATLAB ``.mat`` file.

    The sensor and optical image dataclasses are stored as nested structures
    under the variable name ``'camera'``.
    """
    data = asdict(camera_clear_data(camera))
    savemat(str(Path(path)), {"camera": data})
