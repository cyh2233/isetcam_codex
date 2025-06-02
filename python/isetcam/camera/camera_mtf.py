# mypy: ignore-errors
"""Compute camera MTF from sensor and optics models."""

from __future__ import annotations

from typing import Sequence, Tuple

import numpy as np

from .camera_class import Camera


_DEF_PIXEL_SIZE = 2.8e-6  # meters, matches sensor_create default
_DEF_WAVELENGTH = 550e-9  # meters


def _pixel_mtf(freq: np.ndarray, pixel_size: float) -> np.ndarray:
    """Return MTF of a square pixel aperture.

    Parameters
    ----------
    freq : np.ndarray
        Spatial frequencies in cycles/mm.
    pixel_size : float
        Pixel width in meters.
    """
    pixel_mm = pixel_size * 1e3
    return np.abs(np.sinc(freq * pixel_mm))


def _diffraction_mtf(freq: np.ndarray, f_number: float, wavelength: float) -> np.ndarray:  # noqa: E501
    """Diffraction limited optics MTF for a circular aperture."""
    # cutoff frequency in cycles/mm
    f_cutoff = 1.0 / (wavelength * f_number) / 1e3
    norm_freq = np.asarray(freq, dtype=float) / float(f_cutoff)
    mtf = np.zeros_like(norm_freq)
    inside = norm_freq <= 1.0
    f = norm_freq[inside]
    mtf[inside] = (2 / np.pi) * (np.arccos(f) - f * np.sqrt(1.0 - f**2))
    return mtf


def camera_mtf(camera: Camera,
               freqs: Sequence[float] | None = None,
               method: str = "product") -> Tuple[np.ndarray, np.ndarray]:
    """Return the modulation transfer function of ``camera``.

    Parameters
    ----------
    camera : Camera
        Camera instance containing ``sensor`` and ``optics`` models.
    freqs : sequence of float, optional
        Spatial frequencies in cycles/mm. When ``None`` a range from 0 to
        the optics diffraction limit is used.
    method : str, optional
        Combination method. Only ``"product"`` (pixel MTF times optics MTF)
        is implemented.

    Returns
    -------
    freqs : np.ndarray
        Frequency samples used for the calculation (cycles/mm).
    mtf : np.ndarray
        MTF values corresponding to ``freqs``.
    """
    pixel_size = getattr(camera.sensor, "pixel_size", _DEF_PIXEL_SIZE)
    f_number = getattr(camera.optics, "f_number", 4.0)
    wavelength = float(np.mean(camera.sensor.wave)) * 1e-9 if getattr(camera.sensor, "wave", None) is not None else _DEF_WAVELENGTH  # noqa: E501
    # diffraction cutoff frequency in cycles/mm
    f_cutoff = 1.0 / (wavelength * f_number) / 1e3
    if freqs is None:
        freqs = np.linspace(0, f_cutoff, 100)
    else:
        freqs = np.asarray(freqs, dtype=float)

    if method != "product":
        raise ValueError(f"Unknown method '{method}'")

    mtf_pixel = _pixel_mtf(freqs, pixel_size)
    mtf_optics = _diffraction_mtf(freqs, f_number, wavelength)
    mtf = mtf_pixel * mtf_optics
    return freqs, mtf


__all__ = ["camera_mtf"]
