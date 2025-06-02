# mypy: ignore-errors
"""Determine pixel positions for a Bayer mosaic."""

from __future__ import annotations

from typing import Sequence, Tuple

import numpy as np


def bayer_indices(
    pattern: str,
    size: int | Sequence[int],
    clip: int = 0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:  # noqa: E501
    """Return index arrays for R, B, G1 and G2 pixels.

    Parameters
    ----------
    pattern : str
        CFA pattern such as ``"rggb"`` or ``"grbg"``.
    size : int | Sequence[int]
        Image size given either as ``(rows, cols)`` or a single integer for
        square images.
    clip : int, optional
        Number of pixels to ignore at each border. Default is ``0``.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]  # noqa: E501
        Arrays ``(rx, ry, bx, by, g1x, g1y, g2x, g2y)`` containing zero-based
        column and row indices of the respective pixel types.
    """

    if isinstance(size, int):
        vex = hex_ = int(size)
    else:
        if len(size) != 2:
            raise ValueError("size must be an int or a length-2 sequence")
        vex, hex_ = int(size[0]), int(size[1])

    pattern = pattern.lower()
    if pattern not in {"rggb", "grbg", "gbrg", "bggr"}:
        raise ValueError("Unsupported Bayer pattern")

    c0 = np.arange(clip, hex_ - clip, 2, dtype=int)
    c1 = np.arange(1 + clip, hex_ - clip, 2, dtype=int)
    r0 = np.arange(clip, vex - clip, 2, dtype=int)
    r1 = np.arange(1 + clip, vex - clip, 2, dtype=int)

    if pattern == "grbg":
        g1x, g1y = c0, r0
        rx, ry = c1, r0
        bx, by = c0, r1
        g2x, g2y = c1, r1
    elif pattern == "rggb":
        g1x, g1y = c1, r0
        rx, ry = c0, r0
        bx, by = c1, r1
        g2x, g2y = c0, r1
    elif pattern == "gbrg":
        g1x, g1y = c0, r0
        rx, ry = c0, r1
        bx, by = c1, r0
        g2x, g2y = c1, r1
    else:  # pattern == "bggr"
        g1x, g1y = c1, r0
        rx, ry = c1, r1
        bx, by = c0, r0
        g2x, g2y = c0, r1

    return rx, ry, bx, by, g1x, g1y, g2x, g2y
