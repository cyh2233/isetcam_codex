"""Simplified factory for :class:`Scene` objects."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
from scipy.io import loadmat

from .scene_class import Scene
from ..luminance_from_photons import luminance_from_photons
from ..iset_root_path import iset_root_path


_DEF_DIR = "data"


def _load_macbeth_data(wave: Optional[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    """Return reflectance data and wavelength array for the Macbeth chart."""
    root = iset_root_path()
    mat = loadmat(root / _DEF_DIR / "surfaces" / "reflectances" / "macbethChart.mat")
    src_wave = mat["wavelength"].ravel().astype(float)
    refl = mat["data"].astype(float)
    if wave is None:
        return refl, src_wave
    wave = np.asarray(wave, dtype=float).reshape(-1)
    interp = np.zeros((wave.size, refl.shape[1]), dtype=float)
    for i in range(refl.shape[1]):
        interp[:, i] = np.interp(wave, src_wave, refl[:, i], left=0.0, right=0.0)
    return interp, wave


def _load_d65(wave: np.ndarray) -> np.ndarray:
    """Return D65 spectral power distribution sampled at ``wave``."""
    root = iset_root_path()
    mat = loadmat(root / _DEF_DIR / "lights" / "D65.mat")
    src_wave = mat["wavelength"].ravel().astype(float)
    spd = mat["data"].ravel().astype(float)
    return np.interp(wave, src_wave, spd, left=0.0, right=0.0)


def _create_macbeth_d65(patch_size: int = 16, wave: Optional[np.ndarray] = None,
                        mean_luminance: Optional[float] = None) -> Scene:
    refl, wave = _load_macbeth_data(wave)
    d65 = _load_d65(wave)

    nrows, ncols = 4, 6
    photons = np.zeros((patch_size * nrows, patch_size * ncols, wave.size), dtype=float)
    idx = 0
    for r in range(nrows):
        for c in range(ncols):
            patch = refl[:, idx] * d65
            photons[r*patch_size:(r+1)*patch_size, c*patch_size:(c+1)*patch_size, :] = patch
            idx += 1

    sc = Scene(photons=photons, wave=wave, name="Macbeth D65")
    if mean_luminance is not None:
        lum = luminance_from_photons(sc.photons, sc.wave)
        cur = float(lum.mean())
        if cur > 0:
            sc.photons = sc.photons * (mean_luminance / cur)
    return sc


def _create_uniform_monochromatic(wavelength: float = 550.0, size: int = 128) -> Scene:
    wave = np.array([float(wavelength)], dtype=float)
    photons = np.ones((size, size, 1), dtype=float)
    return Scene(photons=photons, wave=wave, name="Uniform monochromatic")


def _create_whitenoise(size: int = 128, contrast: float = 0.2,
                       wave: Optional[np.ndarray] = None) -> Scene:
    if wave is None:
        wave = np.array([550.0], dtype=float)
    else:
        wave = np.asarray(wave, dtype=float).reshape(-1)
    photons = np.random.randn(size, size, wave.size) * float(contrast) + 1.0
    photons = np.clip(photons, 0.0, None)
    return Scene(photons=photons, wave=wave, name="White noise")


_VALID_TYPES = {
    "macbethd65": _create_macbeth_d65,
    "uniformmonochromatic": _create_uniform_monochromatic,
    "whitenoise": _create_whitenoise,
}


def scene_create(name: str, **kwargs) -> Scene:
    """Create a simple :class:`Scene` specified by ``name``."""
    flag = name.lower().replace(" ", "")
    if flag not in _VALID_TYPES:
        raise ValueError(f"Unknown scene type '{name}'")
    return _VALID_TYPES[flag](**kwargs)
