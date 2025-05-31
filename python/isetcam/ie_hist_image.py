"""Image histogram plotting utility."""

from __future__ import annotations

import numpy as np

try:  # pragma: no cover - matplotlib might not be installed
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore


def ie_hist_image(img: np.ndarray, bins: int = 256, ax: "plt.Axes | None" = None) -> "plt.Axes":
    """Plot a histogram of ``img`` pixel values.

    Parameters
    ----------
    img : np.ndarray
        Input image array. Can be 2-D grayscale or 3-D RGB with shape
        ``(R, C, 3)``.
    bins : int, optional
        Number of histogram bins, by default ``256``.
    ax : matplotlib.axes.Axes, optional
        Axis to plot the histogram into. When ``None`` a new figure and
        axis are created.

    Returns
    -------
    matplotlib.axes.Axes
        Axis containing the histogram plot.
    """
    if plt is None:
        raise ImportError("matplotlib is required for ie_hist_image")

    img = np.asarray(img, dtype=float)
    if img.ndim == 2:
        channels = 1
    elif img.ndim == 3 and img.shape[2] == 3:
        channels = 3
    else:
        raise ValueError("img must be 2-D grayscale or 3-D RGB array")

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    vmin = float(img.min())
    vmax = float(img.max())

    if channels == 1:
        hist, edges = np.histogram(img.ravel(), bins=bins, range=(vmin, vmax))
        width = edges[1] - edges[0]
        ax.bar(edges[:-1], hist, width=width, color="gray", edgecolor="none")
    else:
        colors = ("r", "g", "b")
        for i, color in enumerate(colors):
            data = img[:, :, i].ravel()
            hist, edges = np.histogram(data, bins=bins, range=(vmin, vmax))
            width = edges[1] - edges[0]
            ax.bar(edges[:-1], hist, width=width, color=color, alpha=0.5, edgecolor="none")

    ax.set_xlabel("Pixel value")
    ax.set_ylabel("Count")
    fig.tight_layout()
    return ax


__all__ = ["ie_hist_image"]
