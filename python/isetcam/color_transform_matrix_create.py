"""Create color transformation matrix from spectral data."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np

from .ie_read_spectra import ie_read_spectra


def _load_data(src: str | Path | np.ndarray, wave: Iterable[float] | None) -> np.ndarray:
    if isinstance(src, (str, Path)):
        data, _, _, _ = ie_read_spectra(src, wave)
    else:
        data = np.asarray(src, dtype=float)
        if wave is not None and data.shape[0] != len(list(wave)):
            raise ValueError("Data length must match wavelength vector")
    return data


def color_transform_matrix_create(
    src: str | Path | np.ndarray,
    dst: str | Path | np.ndarray,
    wave: Iterable[float] | None = None,
) -> np.ndarray:
    """Compute a least-squares transform between spectral datasets.

    Parameters
    ----------
    src, dst : str or Path or array-like
        Source and target spectral data or filenames understood by
        :func:`~isetcam.ie_read_spectra`.
    wave : array-like, optional
        Wavelength sampling used when loading spectra from files.

    Returns
    -------
    np.ndarray
        Matrix ``T`` such that ``src @ T`` approximates ``dst``.
    """
    src_data = _load_data(src, wave)
    dst_data = _load_data(dst, wave)

    if src_data.shape[0] != dst_data.shape[0]:
        raise ValueError("src and dst must have the same number of rows")

    T, _, _, _ = np.linalg.lstsq(src_data, dst_data, rcond=None)
    return T
