# mypy: ignore-errors
"""Save shift-invariant PSF data to a MAT-file."""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from scipy.io import savemat


def ie_save_si_data_file(
    path: str | Path,
    psf: np.ndarray,
    wave: Iterable[float],
    um_per_samp: Sequence[float],
) -> None:
    """Write ``psf`` and associated metadata to ``path``."""
    data = {
        "psf": np.asarray(psf, dtype=float),
        "wave": np.asarray(list(wave), dtype=float),
        "umPerSamp": np.asarray(um_per_samp, dtype=float),
        "notes": {"timeStamp": datetime.datetime.now().isoformat()},
    }
    savemat(str(Path(path)), data)


__all__ = ["ie_save_si_data_file"]
