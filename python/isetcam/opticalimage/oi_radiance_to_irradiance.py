"""Convert scene radiance to optical image irradiance."""

from __future__ import annotations

import numpy as np


def oi_radiance_to_irradiance(radiance: np.ndarray, f_number: float) -> np.ndarray:
    """Return irradiance from scene radiance for a lens with ``f_number``.

    Parameters
    ----------
    radiance : array-like
        Scene radiance values.
    f_number : float
        Lens f-number.

    Returns
    -------
    np.ndarray
        Irradiance corresponding to ``radiance``.
    """
    return np.asarray(radiance, dtype=float) * (np.pi / float(f_number) ** 2)


__all__ = ["oi_radiance_to_irradiance"]
