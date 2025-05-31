"""Plot points on the CIE xy chromaticity diagram."""

from __future__ import annotations

import numpy as np
from pathlib import Path
from scipy.io import loadmat

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore

from .chromaticity import chromaticity
from .srgb_xyz import xyz_to_srgb


def chromaticity_plot(
    x: np.ndarray | None = None,
    y: np.ndarray | None = None,
    ax: "plt.Axes | None" = None,
) -> "plt.Axes":
    """Return axis with xy chromaticity diagram and optional points.

    Parameters
    ----------
    x, y : np.ndarray, optional
        Arrays of x and y coordinates.  If ``x`` has shape ``(N, 2)`` and ``y``
        is ``None`` the two columns are interpreted as x and y.
    ax : matplotlib.axes.Axes, optional
        Axis to draw into. When ``None`` a new figure and axis are created.

    Returns
    -------
    matplotlib.axes.Axes
        Axis containing the chromaticity diagram.
    """
    if plt is None:
        raise ImportError("matplotlib is required for chromaticity_plot")

    if y is None and x is not None and x.ndim == 2 and x.shape[1] == 2:
        x, y = x[:, 0], x[:, 1]
    x = np.asarray(x, dtype=float) if x is not None else np.empty(0)
    y = np.asarray(y, dtype=float) if y is not None else np.empty(0)
    if x.size and x.shape != y.shape:
        raise ValueError("x and y must have the same shape")

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    # Load CIE XYZ color matching functions for wavelengths 370-730 nm
    from .data_path import data_path
    data = loadmat(data_path("human/XYZ.mat"))
    XYZ = data["data"]
    xy = chromaticity(XYZ)

    # Convert locus colors to sRGB for display
    srgb, _, _ = xyz_to_srgb(XYZ)
    srgb = np.clip(srgb, 0.0, 1.0)

    # Plot horseshoe locus coloured by wavelength
    for i in range(len(xy) - 1):
        ax.plot(
            xy[i : i + 2, 0],
            xy[i : i + 2, 1],
            color=srgb[i],
            linewidth=2,
        )
    ax.plot([xy[-1, 0], xy[0, 0]], [xy[-1, 1], xy[0, 1]], color=srgb[-1], linewidth=2)

    if x.size:
        ax.plot(x, y, "ko", markerfacecolor="none")

    ax.set_xlim(0.0, 0.8)
    ax.set_ylim(0.0, 0.9)
    ax.set_xlabel("CIE x")
    ax.set_ylabel("CIE y")
    ax.grid(True)

    fig.tight_layout()
    return ax
