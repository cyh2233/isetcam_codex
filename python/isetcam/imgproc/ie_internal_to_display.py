# mypy: ignore-errors
"""Linear transform from internal color space to display RGB."""

from __future__ import annotations

import numpy as np


def ie_internal_to_display(
    internal_cmf: np.ndarray, display_spd: np.ndarray
) -> np.ndarray:
    """Return transformation from internal color space to display RGB.

    Parameters
    ----------
    internal_cmf : np.ndarray
        Color matching functions of the internal color space with shape
        ``(n_wavelengths, n_channels)``.
    display_spd : np.ndarray
        Spectral power distribution of the display primaries with shape
        ``(n_wavelengths, 3)``.

    Returns
    -------
    np.ndarray
        Matrix ``T`` such that ``internal_values @ T`` yields display RGB
        values whose SPD reproduces ``internal_values`` when measured by
        ``internal_cmf``.
    """

    internal_cmf = np.asarray(internal_cmf, dtype=float)
    display_spd = np.asarray(display_spd, dtype=float)
    if internal_cmf.shape[0] != display_spd.shape[0]:
        raise ValueError("internal_cmf and display_spd must have matching lengths")

    M = display_spd.T @ internal_cmf
    if np.linalg.matrix_rank(M) < M.shape[0]:
        raise np.linalg.LinAlgError("display_spd.T @ internal_cmf is singular")
    return np.linalg.inv(M)
