# mypy: ignore-errors
"""Generate a list of random faulty pixel coordinates."""

from __future__ import annotations

import numpy as np


def faulty_list(
    row: int,
    col: int,
    n_bad_pixels: int | None = None,
    min_separation: int = 2,
) -> np.ndarray:
    """Return a list of randomly spaced pixel locations.

    Parameters
    ----------
    row, col : int
        Image size in rows and columns.
    n_bad_pixels : int, optional
        Number of faulty pixels to generate. Default is ``1%`` of pixels.
    min_separation : int, optional
        Minimum Euclidean distance between faulty pixels. Default is ``2``.

    Returns
    -------
    np.ndarray
        Array of shape ``(N, 2)`` with columns ``(x, y)``.
    """
    if n_bad_pixels is None:
        n_bad_pixels = int(round(row * col * 0.01))
    if n_bad_pixels < 0:
        raise ValueError("n_bad_pixels must be non-negative")
    if n_bad_pixels == 0:
        return np.empty((0, 2), dtype=int)

    if n_bad_pixels * min_separation * 4 > row * col:
        raise ValueError("Separation parameter and size are poorly chosen")

    coords: list[tuple[int, int]] = []
    rng = np.random.default_rng()
    attempts = 0
    while len(coords) < n_bad_pixels:
        x = int(rng.integers(0, col))
        y = int(rng.integers(0, row))
        candidate = (x, y)
        # ensure unique and adequately separated
        ok = True
        for ex in coords:
            if ex == candidate:
                ok = False
                break
            if np.hypot(ex[0] - x, ex[1] - y) < min_separation:
                ok = False
                break
        if ok:
            coords.append(candidate)
        attempts += 1
        if attempts > 10000:
            raise RuntimeError("unable to generate faulty pixel list")

    return np.array(coords, dtype=int)
