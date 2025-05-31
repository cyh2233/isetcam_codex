"""RGB directions that approximately isolate the cones of a display."""

from __future__ import annotations

import numpy as np

from ..display import Display
from ..ie_read_spectra import ie_read_spectra
from ..iset_root_path import iset_root_path


def human_cone_isolating(display: Display) -> tuple[np.ndarray, np.ndarray]:
    """Return RGB vectors that isolate L, M and S cones.

    Parameters
    ----------
    display : :class:`~isetcam.display.Display`
        Display model providing spectral power distributions of its
        primaries.

    Returns
    -------
    cone_isolating : np.ndarray
        ``(3, 3)`` matrix whose columns are linear RGB directions scaled so
        that ``max(abs(col)) == 0.5``.
    spd : np.ndarray
        Spectral power distributions of the three directions with shape
        ``(len(display.wave), 3)``.
    """
    wave = np.asarray(display.wave, dtype=float)
    spd = np.asarray(display.spd, dtype=float)

    root = iset_root_path()
    cone_file = root / "data" / "human" / "stockman.mat"
    cones, _, _, _ = ie_read_spectra(cone_file, wave)

    rgb2lms = (cones.T @ spd).T
    cone_isolating = np.linalg.inv(rgb2lms)
    mx = np.max(np.abs(cone_isolating), axis=0)
    cone_isolating = cone_isolating / (2 * mx)
    spd_dirs = spd @ cone_isolating

    return cone_isolating, spd_dirs
