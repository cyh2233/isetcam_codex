# mypy: ignore-errors
"""Render a sensor image to display RGB."""

from __future__ import annotations

import numpy as np

from ..sensor import Sensor
from ..display import Display, display_apply_gamma, display_render
from ..color_transform_matrix import color_transform_matrix
from ..rgb_to_xw_format import rgb_to_xw_format
from ..xw_to_rgb_format import xw_to_rgb_format
from ..imgproc.image_illuminant_correction import image_illuminant_correction
from .vcimage_class import VCImage
from .ip_create import ip_create
from .ip_demosaic import ip_demosaic


def _image_linear_transform(im: np.ndarray, T: np.ndarray) -> np.ndarray:
    """Return ``im`` transformed by ``T`` in either RGB or XW format."""
    if im.ndim == 3:
        xw, r, c = rgb_to_xw_format(im)
        out = xw @ T
        return xw_to_rgb_format(out, r, c)
    if im.ndim == 2:
        if im.shape[1] != T.shape[0]:
            raise ValueError("Matrix dimensions do not align")
        return im @ T
    raise ValueError("Image must be RGB or XW format")


def ip_compute(sensor: Sensor, display: Display) -> VCImage:
    """Return ``VCImage`` rendered from ``sensor`` for ``display``."""

    ip = ip_create(sensor, display)

    # ----- Demosaic -----
    method = getattr(ip, "demosaic_method", None)
    if method is None:
        method = "bilinear"
        ip.demosaic_method = method
    vols = np.asarray(sensor.volts, dtype=float)
    if vols.ndim == 2:
        pattern = getattr(sensor, "filter_color_letters", "rggb")
        rgb = ip_demosaic(vols, pattern, method=method)
    elif vols.ndim == 3 and vols.shape[2] == 3:
        rgb = vols
    else:
        rgb = np.repeat(vols[:, :, None], 3, axis=2)

    # ----- Convert to internal color space -----
    ics = getattr(ip, "internal_cs", None)
    if ics is None:
        ics = "XYZ"
        ip.internal_cs = ics
    cs_key = ics.replace(" ", "").lower()
    if cs_key == "xyz":
        T = color_transform_matrix("srgb2xyz")
        img_ics = _image_linear_transform(rgb, T)
    elif cs_key in {"linearsrgb", "srgb"}:
        img_ics = rgb
    else:
        raise ValueError("Unknown internal color space")

    # ----- Illuminant correction -----
    illum_method = getattr(ip, "illuminant_correction_method", None)
    if illum_method is None:
        illum_method = "none"
        ip.illuminant_correction_method = illum_method
    img_ics, _ = image_illuminant_correction(
        img_ics, method=illum_method, internal_cmf=None, wave=ip.wave
    )

    # ----- Convert to display space -----
    if cs_key == "xyz":
        T = color_transform_matrix("xyz2srgb")
        lin_rgb = _image_linear_transform(img_ics, T)
    else:
        lin_rgb = img_ics

    _ = display_render(lin_rgb, display, apply_gamma=False)

    if display.gamma is not None:
        rgb_out = display_apply_gamma(lin_rgb, display, inverse=True)
    else:
        rgb_out = lin_rgb

    ip.rgb = rgb_out
    return ip
