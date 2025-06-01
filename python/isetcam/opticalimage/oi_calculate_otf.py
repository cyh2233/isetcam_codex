"""Calculate optical transfer function for an optical image."""

from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from .oi_class import OpticalImage
from .oi_frequency_support import oi_frequency_support
from ..optics import Optics, optics_defocus_core


def _cpd_scale(units: str, optics: Optics) -> float:
    """Conversion factor from ``units`` to cycles/degree."""
    deg_per_mm = 1.0 / (np.tan(np.deg2rad(1.0)) * optics.f_length * 1000.0)
    u = units.lower()
    if u in {"cyclesperdegree", "cycperdeg", "cpd"}:
        return deg_per_mm * 1e-3
    if u in {"cyclespermillimeter", "mm", "millimeter", "millimeters"}:
        return deg_per_mm
    if u in {"cyclespermicron", "um", "micron", "microns", "micrometer", "micrometers"}:
        return deg_per_mm * 1e3
    if u in {"cyclespermeter", "m", "meter", "meters"}:
        return deg_per_mm / 1e3
    raise ValueError(f"Unknown frequency unit '{units}'")


def _dl_otf(
    oi: OpticalImage,
    optics: Optics,
    f_support: np.ndarray,
    wave: np.ndarray,
    units: str,
) -> np.ndarray:
    """Diffraction limited (optionally defocused) OTF."""
    fx = f_support[:, :, 0]
    fy = f_support[:, :, 1]
    dist = np.sqrt(fx ** 2 + fy ** 2)
    scale = _cpd_scale(units, optics)
    sample_sf = dist * scale

    D = getattr(optics, "defocus_diopters", None)
    if D is None:
        D = np.zeros_like(wave, dtype=float)
    else:
        D = np.asarray(D, dtype=float)
        if D.size == 1:
            D = np.full(wave.shape, D.item(), dtype=float)
        if D.size != wave.size:
            raise ValueError("defocus_diopters length must match wave")

    otf_flat, _ = optics_defocus_core(optics, sample_sf.ravel(), D)

    r, c = fx.shape
    otf = np.zeros((r, c, wave.size), dtype=float)
    for i in range(wave.size):
        otf[:, :, i] = otf_flat[i].reshape(r, c)
    return otf


def _custom_otf(
    oi: OpticalImage,
    optics: Optics,
    f_support: np.ndarray,
    wave: np.ndarray,
    units: str,
) -> np.ndarray:
    """Interpolate custom OTF data onto ``f_support``."""
    otf_data = getattr(optics, "otf_data", None)
    otf_support = getattr(optics, "otf_support", None)
    if otf_data is None or otf_support is None:
        raise ValueError("optics.otf_data and optics.otf_support required")
    otf_units = getattr(optics, "otf_support_units", units)

    fx = np.asarray(otf_support["fx"], dtype=float)
    fy = np.asarray(otf_support["fy"], dtype=float)
    scale = _cpd_scale(units, optics) / _cpd_scale(otf_units, optics)
    fx = fx / scale
    fy = fy / scale

    Xo, Yo = np.meshgrid(fx, fy)
    Xi = f_support[:, :, 0]
    Yi = f_support[:, :, 1]
    r, c = Xi.shape

    if otf_data.ndim == 2:
        otf_data = otf_data[:, :, np.newaxis]
    if otf_data.shape[2] == wave.size:
        data_wave = wave
    else:
        data_wave = getattr(optics, "wave", wave)
        if data_wave.size != otf_data.shape[2]:
            raise ValueError("optf_data wavelength dimension mismatch")

    otf = np.zeros((r, c, wave.size), dtype=complex)
    for iw, lam in enumerate(wave):
        if data_wave.size == 1:
            plane = otf_data[:, :, 0]
        else:
            idx = int(np.argmin(np.abs(data_wave - lam)))
            plane = otf_data[:, :, idx]
        interp = RegularGridInterpolator((fy, fx), plane, bounds_error=False, fill_value=0)
        vals = interp(np.stack((Yi.ravel(), Xi.ravel()), axis=-1))
        otf[:, :, iw] = vals.reshape(r, c)
    return otf


def oi_calculate_otf(
    oi: OpticalImage,
    optics: Optics,
    wave: np.ndarray | None = None,
    units: str = "cyclesPerDegree",
) -> tuple[np.ndarray, np.ndarray]:
    """Return optical transfer function for ``oi`` and ``optics``."""
    if wave is None:
        wave = oi.wave
    wave = np.asarray(wave, dtype=float)

    sup = oi_frequency_support(oi, units)
    fx, fy = np.meshgrid(sup["fx"], sup["fy"])
    f_support = np.stack((fx, fy), axis=2)

    model = getattr(optics, "model", "diffractionlimited").lower()

    if model in {"diffractionlimited", "dlmtf"}:
        otf = _dl_otf(oi, optics, f_support, wave, units)
    elif model in {"custom", "shiftinvariant"}:
        otf = _custom_otf(oi, optics, f_support, wave, units)
    else:
        raise ValueError(f"Unknown optics model '{model}'")

    return otf, f_support


__all__ = ["oi_calculate_otf"]
