# mypy: ignore-errors
"""Adaptive Laplacian demosaicing for Bayer-pattern images."""

from __future__ import annotations

import numpy as np


def _mosaic_converter(bayer: np.ndarray, pattern: str) -> tuple[np.ndarray, str]:
    """Convert Bayer mosaic ``pattern`` to ``grbg`` layout.

    This replicates a subset of MATLAB ``mosaicConverter`` used by
    :func:`adaptive_laplacian`.
    """
    pattern = pattern.lower()
    if pattern == "grbg":
        return bayer, "grbg"
    out = np.empty_like(bayer)
    if pattern == "rggb":
        out[:, :-1] = bayer[:, 1:]
        out[:, -1] = bayer[:, -2]
    elif pattern == "bggr":
        out[:-1, :] = bayer[1:, :]
        out[-1, :] = bayer[-2, :]
    elif pattern == "gbrg":
        out[:-1, :-1] = bayer[1:, 1:]
        out[-1, :] = bayer[-2, :]
        out[:, -1] = bayer[:, -2]
    else:
        raise ValueError("Unsupported CFA pattern")
    return out, "grbg"


def adaptive_laplacian(bayer: np.ndarray, pattern: str) -> np.ndarray:
    """Demosaic ``bayer`` using the adaptive Laplacian method.

    Parameters
    ----------
    bayer : np.ndarray
        2-D Bayer mosaic image.
    pattern : str
        CFA pattern such as ``"rggb"``.

    Returns
    -------
    np.ndarray
        RGB image with shape ``(rows, cols, 3)``.
    """
    bayer = np.asarray(bayer, dtype=float)
    if bayer.ndim != 2:
        raise ValueError("bayer must be a 2-D array")

    bayer, pattern = _mosaic_converter(bayer, pattern)

    rows, cols = bayer.shape
    rgb = np.zeros((rows, cols, 3), dtype=float)

    # pattern is now 'grbg'
    r_mask = np.zeros_like(bayer, dtype=bool)
    r_mask[0::2, 1::2] = True
    b_mask = np.zeros_like(bayer, dtype=bool)
    b_mask[1::2, 0::2] = True
    g1_mask = np.zeros_like(bayer, dtype=bool)
    g1_mask[0::2, 0::2] = True
    g2_mask = np.zeros_like(bayer, dtype=bool)
    g2_mask[1::2, 1::2] = True

    rgb[r_mask, 0] = bayer[r_mask]
    rgb[b_mask, 2] = bayer[b_mask]
    rgb[g1_mask | g2_mask, 1] = bayer[g1_mask | g2_mask]

    # Pad with two pixels on each side
    bayer_ex = np.pad(rgb, ((2, 2), (2, 2), (0, 0)), mode="edge")
    vex, hex_ = bayer_ex.shape[:2]

    def s(parity: int, length: int) -> slice:
        return slice(2 + parity, length - 2, 2)

    def d(parity: int, length: int) -> slice:
        return slice(parity, length, 2)

    def shift(sl: slice, shift: int) -> slice:
        return slice(sl.start + shift, sl.stop + shift, sl.step)

    ry, rx = s(0, vex), s(1, hex_)
    by, bx = s(1, vex), s(0, hex_)
    g1y, g1x = s(0, vex), s(0, hex_)
    g2y, g2x = s(1, vex), s(1, hex_)

    # Red pixels: estimate green
    gdH = bayer_ex[g1y, g1x, 1] - bayer_ex[g1y, shift(g1x, 2), 1]
    gdV = bayer_ex[g2y, g2x, 1] - bayer_ex[shift(g2y, -2), g2x, 1]
    gsH = bayer_ex[g1y, g1x, 1] + bayer_ex[g1y, shift(g1x, 2), 1]
    gsV = bayer_ex[g2y, g2x, 1] + bayer_ex[shift(g2y, -2), g2x, 1]
    rH = (
        2 * bayer_ex[ry, rx, 0]
        - bayer_ex[ry, shift(rx, -2), 0]
        - bayer_ex[ry, shift(rx, 2), 0]
    )
    rV = (
        2 * bayer_ex[ry, rx, 0]
        - bayer_ex[shift(ry, -2), rx, 0]
        - bayer_ex[shift(ry, 2), rx, 0]
    )
    deltaH = np.abs(gdH) + np.abs(rH)
    deltaV = np.abs(gdV) + np.abs(rV)
    val = (
        (deltaH < deltaV) * (0.50 * gsH + 0.25 * rH)
        + (deltaH > deltaV) * (0.50 * gsV + 0.25 * rV)
        + (deltaH == deltaV) * (0.25 * (gsH + gsV) + 0.125 * (rH + rV))
    )
    rgb[d(0, rows), d(1, cols), 1] = val

    # Blue pixels: estimate green
    gdH = bayer_ex[g2y, g2x, 1] - bayer_ex[g2y, shift(g2x, -2), 1]
    gdV = bayer_ex[g1y, g1x, 1] - bayer_ex[shift(g1y, 2), g1x, 1]
    gsH = bayer_ex[g2y, g2x, 1] + bayer_ex[g2y, shift(g2x, -2), 1]
    gsV = bayer_ex[g1y, g1x, 1] + bayer_ex[shift(g1y, 2), g1x, 1]
    bH = (
        2 * bayer_ex[by, bx, 0]
        - bayer_ex[by, shift(bx, -2), 0]
        - bayer_ex[by, shift(bx, 2), 0]
    )
    bV = (
        2 * bayer_ex[by, bx, 0]
        - bayer_ex[shift(by, -2), bx, 0]
        - bayer_ex[shift(by, 2), bx, 0]
    )
    deltaH = np.abs(gdH) + np.abs(bH)
    deltaV = np.abs(gdV) + np.abs(bV)
    val = (
        (deltaH < deltaV) * (0.50 * gsH + 0.25 * bH)
        + (deltaH > deltaV) * (0.50 * gsV + 0.25 * bV)
        + (deltaH == deltaV) * (0.25 * (gsH + gsV) + 0.125 * (bH + bV))
    )
    rgb[d(1, rows), d(0, cols), 1] = val

    # Update green channel in extended mosaic
    grn = np.pad(rgb[:, :, 1], ((2, 2), (2, 2)), mode="edge")
    bayer_ex[:, :, 1] = grn

    # Green pixels: estimate red
    val = (
        0.5 * (bayer_ex[ry, rx, 0] + bayer_ex[ry, shift(rx, -2), 0])
        + 0.25
        * (
            2 * bayer_ex[g1y, g1x, 1]
            - bayer_ex[ry, shift(rx, -2), 1]
            - bayer_ex[ry, rx, 1]
        )
    )
    rgb[d(0, rows), d(0, cols), 0] = val

    val = (
        0.5 * (bayer_ex[ry, rx, 0] + bayer_ex[shift(ry, 2), rx, 0])
        + 0.25
        * (
            2 * bayer_ex[g2y, g2x, 1]
            - bayer_ex[shift(ry, 2), rx, 1]
            - bayer_ex[ry, rx, 1]
        )
    )
    rgb[d(1, rows), d(1, cols), 0] = val

    # Green pixels: estimate blue
    val = (
        0.5 * (bayer_ex[by, bx, 2] + bayer_ex[by, shift(bx, 2), 2])
        + 0.25
        * (
            2 * bayer_ex[g2y, g2x, 1]
            - bayer_ex[by, shift(bx, 2), 1]
            - bayer_ex[by, bx, 1]
        )
    )
    rgb[d(1, rows), d(1, cols), 2] = val

    val = (
        0.5 * (bayer_ex[by, bx, 2] + bayer_ex[shift(by, -2), bx, 2])
        + 0.25
        * (
            2 * bayer_ex[g1y, g1x, 1]
            - bayer_ex[shift(by, -2), bx, 1]
            - bayer_ex[by, bx, 1]
        )
    )
    rgb[d(0, rows), d(0, cols), 2] = val

    # Blue pixels: estimate red
    rdN = bayer_ex[ry, shift(rx, -2), 0] - bayer_ex[shift(ry, 2), rx, 0]
    rdP = bayer_ex[ry, rx, 0] - bayer_ex[shift(ry, 2), shift(rx, -2), 0]
    rsN = bayer_ex[ry, shift(rx, -2), 0] + bayer_ex[shift(ry, 2), rx, 0]
    rsP = bayer_ex[ry, rx, 0] + bayer_ex[shift(ry, 2), shift(rx, -2), 0]
    gN = (
        2 * bayer_ex[by, bx, 1]
        - bayer_ex[ry, shift(rx, -2), 1]
        - bayer_ex[shift(ry, 2), rx, 1]
    )
    gP = (
        2 * bayer_ex[by, bx, 1]
        - bayer_ex[ry, rx, 1]
        - bayer_ex[shift(ry, 2), shift(rx, -2), 1]
    )
    deltaN = np.abs(rdN) + np.abs(gN)
    deltaP = np.abs(rdP) + np.abs(gP)
    val = (
        (deltaN < deltaP) * (0.50 * rsN + 0.25 * gN)
        + (deltaN > deltaP) * (0.50 * rsP + 0.25 * gP)
        + (deltaN == deltaP) * (0.25 * (rsN + rsP) + 0.125 * (gN + gP))
    )
    rgb[d(1, rows), d(0, cols), 0] = val

    # Red pixels: estimate blue
    bdN = bayer_ex[shift(by, -2), bx, 2] - bayer_ex[by, shift(bx, 2), 2]
    bdP = bayer_ex[by, bx, 2] - bayer_ex[shift(by, -2), shift(bx, 2), 2]
    bsN = bayer_ex[shift(by, -2), bx, 2] + bayer_ex[by, shift(bx, 2), 2]
    bsP = bayer_ex[by, bx, 2] + bayer_ex[shift(by, -2), shift(bx, 2), 2]
    gN = (
        2 * bayer_ex[ry, rx, 1]
        - bayer_ex[shift(by, -2), bx, 1]
        - bayer_ex[by, shift(bx, 2), 1]
    )
    gP = (
        2 * bayer_ex[ry, rx, 1]
        - bayer_ex[by, bx, 1]
        - bayer_ex[shift(by, -2), shift(bx, 2), 1]
    )
    deltaN = np.abs(bdN) + np.abs(gN)
    deltaP = np.abs(bdP) + np.abs(gP)
    val = (
        (deltaN < deltaP) * (0.50 * bsN + 0.25 * gN)
        + (deltaN > deltaP) * (0.50 * bsP + 0.25 * gP)
        + (deltaN == deltaP) * (0.25 * (bsN + bsP) + 0.125 * (gN + gP))
    )
    rgb[d(0, rows), d(1, cols), 2] = val

    return rgb
