"""Create a reflectance based display model."""

from __future__ import annotations

import numpy as np

from .display_class import Display
from .display_create import display_create
from .display_set import display_set
from .display_get import display_get
from .display_set_max_luminance import display_set_max_luminance
from ..ie_read_spectra import ie_read_spectra
from ..data_path import data_path
from ..color_transform_matrix import color_transform_matrix
from ..illuminant import illuminant_blackbody
from ..ie_xyz_from_energy import ie_xyz_from_energy


def display_reflectance(ctemp: float, wave: np.ndarray | None = None) -> tuple[Display, np.ndarray, np.ndarray]:
    """Return a display representing surfaces illuminated by a blackbody."""
    if wave is None:
        wave = np.arange(400, 701, 5, dtype=float)
    else:
        wave = np.asarray(wave, dtype=float)

    basis, _, _, _ = ie_read_spectra(data_path('surfaces/reflectanceBasis.mat'), wave)
    basis[:, 0] *= -1

    ill_energy = illuminant_blackbody(float(ctemp), wave)

    radiance_basis = basis[:, :3] * ill_energy[:, np.newaxis]

    lrgb2xyz = color_transform_matrix('lrgb2xyz')
    lXYZinCols = lrgb2xyz.T
    XYZ, _, _, _ = ie_read_spectra(data_path('human/XYZEnergy.mat'), wave)

    T = np.linalg.pinv(XYZ.T @ radiance_basis) @ lXYZinCols
    rgb_primaries = radiance_basis @ T

    disp = display_create()
    display_set(disp, 'wave', wave)
    display_set(disp, 'spd', rgb_primaries)
    display_set_max_luminance(disp, 100)
    disp.gamma = display_create('LCD-Apple').gamma
    disp.name = f'Natural (ill {int(ctemp)}K)'

    scaled_ill = ill_energy * (display_get(disp, 'max_luminance') / 100)
    return disp, disp.spd, scaled_ill


__all__ = ["display_reflectance"]
