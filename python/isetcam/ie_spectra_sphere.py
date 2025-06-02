# mypy: ignore-errors
"""Generate spectra whose CIE XYZ values lie on a sphere."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import loadmat

from .ie_xyz_from_energy import ie_xyz_from_energy, _xyz_color_matching
from .data_path import data_path

_DEF_FILE = "cieDaylightBasis.mat"


def _load_basis(wave: np.ndarray, basis: np.ndarray | str | Path | None) -> np.ndarray:
    """Return spectral basis functions interpolated to ``wave``."""
    wave = np.asarray(wave, dtype=float).reshape(-1)
    if basis is None:
        path = data_path(f"lights/{_DEF_FILE}")
    elif isinstance(basis, (str, Path)):
        p = Path(basis)
        if not p.is_absolute():
            p2 = data_path(f"lights/{p}")
            if p2.exists():
                p = p2
        path = p
    else:
        data = np.asarray(basis, dtype=float)
        if data.shape[0] != wave.size:
            raise ValueError("Basis shape must match number of wavelengths")
        return data

    mat = loadmat(path)
    src_wave = mat["wavelength"].ravel()
    data = mat["data"]
    out = np.zeros((wave.size, data.shape[1]), dtype=float)
    for i in range(data.shape[1]):
        out[:, i] = np.interp(wave, src_wave, data[:, i], left=0.0, right=0.0)
    return out


def _sphere(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate ``(x, y, z)`` coordinates on a unit sphere."""
    phi = np.linspace(0.0, 2 * np.pi, n + 1)
    theta = np.linspace(0.0, np.pi, n + 1)
    x = np.outer(np.sin(theta), np.cos(phi))
    y = np.outer(np.sin(theta), np.sin(phi))
    z = np.outer(np.cos(theta), np.ones_like(phi))
    return x, y, z


def ie_spectra_sphere(
    wave: np.ndarray,
    spectrum_e: np.ndarray,
    n: int = 8,
    basis: np.ndarray | str | Path | None = None,
    factor: float = 0.05,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return spectra surrounding ``spectrum_e`` in CIE XYZ space."""
    wave = np.asarray(wave, dtype=float).reshape(-1)
    spectrum_e = np.asarray(spectrum_e, dtype=float).reshape(-1)
    if spectrum_e.size != wave.size:
        raise ValueError("spectrum_e must match wave length")

    B = _load_basis(wave, basis)
    cmf = _xyz_color_matching(wave)

    X, Y, Z = _sphere(n)
    dXYZ = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])

    weights = np.linalg.solve(cmf.T @ B, dXYZ.T)
    spectra = B @ weights
    if spectra.shape[1] == 0:
        return np.empty((len(wave), 0)), np.empty((0, 3)), np.array([]), B

    spectra *= factor * np.linalg.norm(spectrum_e) / np.linalg.norm(spectra[:, 0])
    spectra = spectra + spectrum_e[:, np.newaxis]

    XYZ = ie_xyz_from_energy(spectra.T, wave)
    XYZ0 = ie_xyz_from_energy(spectrum_e[np.newaxis, :], wave).ravel()

    return spectra, XYZ, XYZ0, B
