"""Approximate a hyperspectral cube using basis functions."""

from __future__ import annotations

import numpy as np


def hc_basis(cube: np.ndarray, basis: np.ndarray) -> np.ndarray:
    """Approximate ``cube`` using ``basis`` and reconstruct it.

    Parameters
    ----------
    cube : np.ndarray
        Input hyperspectral cube with shape ``(rows, cols, bands)``.
    basis : np.ndarray
        Basis matrix of shape ``(bands, n_basis)``.

    Returns
    -------
    np.ndarray
        Reconstructed cube with the same shape as ``cube``.
    """
    cube = np.asarray(cube, dtype=float)
    basis = np.asarray(basis, dtype=float)
    if cube.ndim != 3:
        raise ValueError("cube must be 3-D")
    if basis.ndim != 2 or basis.shape[0] != cube.shape[2]:
        raise ValueError("basis must be (bands, n_basis)")

    rows, cols, bands = cube.shape
    xw = cube.reshape(-1, bands)
    # Compute coefficients that best approximate the spectra in a
    # least-squares sense and reconstruct the cube.
    coef, _, _, _ = np.linalg.lstsq(basis, xw.T, rcond=None)
    recon = (basis @ coef).T.reshape(rows, cols, bands)
    return recon
