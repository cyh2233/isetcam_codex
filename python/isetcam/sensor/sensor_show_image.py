# mypy: ignore-errors
"""Display a Sensor image using Matplotlib."""

from __future__ import annotations

import numpy as np

try:  # pragma: no cover - matplotlib might not be installed
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore

from .sensor_class import Sensor
from ..display import (
    Display,
    display_create,
    display_render,
    display_apply_gamma,
)
from ..ip import ip_demosaic
from ..srgb_to_lrgb import srgb_to_lrgb
from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb
from ..ie_format_figure import ie_format_figure


def sensor_show_image(sensor: Sensor, display: Display | None = None):
    """Render ``sensor.volts`` to sRGB and show with matplotlib.

    Parameters
    ----------
    sensor : Sensor
        Sensor containing voltage data in sRGB format.
    display : Display, optional
        Display model used to convert the linear RGB image to spectral
        radiance. When ``None`` a default display is created.

    Returns
    -------
    matplotlib.axes.Axes
        Axis containing the displayed image.
    """
    if plt is None:
        raise ImportError("matplotlib is required for sensor_show_image")
    if display is None:
        display = display_create()

    volts = np.asarray(sensor.volts, dtype=float)

    if volts.ndim == 2:
        pattern = getattr(sensor, "filter_color_letters", None)
        if pattern is not None:
            pattern_str = "".join(np.ravel(pattern).tolist()) if not isinstance(pattern, str) else str(pattern)
            vols_rgb = ip_demosaic(volts, pattern_str, method="bilinear")
        else:
            vols_rgb = np.repeat(volts[:, :, None], 3, axis=2)
        if display.gamma is not None:
            volts = display_apply_gamma(vols_rgb, display, inverse=True)
        else:
            volts = vols_rgb
    elif volts.ndim == 3 and volts.shape[2] == 3:
        pass
    else:
        raise ValueError("sensor.volts must be (rows, cols) or (rows, cols, 3)")

    lrgb = srgb_to_lrgb(volts)
    spectral = display_render(lrgb, display, apply_gamma=False)
    if spectral.shape[-1] != len(display.wave):
        raise ValueError(
            "display.spd must be resampled to display.wave; expected"
            f" {len(display.wave)}, got {spectral.shape[-1]}"
        )
    xyz = ie_xyz_from_photons(spectral, display.wave)
    srgb, _, _ = xyz_to_srgb(xyz)

    fig, ax = plt.subplots()
    ax.imshow(np.clip(srgb, 0.0, 1.0))
    ax.axis("off")
    ie_format_figure(ax)
    return ax
