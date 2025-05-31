"""Visualize different properties of a Display."""

from __future__ import annotations

import numpy as np

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore

from .display_class import Display
from ..ie_xyz_from_energy import ie_xyz_from_energy
from ..chromaticity import chromaticity


_DEF_COLORS = ["r", "g", "b"]


def display_plot(display: Display, kind: str = "spd", ax: "plt.Axes | None" = None) -> "plt.Axes":  # noqa: E501
    """Plot information about ``display``.

    Parameters
    ----------
    display : Display
        Display definition.
    kind : str, optional
        One of ``'spd'``, ``'gamma'`` or ``'gamut'``.  ``'spd'`` plots the
        spectral power distribution of the primaries versus wavelength.
        ``'gamma'`` plots the gamma curves if available. ``'gamut'`` plots the
        chromaticity coordinates of the primaries.
    ax : matplotlib.axes.Axes, optional
        Axis to plot into. When ``None`` a new figure and axis are created.

    Returns
    -------
    matplotlib.axes.Axes
        Axis containing the plot.
    """
    if plt is None:
        raise ImportError("matplotlib is required for display_plot")

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    kind = kind.lower()
    if kind == "spd":
        wave = np.asarray(display.wave, dtype=float)
        spd = np.asarray(display.spd, dtype=float)
        if spd.shape[0] != wave.shape[0]:
            raise ValueError("display.spd and display.wave size mismatch")
        for i in range(min(spd.shape[1], 3)):
            ax.plot(wave, spd[:, i], color=_DEF_COLORS[i])
        ax.set_xlabel("Wavelength (nm)")
        ax.set_ylabel("Spectral power")
    elif kind == "gamma":
        if display.gamma is None:
            raise ValueError("display has no gamma table")
        gamma = np.asarray(display.gamma, dtype=float)
        x = np.linspace(0, 1, gamma.shape[0])
        for i in range(min(gamma.shape[1], 3)):
            ax.plot(x, gamma[:, i], color=_DEF_COLORS[i])
        ax.set_xlabel("Input level")
        ax.set_ylabel("Output level")
    elif kind == "gamut":
        wave = np.asarray(display.wave, dtype=float)
        spd = np.asarray(display.spd, dtype=float)
        xyz = ie_xyz_from_energy(spd.T, wave)
        xy = chromaticity(xyz)
        for i in range(min(xy.shape[0], 3)):
            ax.plot(xy[i, 0], xy[i, 1], "o", color=_DEF_COLORS[i])
        # draw triangle
        order = list(range(min(xy.shape[0], 3))) + [0]
        ax.plot(xy[order, 0], xy[order, 1], "k-")
        ax.set_xlabel("CIE x")
        ax.set_ylabel("CIE y")
        ax.set_xlim(0.0, 0.8)
        ax.set_ylim(0.0, 0.9)
    else:
        raise ValueError("Unknown kind '%s'" % kind)

    fig.tight_layout()
    return ax


__all__ = ["display_plot"]
