"""Compute correlated color temperature from ``uv`` coordinates."""

from __future__ import annotations

from pathlib import Path
import numpy as np
from scipy.io import loadmat

from .data_path import data_path


def _load_cct_table() -> np.ndarray:
    """Load isotemperature line data."""
    # Prefer data in human subfolder if available
    path = data_path("human/cct.mat")
    if not path.exists():
        path = data_path("color/cct.mat")
        if not path.exists():
            path = data_path("lights/cct.mat")
    data = loadmat(path)
    return data["table"]


def cct(uv: np.ndarray) -> np.ndarray:
    """Return correlated color temperature for CIE uv coordinates.

    Parameters
    ----------
    uv : np.ndarray
        Array of uv coordinates provided either as ``(2, N)`` or ``(N, 2)``.

    Returns
    -------
    np.ndarray
        Estimated correlated color temperature in Kelvin.
    """
    uv = np.asarray(uv, dtype=float)
    if uv.shape[0] == 2:
        uv = uv.copy()
    elif uv.shape[1] == 2:
        uv = uv.T
    else:
        raise ValueError("uv must be (2,N) or (N,2)")

    table = _load_cct_table()
    T = table[:, 0][:, np.newaxis]
    u = table[:, 1][:, np.newaxis]
    v = table[:, 2][:, np.newaxis]
    t = table[:, 3][:, np.newaxis]

    Nd = uv.shape[1]
    us = np.tile(uv[0], (len(table), 1))
    vs = np.tile(uv[1], (len(table), 1))
    T = np.tile(T, (1, Nd))
    u = np.tile(u, (1, Nd))
    v = np.tile(v, (1, Nd))
    t = np.tile(t, (1, Nd))

    d = ((us - u) - t * (vs - v)) / np.sqrt(1 + t**2)

    ds = np.sign(d)
    ds = np.where(ds == 0, 1, ds)
    ds = np.vstack([ds, np.zeros((1, Nd))])

    j = np.where(np.abs(np.diff(ds, axis=0)) == 2)[0]
    if j.size != Nd:
        raise ValueError("Check input range of uv coordinates")

    Tc = 1.0 / (
        1.0 / T[j, range(Nd)]
        + d[j, range(Nd)]
        / (d[j, range(Nd)] - d[j + 1, range(Nd)])
        * (1.0 / T[j + 1, range(Nd)] - 1.0 / T[j, range(Nd)])
    )

    return Tc.squeeze()
