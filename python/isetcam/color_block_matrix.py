# mypy: ignore-errors
"""Block matrix used to visualize spectral data as RGB."""

from __future__ import annotations

import numpy as np


def color_block_matrix(
    wave: np.ndarray,
    extrap_val: float = 0.0,
    white_spd: np.ndarray | None = None,
) -> np.ndarray:
    """Return a block matrix mapping a spectrum to RGB values.

    Parameters
    ----------
    wave : array-like
        Wavelength samples in nanometers.
    extrap_val : float, optional
        Value used outside the 400--700 nm range when ``wave`` extends
        beyond the defaults. Default ``0.0``.
    white_spd : array-like, optional
        Photon spectrum that should map to ``(1, 1, 1)``. When provided the
        returned matrix is premultiplied by ``diag(1 / white_spd)``.

    Returns
    -------
    np.ndarray
        Matrix with shape ``(len(wave), 3)`` that converts spectra to RGB.
    """
    wave = np.asarray(wave, dtype=float).ravel()
    if wave.ndim != 1:
        raise ValueError("wave must be a 1-D array")

    default_wave = np.arange(400, 701, 10, dtype=float)

    b = 10
    g = 8
    r = 31 - b - g
    default_matrix = np.vstack(
        [
            np.concatenate([np.zeros(b), np.zeros(g), np.ones(r)]),
            np.concatenate([np.zeros(b), np.ones(g), np.zeros(r)]),
            np.concatenate([np.ones(b), np.zeros(g), np.zeros(r)]),
        ]
    ).T

    if wave.size == default_wave.size and np.allclose(wave, default_wave):
        b_matrix = default_matrix.copy()
    else:
        b_matrix = np.zeros((wave.size, 3), dtype=float)
        for i in range(3):
            b_matrix[:, i] = np.interp(
                wave, default_wave, default_matrix[:, i], left=extrap_val, right=extrap_val  # noqa: E501
            )

    # Normalize so that each column sums to one
    b_matrix /= b_matrix.sum(axis=0, keepdims=True)

    if white_spd is not None:
        white_spd = np.asarray(white_spd, dtype=float).ravel()
        if white_spd.size != wave.size:
            raise ValueError("white_spd must match wave length")
        b_matrix = np.diag(1.0 / white_spd) @ b_matrix

    return b_matrix
