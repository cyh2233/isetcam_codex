# mypy: ignore-errors
"""Spatial CIELAB (S-CIELAB) color difference metric."""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Sequence, Tuple
from scipy.signal import fftconvolve

from ..rgb_to_xw_format import rgb_to_xw_format
from ..xw_to_rgb_format import xw_to_rgb_format
from ..xyz_to_lab import xyz_to_lab
from ..lab_to_xyz import lab_to_xyz


@dataclass
class SCIELABParams:
    """Parameters controlling the :func:`scielab` calculation."""

    deltaEversion: str = "2000"
    imageFormat: str = "xyz10"
    sampPerDeg: float = 224.0
    filterSize: int = 224
    filters: Sequence[np.ndarray] | None = None
    filterversion: str = "distribution"


def sc_params(dpi: float = 120.0, dist: float = 0.5) -> SCIELABParams:
    """Return default :class:`SCIELABParams`.

    The defaults match the MATLAB ``scParams`` function and assume a
    120 DPI display viewed from 0.5 meters.
    """

    pixel_spacing = 0.0254 / dpi
    deg_per_pixel = np.degrees(np.arctan(pixel_spacing / dist))
    n_pixel = int(round(1 / deg_per_pixel))

    return SCIELABParams(sampPerDeg=n_pixel, filterSize=n_pixel)


# Opponent conversion matrices (10-deg XYZ)
_XYZ2OPP = np.array(
    [
        [288.5613, 659.7617, -130.5654],
        [-464.8864, 326.2702, 62.4200],
        [79.8787, -554.7976, 481.4746],
    ]
) / 1000
_OPP2XYZ = np.linalg.inv(_XYZ2OPP)


def _ie_hwhm2sd(hwhm: float) -> float:
    return hwhm / np.sqrt(2 * np.log(2))


def _gauss2(hwhm_y: float, support_y: int, hwhm_x: float, support_x: int) -> np.ndarray:
    x = np.arange(support_x) - support_x // 2
    y = np.arange(support_y) - support_y // 2
    X, Y = np.meshgrid(x, y)
    sd_x = _ie_hwhm2sd(hwhm_x)
    sd_y = _ie_hwhm2sd(hwhm_y)
    g = np.exp(-0.5 * ((X / sd_x) ** 2 + (Y / sd_y) ** 2))
    return g / g.sum()


def _sum_gauss(params: Sequence[float]) -> np.ndarray:
    width = int(round(params[0]))
    g = np.zeros((width, width), dtype=float)
    n = (len(params) - 1) // 2
    for i in range(n):
        h = params[2 * i + 1]
        w = params[2 * i + 2]
        g += w * _gauss2(h, width, h, width)
    return g / g.sum()


def _sc_gaussian_parameters(samp_per_deg: float, params: SCIELABParams) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:  # noqa: E501
    v = params.filterversion.lower()
    if v not in {"distribution", "johnson", "original", "published1996", "hires"}:
        v = "distribution"

    if v in {"distribution", "johnson"}:
        x1 = [0.05, 1.00327, 0.225, 0.114416, 7.0, -0.117686]
        x2 = [0.0685, 0.616725, 0.826, 0.383275]
        x3 = [0.0920, 0.567885, 0.6451, 0.432115]
    elif v in {"original", "published1996"}:
        x1 = [0.0283, 0.921, 0.133, 0.105, 4.336, -0.1080]
        x2 = [0.0392, 0.531, 0.494, 0.33]
        x3 = [0.0536, 0.488, 0.386, 0.371]
    else:  # hires
        x1 = [0.0283 / 2, 0.921, 0.133 / 2, 0.105, 4.336 / 2, -0.1080]
        x2 = [0.0392 / 2, 0.531, 0.494 / 2, 0.33]
        x3 = [0.0536 / 2, 0.488, 0.386 / 2, 0.371]

    x1[0], x1[2], x1[4] = [v * samp_per_deg for v in x1[0:5:2]]
    x2[0], x2[2] = [v * samp_per_deg for v in x2[0:3:2]]
    x3[0], x3[2] = [v * samp_per_deg for v in x3[0:3:2]]

    return np.array(x1), np.array(x2), np.array(x3)


def _sc_prepare_filters(params: SCIELABParams) -> Tuple[Tuple[np.ndarray, np.ndarray, np.ndarray], np.ndarray]:  # noqa: E501
    filter_size = int(np.ceil(params.filterSize))
    if filter_size % 2 == 0:
        support = filter_size - 1
    else:
        support = filter_size
    params.filterSize = support
    x1, x2, x3 = _sc_gaussian_parameters(params.sampPerDeg, params)
    f1 = _sum_gauss([support, *x1])
    f2 = _sum_gauss([support, *x2])
    f3 = _sum_gauss([support, *x3])
    support_axis = (np.arange(support) - support // 2) / params.sampPerDeg
    return (f1, f2, f3), support_axis


def _image_linear_transform(im: np.ndarray, T: np.ndarray) -> np.ndarray:
    if im.ndim == 3:
        xw, r, c = rgb_to_xw_format(im)
        out = xw @ T
        return xw_to_rgb_format(out, r, c)
    elif im.ndim == 2:
        if im.shape[1] != T.shape[0]:
            raise ValueError("Matrix dimensions do not align")
        return im @ T
    else:
        raise ValueError("Image must be RGB or XW format")


def _sc_apply_filters(image: np.ndarray, filters: Sequence[np.ndarray]) -> np.ndarray:
    if image.ndim == 2:
        image = image.reshape(1, image.shape[0], image.shape[1])
    out = np.zeros_like(image, dtype=float)
    for i in range(3):
        f = filters[i]
        pad_y = f.shape[0] // 2
        pad_x = f.shape[1] // 2
        padded = np.pad(
            image[:, :, i], ((pad_y, pad_y), (pad_x, pad_x)), mode="reflect"
        )
        conv = fftconvolve(padded, f, mode="same")
        out[:, :, i] = conv[pad_y : pad_y + image.shape[0], pad_x : pad_x + image.shape[1]]  # noqa: E501
    return out


def _sc_opponent_filter(image: np.ndarray, params: SCIELABParams) -> np.ndarray:
    opp = _image_linear_transform(image, _XYZ2OPP)
    filtered = _sc_apply_filters(opp, params.filters)
    return _image_linear_transform(filtered, _OPP2XYZ)


def _delta_e_2000(lab1: np.ndarray, lab2: np.ndarray) -> np.ndarray:
    L1, a1, b1 = lab1[..., 0], lab1[..., 1], lab1[..., 2]
    L2, a2, b2 = lab2[..., 0], lab2[..., 1], lab2[..., 2]

    C1 = np.sqrt(a1 ** 2 + b1 ** 2)
    C2 = np.sqrt(a2 ** 2 + b2 ** 2)
    C_bar = (C1 + C2) / 2

    G = 0.5 * (1 - np.sqrt((C_bar ** 7) / (C_bar ** 7 + 25 ** 7)))
    a1p = (1 + G) * a1
    a2p = (1 + G) * a2

    C1p = np.sqrt(a1p ** 2 + b1 ** 2)
    C2p = np.sqrt(a2p ** 2 + b2 ** 2)

    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360

    dLp = L2 - L1
    dCp = C2p - C1p

    dhp = h2p - h1p
    dhp = np.where(dhp > 180, dhp - 360, dhp)
    dhp = np.where(dhp < -180, dhp + 360, dhp)
    dhp = np.where((C1p * C2p) == 0, 0, dhp)

    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp) / 2)

    Lp_bar = (L1 + L2) / 2
    Cp_bar = (C1p + C2p) / 2

    hp_bar = h1p + h2p
    hp_bar = np.where(np.abs(h1p - h2p) > 180, hp_bar + 360, hp_bar)
    hp_bar = np.where((C1p * C2p) == 0, h1p + h2p, hp_bar)
    hp_bar /= 2

    T = (
        1
        - 0.17 * np.cos(np.radians(hp_bar - 30))
        + 0.24 * np.cos(np.radians(2 * hp_bar))
        + 0.32 * np.cos(np.radians(3 * hp_bar + 6))
        - 0.2 * np.cos(np.radians(4 * hp_bar - 63))
    )

    dtheta = 30 * np.exp(-((hp_bar - 275) / 25) ** 2)
    Rc = 2 * np.sqrt((Cp_bar ** 7) / (Cp_bar ** 7 + 25 ** 7))

    Sl = 1 + (0.015 * ((Lp_bar - 50) ** 2)) / np.sqrt(20 + (Lp_bar - 50) ** 2)
    Sc = 1 + 0.045 * Cp_bar
    Sh = 1 + 0.015 * Cp_bar * T

    Rt = -Rc * np.sin(2 * np.radians(dtheta))

    dE = np.sqrt(
        (dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh)  # noqa: E501
    )
    return dE


def _sc_compute_difference(xyz1: np.ndarray, xyz2: np.ndarray, white: Sequence[np.ndarray] | np.ndarray, version: str) -> np.ndarray:  # noqa: E501
    if isinstance(white, Sequence) and not isinstance(white, np.ndarray):
        w1, w2 = white[0], white[1]
    else:
        w1 = w2 = white

    lab1 = xyz_to_lab(xyz1, w1)
    lab2 = xyz_to_lab(xyz2, w2)

    version = version.lower()
    if version in {"2000", "de2000", "ciede2000"}:
        de = _delta_e_2000(lab1, lab2)
    elif version in {"1976", "lab"}:
        diff = lab1 - lab2
        de = np.sqrt(np.sum(diff ** 2, axis=-1))
    else:
        raise ValueError(f"Unsupported deltaE version: {version}")

    return de


def scielab(image1: np.ndarray, image2: np.ndarray, white_point: Sequence[np.ndarray] | np.ndarray, params: SCIELABParams | None = None) -> np.ndarray:  # noqa: E501
    """Return the Spatial CIELAB error map between ``image1`` and ``image2``.

    ``image1`` and ``image2`` should be XYZ images in either ``(M,N,3)`` RGB
    format or ``(P,3)`` XW format. ``white_point`` may be a single XYZ
    white or a sequence ``(wp1, wp2)`` giving separate white points for the
    two images.
    """

    if params is None:
        params = sc_params()

    if params.filters is None:
        params.filters, _ = _sc_prepare_filters(params)

    if image1.ndim == 2:
        image1 = image1.reshape(1, image1.shape[0], image1.shape[1])
    if image2.ndim == 2:
        image2 = image2.reshape(1, image2.shape[0], image2.shape[1])

    xyz1 = _sc_opponent_filter(image1, params)
    xyz2 = _sc_opponent_filter(image2, params)

    return _sc_compute_difference(xyz1, xyz2, white_point, params.deltaEversion)


__all__ = ["SCIELABParams", "sc_params", "scielab"]
