"""Compute sensor-to-color-space transformation matrices."""

from __future__ import annotations

from pathlib import Path
import numpy as np
from scipy.io import loadmat

from .iset_root_path import iset_root_path
from .illuminant import illuminant_create


_XYZ2LRGB = np.array([
    [3.2410, -1.5374, -0.4986],
    [-0.9692, 1.8760, 0.0416],
    [0.0556, -0.2040, 1.0570],
])


def _interp_data(src_wave: np.ndarray, data: np.ndarray, wave: np.ndarray) -> np.ndarray:
    result = np.zeros((len(wave), data.shape[1]))
    for i in range(data.shape[1]):
        result[:, i] = np.interp(wave, src_wave, data[:, i], left=0.0, right=0.0)
    return result


def _load_surfaces(name: str, wave: np.ndarray) -> np.ndarray:
    root = iset_root_path()
    if name.lower() in {"mcc", "macbeth"}:
        path = root / "data" / "surfaces" / "reflectances" / "macbethChart.mat"
    else:
        raise ValueError("Unknown surface set: %s" % name)
    data = loadmat(path)
    src_wave = data["wavelength"].ravel()
    refl = data["data"]
    return _interp_data(src_wave, refl, wave)


def _load_xyz(wave: np.ndarray) -> np.ndarray:
    root = iset_root_path()
    data = loadmat(root / "data" / "human" / "XYZ.mat")
    src_wave = data["wavelength"].ravel()
    xyz = data["data"]
    return _interp_data(src_wave, xyz, wave)


def ie_color_transform(
    sensor_qe: np.ndarray,
    wave: np.ndarray,
    target_space: str = "XYZ",
    illuminant: str | np.ndarray = "D65",
    surface: str = "macbeth",
) -> np.ndarray:
    """Return a linear transform from sensor space to a color space.

    Parameters
    ----------
    sensor_qe : np.ndarray
        Spectral quantum efficiency of the sensor channels with shape
        ``(n_wavelengths, n_channels)``.
    wave : np.ndarray
        Wavelength sampling corresponding to the rows of ``sensor_qe``.
    target_space : str, optional
        Output color space. ``"XYZ"`` or ``"srgb"`` (linear). Default ``"XYZ"``.
    illuminant : str or np.ndarray, optional
        Illuminant spectral power distribution as a vector matching ``wave`` or
        a name understood by :func:`~isetcam.illuminant.illuminant_create`.
        Default ``"D65"``.
    surface : str, optional
        Name of the reflectance data set used for the fit. Only ``"macbeth"`` is
        currently implemented.

    Returns
    -------
    np.ndarray
        Matrix ``T`` such that ``sensor_values @ T`` yields values in the
        requested color space.
    """
    sensor_qe = np.asarray(sensor_qe, dtype=float)
    wave = np.asarray(wave, dtype=float)
    if sensor_qe.shape[0] != wave.size:
        raise ValueError("sensor_qe and wave must have matching lengths")

    if isinstance(illuminant, str):
        illum = illuminant_create(illuminant, wave)
        ill_spd = illum.spd.astype(float)
    else:
        ill_spd = np.asarray(illuminant, dtype=float)
        if ill_spd.size != wave.size:
            raise ValueError("Illuminant vector must match wave length")

    sur_ref = _load_surfaces(surface, wave)  # (n_wave, n_surfaces)
    sensor_resp = (sensor_qe.T @ (ill_spd[:, None] * sur_ref)).T

    ts = target_space.lower().replace(" ", "")
    if ts in {"xyz", "ciexyz"}:
        target_qe = _load_xyz(wave)
        target_resp = (target_qe.T @ (ill_spd[:, None] * sur_ref)).T
    elif ts in {"srgb", "linearsrgb", "lrgb"}:
        target_qe = _load_xyz(wave)
        xyz_resp = (target_qe.T @ (ill_spd[:, None] * sur_ref)).T
        target_resp = xyz_resp @ _XYZ2LRGB
    else:
        raise ValueError(f"Unknown target space '{target_space}'")

    T, _, _, _ = np.linalg.lstsq(sensor_resp, target_resp, rcond=None)
    return T
