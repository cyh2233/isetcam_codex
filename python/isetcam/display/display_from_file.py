# mypy: ignore-errors
"""Load a :class:`Display` from a MATLAB ``.mat`` file."""

from __future__ import annotations

from pathlib import Path

from .display_create import _load_display
from .display_class import Display


def display_from_file(path: str | Path) -> Display:
    """Load ``path`` and return a :class:`Display`.

    Parameters
    ----------
    path : str or Path
        MAT-file containing a display structure ``d``.
    """
    wave, spd, gamma = _load_display(Path(path))
    return Display(spd=spd, wave=wave, gamma=gamma)
