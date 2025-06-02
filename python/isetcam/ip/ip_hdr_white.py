# mypy: ignore-errors
"""Whiten near-saturated pixels in a VCImage."""

from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter

from .vcimage_class import VCImage


def ip_hdr_white(
    ip: VCImage,
    *,
    saturation: float | None = None,
    hdr_level: float = 0.95,
    wgt_blur: float = 1.0,
    white_level: float = 1.0,
) -> tuple[VCImage, np.ndarray]:
    """Return ``ip`` with bright regions shifted toward white.

    Parameters
    ----------
    ip : VCImage
        Image to modify in-place.
    saturation : float, optional
        Level at which input values are considered saturated. Defaults to
        the maximum value of ``ip.rgb`` when ``None``.
    hdr_level : float, optional
        Fraction of ``saturation`` from which the whitening begins. Pixels
        below this fraction are unaffected. Defaults to ``0.95``.
    wgt_blur : float, optional
        Standard deviation of the Gaussian filter used to blur the weight
        map. Defaults to ``1.0``.
    white_level : float, optional
        Desired output level for the brightest region. Defaults to ``1.0``.

    Returns
    -------
    tuple
        ``(ip, weights)`` where ``ip`` is the same instance with modified
        ``rgb`` data and ``weights`` is the 2-D map of whitening weights.
    """

    rgb = np.asarray(ip.rgb, dtype=float)
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError("ip.rgb must have shape (H, W, 3)")

    if saturation is None:
        saturation = float(rgb.max())

    luminance = rgb.mean(axis=2)
    wgts = (luminance / saturation - hdr_level) / (1.0 - hdr_level)
    wgts = np.clip(wgts, 0.0, 1.0)
    if wgt_blur > 0:
        wgts = gaussian_filter(wgts, sigma=float(wgt_blur), mode="nearest")

    new_rgb = rgb * (1.0 - wgts[..., None]) + white_level * wgts[..., None]

    lum_max = new_rgb.mean(axis=2).max()
    if lum_max > 0:
        new_rgb *= white_level / lum_max

    ip.rgb = new_rgb
    return ip, wgts


__all__ = ["ip_hdr_white"]
