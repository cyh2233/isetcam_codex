# mypy: ignore-errors
"""Conversions between RGB, HSV, and HSL color spaces."""

from __future__ import annotations

import numpy as np


_DEF_SHAPE_ERR = "Input must be (rows, cols, 3) or (n, 3)"


def _check_rgb_shape(arr: np.ndarray) -> None:
    if arr.ndim == 3 and arr.shape[2] == 3:
        return
    if arr.ndim == 2 and arr.shape[1] == 3:
        return
    raise ValueError(_DEF_SHAPE_ERR)


def rgb_to_hsv(rgb: np.ndarray) -> np.ndarray:
    """Convert RGB values to HSV.

    Parameters
    ----------
    rgb : np.ndarray
        RGB values in either ``(n, 3)`` or ``(rows, cols, 3)`` format.

    Returns
    -------
    np.ndarray
        HSV values in the same shape as ``rgb``.
    """
    rgb = np.asarray(rgb, dtype=float)
    _check_rgb_shape(rgb)

    r = rgb[..., 0]
    g = rgb[..., 1]
    b = rgb[..., 2]

    maxc = np.maximum.reduce([r, g, b])
    minc = np.minimum.reduce([r, g, b])
    delta = maxc - minc

    v = maxc

    s = np.zeros_like(maxc)
    nz = maxc != 0
    s[nz] = delta[nz] / maxc[nz]

    h = np.zeros_like(maxc)
    mask = delta != 0
    rc = np.zeros_like(maxc)
    gc = np.zeros_like(maxc)
    bc = np.zeros_like(maxc)
    rc[mask] = (g[mask] - b[mask]) / delta[mask]
    gc[mask] = (b[mask] - r[mask]) / delta[mask] + 2
    bc[mask] = (r[mask] - g[mask]) / delta[mask] + 4
    h[mask & (maxc == r)] = rc[mask & (maxc == r)]
    h[mask & (maxc == g)] = gc[mask & (maxc == g)]
    h[mask & (maxc == b)] = bc[mask & (maxc == b)]
    h = (h / 6.0) % 1.0

    hsv = np.stack((h, s, v), axis=-1)
    return hsv


def hsv_to_rgb(hsv: np.ndarray) -> np.ndarray:
    """Convert HSV values to RGB."""
    hsv = np.asarray(hsv, dtype=float)
    _check_rgb_shape(hsv)

    h = hsv[..., 0]
    s = hsv[..., 1]
    v = hsv[..., 2]

    r = np.empty_like(h)
    g = np.empty_like(h)
    b = np.empty_like(h)

    i = np.floor(h * 6).astype(int)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6

    mask = i == 0
    r[mask], g[mask], b[mask] = v[mask], t[mask], p[mask]
    mask = i == 1
    r[mask], g[mask], b[mask] = q[mask], v[mask], p[mask]
    mask = i == 2
    r[mask], g[mask], b[mask] = p[mask], v[mask], t[mask]
    mask = i == 3
    r[mask], g[mask], b[mask] = p[mask], q[mask], v[mask]
    mask = i == 4
    r[mask], g[mask], b[mask] = t[mask], p[mask], v[mask]
    mask = i == 5
    r[mask], g[mask], b[mask] = v[mask], p[mask], q[mask]

    rgb = np.stack((r, g, b), axis=-1)
    return rgb


def rgb_to_hsl(rgb: np.ndarray) -> np.ndarray:
    """Convert RGB values to HSL."""
    rgb = np.asarray(rgb, dtype=float)
    _check_rgb_shape(rgb)

    r = rgb[..., 0]
    g = rgb[..., 1]
    b = rgb[..., 2]

    maxc = np.maximum.reduce([r, g, b])
    minc = np.minimum.reduce([r, g, b])
    delta = maxc - minc

    l = (maxc + minc) / 2

    s = np.zeros_like(l)
    mask = delta != 0
    s[mask] = np.where(
        l[mask] < 0.5,
        delta[mask] / (maxc[mask] + minc[mask]),
        delta[mask] / (2 - maxc[mask] - minc[mask]),
    )

    h = np.zeros_like(l)
    rc = np.zeros_like(l)
    gc = np.zeros_like(l)
    bc = np.zeros_like(l)
    rc[mask] = (g[mask] - b[mask]) / delta[mask]
    gc[mask] = (b[mask] - r[mask]) / delta[mask] + 2
    bc[mask] = (r[mask] - g[mask]) / delta[mask] + 4
    h[mask & (maxc == r)] = rc[mask & (maxc == r)]
    h[mask & (maxc == g)] = gc[mask & (maxc == g)]
    h[mask & (maxc == b)] = bc[mask & (maxc == b)]
    h = (h / 6.0) % 1.0

    hsl = np.stack((h, s, l), axis=-1)
    return hsl


def hsl_to_rgb(hsl: np.ndarray) -> np.ndarray:
    """Convert HSL values to RGB."""
    hsl = np.asarray(hsl, dtype=float)
    _check_rgb_shape(hsl)

    h = hsl[..., 0]
    s = hsl[..., 1]
    l = hsl[..., 2]

    r = np.empty_like(h)
    g = np.empty_like(h)
    b = np.empty_like(h)

    mask = s == 0
    r[mask] = l[mask]
    g[mask] = l[mask]
    b[mask] = l[mask]

    notmask = ~mask
    if np.any(notmask):
        q = np.where(l[notmask] < 0.5,
                      l[notmask] * (1 + s[notmask]),
                      l[notmask] + s[notmask] - l[notmask] * s[notmask])
        p = 2 * l[notmask] - q

        tr = (h[notmask] + 1/3) % 1.0
        tg = h[notmask] % 1.0
        tb = (h[notmask] - 1/3) % 1.0

        def hue_to_rgb(t):
            res = np.empty_like(t)
            c1 = t < 1 / 6
            c2 = (t >= 1 / 6) & (t < 1 / 2)
            c3 = (t >= 1 / 2) & (t < 2 / 3)
            res[c1] = p[c1] + (q[c1] - p[c1]) * 6 * t[c1]
            res[c2] = q[c2]
            res[c3] = p[c3] + (q[c3] - p[c3]) * (2 / 3 - t[c3]) * 6
            res[~(c1 | c2 | c3)] = p[~(c1 | c2 | c3)]
            return res

        r[notmask] = hue_to_rgb(tr)
        g[notmask] = hue_to_rgb(tg)
        b[notmask] = hue_to_rgb(tb)

    rgb = np.stack((r, g, b), axis=-1)
    return rgb
