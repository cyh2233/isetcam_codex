# mypy: ignore-errors
"""Load a :class:`Display` from a MATLAB ``.mat`` file."""

from __future__ import annotations

from pathlib import Path

from .display_create import _load_display
from .display_class import Display


def display_from_file(path: str | Path, wave: np.ndarray | None = None) -> Display:
    """Load ``path`` and return a :class:`Display`.

    Parameters
    ----------
    path : str or Path
        MAT-file containing a display structure ``d``.
    """
    file_wave, spd, gamma = _load_display(Path(path))
    if wave is not None:
        new_wave = np.asarray(wave, dtype=float).ravel()
        if len(new_wave) != len(file_wave):
            spd = np.column_stack(
                [np.interp(new_wave, file_wave, spd[:, i]) for i in range(spd.shape[1])]
            )
            if gamma is not None and gamma.shape[0] == len(file_wave):
                gamma = np.column_stack(
                    [np.interp(new_wave, file_wave, gamma[:, i]) for i in range(gamma.shape[1])]
                )
            file_wave = new_wave
    return Display(spd=spd, wave=file_wave, gamma=gamma)
