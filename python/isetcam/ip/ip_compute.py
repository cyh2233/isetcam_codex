"""Render a sensor image to display RGB."""

from __future__ import annotations

import numpy as np

from ..sensor import Sensor
from ..display import Display, display_apply_gamma
from .vcimage_class import VCImage
from .ip_create import ip_create


def ip_compute(sensor: Sensor, display: Display) -> VCImage:
    """Return ``VCImage`` rendered from ``sensor`` for ``display``."""
    ip = ip_create(sensor, display)
    rgb = np.repeat(sensor.volts[:, :, None], 3, axis=2)
    if display.gamma is not None:
        rgb = display_apply_gamma(rgb, display, inverse=True)
    ip.rgb = rgb
    return ip
