# mypy: ignore-errors
"""Visualize a cone mosaic using a gaussian blurred RGB image."""

from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore


def human_cone_plot(
    positions: np.ndarray,
    cone_types: np.ndarray,
    support: tuple[int, int] | None = None,
    spread: float | None = None,
    delta: float = 0.4,
    ax: "plt.Axes | None" = None,
) -> "plt.Axes":
    """Return axis with gaussian blurred cone mosaic image.

    Parameters
    ----------
    positions : np.ndarray
        ``(N, 2)`` array of cone ``x``/``y`` coordinates in microns.
    cone_types : np.ndarray
        Integer array of cone types using ``1`` for empty, ``2`` for L,
        ``3`` for M and ``4`` for S cones.  May have shape ``(N,)`` or the
        original mosaic shape.
    support : tuple[int, int], optional
        Kernel size used for the gaussian blur.  When ``None`` the kernel
        size is ``(round(3 * spread), round(3 * spread))``.
    spread : float, optional
        Standard deviation in pixels of the gaussian blur.  When ``None``
        it is estimated from the grid spacing of the mosaic.
    delta : float, optional
        Spatial sampling for mapping positions to pixels in microns.
        Defaults to ``0.4`` which mimics the MATLAB implementation.
    ax : matplotlib.axes.Axes, optional
        Axis to draw into.  When ``None`` a new figure and axis are created.

    Returns
    -------
    matplotlib.axes.Axes
        Axis containing the plotted cone mosaic.
    """
    if plt is None:
        raise ImportError("matplotlib is required for human_cone_plot")

    positions = np.asarray(positions, dtype=float)
    cone_types = np.asarray(cone_types)
    if cone_types.ndim > 1:
        cone_types = cone_types.ravel()
    if positions.shape[0] != cone_types.size:
        raise ValueError("positions and cone_types must have compatible sizes")

    x = positions[:, 0]
    y = positions[:, 1]
    x0 = x.min()
    y0 = y.min()
    col = np.round((x - x0) / delta).astype(int)
    row = np.round((y - y0) / delta).astype(int)
    n_rows = row.max() + 1
    n_cols = col.max() + 1

    grid = np.zeros((n_rows, n_cols), dtype=int)
    grid[row, col] = cone_types

    if spread is None:
        first_row = np.where(grid[0, :] > 0)[0]
        if first_row.size >= 2:
            spread = (first_row[1] - first_row[0]) / 3.0
        else:
            spread = 1.0
    if support is None:
        s = int(round(3 * spread))
        support = (s, s)

    cone_image = np.zeros((n_rows, n_cols, 3), dtype=float)
    cone_image[grid == 2, 0] = 1.0
    cone_image[grid == 3, 1] = 1.0
    cone_image[grid == 4, 2] = 1.0

    sigma = spread
    blurred = np.empty_like(cone_image)
    for c in range(3):
        blurred[:, :, c] = gaussian_filter(cone_image[:, :, c], sigma=sigma)

    if ax is None:
        _, ax = plt.subplots()
    ax.imshow(blurred)
    ax.axis("off")
    return ax
