"""Plot sensor voltage image with optional color filter overlay."""

from __future__ import annotations

import numpy as np

try:
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgb
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore
    to_rgb = None  # type: ignore

from .sensor_class import Sensor


_COLOR_MAP = {
    "r": (1.0, 0.0, 0.0),
    "g": (0.0, 1.0, 0.0),
    "b": (0.0, 0.0, 1.0),
    "c": (0.0, 1.0, 1.0),
    "m": (1.0, 0.0, 1.0),
    "y": (1.0, 1.0, 0.0),
    "k": (0.0, 0.0, 0.0),
    "w": (1.0, 1.0, 1.0),
}


def _parse_pattern(letters: np.ndarray | str) -> np.ndarray | None:
    """Return 2-D array of letters from ``letters`` if possible."""
    if isinstance(letters, str):
        size = int(np.sqrt(len(letters)))
        if size * size == len(letters):
            return np.array(list(letters)).reshape(size, size)
        return None
    letters = np.asarray(letters)
    if letters.ndim == 2:
        return letters
    if letters.ndim == 1:
        size = int(np.sqrt(letters.size))
        if size * size == letters.size:
            return letters.reshape(size, size)
    return None


def sensor_plot(sensor: Sensor, *, show_filters: bool = False, ax: "plt.Axes | None" = None) -> "plt.Axes":  # noqa: E501
    """Plot ``sensor.volts`` and return the matplotlib axis."""
    if plt is None:
        raise ImportError("matplotlib is required for sensor_plot")

    volts = np.asarray(sensor.volts, dtype=float)
    if volts.ndim != 2:
        raise ValueError("sensor.volts must be a 2-D array")

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure
    ax.imshow(volts, cmap="gray", origin="upper")
    ax.axis("off")

    if show_filters:
        letters = getattr(sensor, "filter_color_letters", None)
        pattern = None
        if letters is not None:
            pattern = _parse_pattern(letters)
        if pattern is not None:
            rows, cols = volts.shape
            pr, pc = pattern.shape
            rr = rows // pr + 1
            cc = cols // pc + 1
            pattern = np.tile(pattern, (rr, cc))[:rows, :cols]
            overlay = np.zeros((rows, cols, 4), dtype=float)
            for ltr, color in _COLOR_MAP.items():
                mask = pattern == ltr
                overlay[mask, :3] = color
                overlay[mask, 3] = 0.4
            ax.imshow(overlay, interpolation="none")

    fig.tight_layout()
    return ax


__all__ = ["sensor_plot"]
