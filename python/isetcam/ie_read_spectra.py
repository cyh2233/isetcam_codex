# mypy: ignore-errors
"""Load spectral data from a MATLAB file and interpolate.

This function reads variables ``data`` and ``wavelength`` from a MAT-file,
optionally interpolates to a new wavelength sampling, and returns the data
along with any ``comment`` variable found in the file.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Tuple

import numpy as np
from scipy.io import loadmat


def ie_read_spectra(
    fname: str | Path,
    wave: Iterable[float] | None = None,
    extrap_val: float = 0.0,
    make_positive: bool = False,
) -> Tuple[np.ndarray, np.ndarray, str | None, Path]:
    """Read spectral data from ``fname`` and interpolate to ``wave``.

    Parameters
    ----------
    fname:
        Path to a MATLAB ``.mat`` file containing ``data`` and ``wavelength``
        variables.
    wave:
        Optional wavelength samples to interpolate the data to. If ``None``,
        the data are returned at their native sampling.
    extrap_val:
        Value used for extrapolation outside the wavelength range in the file.
    make_positive:
        If ``True``, flip the sign of the data so that the mean of the first
        column is positive.

    Returns
    -------
    res:
        Spectral data interpolated to ``wave`` when provided.
    wave:
        Wavelength samples corresponding to ``res``.
    comment:
        Comment string from the file if present, otherwise ``None``.
    fname:
        Path to the loaded file.
    """
    path = Path(fname)
    mat = loadmat(path)

    if "data" not in mat or "wavelength" not in mat:
        raise KeyError("File must contain 'data' and 'wavelength'")

    data = np.asarray(mat["data"], dtype=float)
    src_wave = np.asarray(mat["wavelength"], dtype=float).reshape(-1)
    comment = mat.get("comment")
    if isinstance(comment, np.ndarray):
        comment = str(comment.squeeze())

    if data.shape[0] != src_wave.size:
        raise ValueError("Mis-match between wavelength and data variables")

    if wave is None:
        wave_out = src_wave
        res = data.astype(float)
    else:
        wave_out = np.asarray(list(wave), dtype=float).reshape(-1)
        if data.ndim == 1:
            res = np.interp(wave_out, src_wave, data, left=extrap_val, right=extrap_val)
        else:
            res = np.column_stack(
                [
                    np.interp(wave_out, src_wave, data[:, i], left=extrap_val, right=extrap_val)  # noqa: E501
                    for i in range(data.shape[1])
                ]
            )

    if make_positive:
        first = res if res.ndim == 1 else res[:, 0]
        if np.mean(first) < 0:
            res = -res

    return res, wave_out, comment, path
