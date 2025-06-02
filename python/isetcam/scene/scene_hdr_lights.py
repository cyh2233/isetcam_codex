# mypy: ignore-errors
"""Create an HDR scene with simple geometric lights."""

from __future__ import annotations

import numpy as np
from skimage.draw import disk, rectangle

from .scene_class import Scene

_DEF_WAVE = np.arange(400, 701, 10, dtype=float)


def _draw_lights(size: int) -> np.ndarray:
    img = np.zeros((size, size), dtype=float)

    # Circles across the top quarter
    centers = np.linspace(0.2, 0.8, 4) * size
    radii = np.array([0.01, 0.035, 0.07, 0.1]) * size
    row = int(round(size * 0.25))
    for c, r in zip(centers, radii):
        rr, cc = disk((row, c), r, shape=img.shape)
        img[rr, cc] = 1

    # Lines in the middle
    centers = np.linspace(0.1, 0.8, 4) * size
    row = int(round(size * 0.5))
    lengths = np.array([7, 3, 1, 1]) * (0.02 * size)
    widths = np.array([1, 1, 3, 8]) * (0.02 * size)
    for c, l, w in zip(centers, lengths, widths):
        start = (int(row - w / 2), int(c))
        end = (int(row + w / 2), int(c + l))
        rr, cc = rectangle(start, end, shape=img.shape)
        img[rr, cc] = 1

    # Squares near the bottom
    centers = np.linspace(0.1, 0.7, 3) * size
    row = int(round(size * 0.75))
    sizes = np.array([2, 5, 9]) * (size / 64)
    for c, s in zip(centers, sizes):
        start = (int(row - s / 2), int(c - s / 2))
        end = (int(row + s / 2), int(c + s / 2))
        rr, cc = rectangle(start, end, shape=img.shape)
        img[rr, cc] = 1

    return img


def scene_hdr_lights(
    *,
    image_size: int = 384,
    dynamic_range: float = 1e7,
    wave: np.ndarray | None = None,
) -> Scene:
    """Return a simple HDR lights scene."""

    if wave is None:
        wave = _DEF_WAVE
    else:
        wave = np.asarray(wave, dtype=float).reshape(-1)

    pattern = _draw_lights(image_size)
    photons = np.ones((image_size, image_size, wave.size), dtype=float)
    photons[pattern > 0] = dynamic_range

    return Scene(photons=photons, wave=wave, name="HDR lights")
