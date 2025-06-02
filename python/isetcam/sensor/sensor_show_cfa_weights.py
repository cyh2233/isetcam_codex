# mypy: ignore-errors
"""Visualize weights using the sensor's CFA colors."""

from __future__ import annotations

from typing import Tuple

import numpy as np

from .sensor_class import Sensor
from .sensor_show_cfa import _COLOR_MAP, _parse_pattern
from ..ie_scale import ie_scale


def sensor_show_cfa_weights(
    weights: np.ndarray,
    sensor: Sensor,
    c_pos: Tuple[int, int] | None = None,
    *,
    img_scale: int = 32,
) -> np.ndarray:
    """Return an RGB image of ``weights`` colored by the sensor CFA."""

    w = np.asarray(weights, dtype=float)
    if w.ndim != 2:
        raise ValueError("weights must be a 2-D array")

    patch_size = w.shape
    if c_pos is None:
        c_pos = (patch_size[0] // 2, patch_size[1] // 2)
    if len(c_pos) != 2:
        raise ValueError("c_pos must have length 2")
    c_row, c_col = int(c_pos[0]), int(c_pos[1])

    letters = getattr(sensor, "filter_color_letters", None)
    if letters is None:
        raise ValueError("sensor has no 'filter_color_letters' attribute")
    pattern = _parse_pattern(letters)
    if pattern is None:
        raise ValueError("filter_color_letters must form a square CFA pattern")
    pattern = np.asarray(pattern)

    pr, pc = pattern.shape
    rr = patch_size[0] // pr + 21
    cc = patch_size[1] // pc + 21
    mosaic = np.tile(pattern, (rr, cc))

    center_row = pr * 10 + c_row
    center_col = pc * 10 + c_col
    h_row = patch_size[0] // 2
    h_col = patch_size[1] // 2
    start_r = center_row - h_row
    start_c = center_col - h_col
    patch_letters = mosaic[
        start_r : start_r + patch_size[0], start_c : start_c + patch_size[1]
    ]

    cfa_img = np.zeros(patch_letters.shape + (3,), dtype=float)
    for ltr, color in _COLOR_MAP.items():
        mask = patch_letters == ltr
        cfa_img[mask, :] = color

    if np.max(w) == np.min(w):
        w_scaled = np.ones_like(w)
    else:
        w_scaled, _, _ = ie_scale(w, 0.0, 1.0)

    img = w_scaled[:, :, None] * cfa_img

    if img_scale > 1:
        img = np.repeat(np.repeat(img, img_scale, axis=0), img_scale, axis=1)

    return img


__all__ = ["sensor_show_cfa_weights"]
