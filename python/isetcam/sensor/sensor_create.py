# mypy: ignore-errors
"""Factory function for :class:`Sensor` objects."""

from __future__ import annotations

from typing import Optional, Tuple

import re

import numpy as np

from .sensor_class import Sensor

# Mapping from Bayer pattern name to (filter_color_letters, n_colors)
BAYER_PATTERN_MAP = {
    "grbg": ("grbg", 3),
    "rggb": ("rggb", 3),
    "bggr": ("bggr", 3),
    "gbrg": ("gbrg", 3),
}


def parse_bayer_pattern(kind: str) -> Tuple[str, int]:
    """Return CFA letters and number of colors for ``kind``.

    Parameters
    ----------
    kind:
        String describing the sensor type, e.g. ``"bayer"`` or
        ``"bayer (rggb)"``.
    """

    flag = kind.lower().replace(" ", "")
    m = re.match(r"bayer(?:[-(]?([a-z]+)[)]?)?$", flag)
    if not m:
        raise ValueError(f"Unknown sensor type '{kind}'")
    pattern = m.group(1) or "grbg"
    if pattern not in BAYER_PATTERN_MAP:
        raise ValueError(f"Unknown Bayer pattern '{pattern}'")
    return BAYER_PATTERN_MAP[pattern]

_DEF_PIXEL_SIZE = 2.8e-6  # meters
_DEF_EXPOSURE = 0.01  # seconds


def sensor_create(kind: str = "bayer", wave: Optional[np.ndarray] = None) -> Sensor:
    """Create a simple :class:`Sensor` by ``kind``.

    Parameters
    ----------
    kind:
        Type of sensor to create. ``"bayer"`` optionally followed by a
        CFA pattern (e.g. ``"bayer (rggb)"``) is supported.
    wave:
        Optional wavelength sampling for the sensor's spectral properties.
    """
    letters, n_colors = parse_bayer_pattern(kind)

    volts = np.zeros((1, 1), dtype=float)
    s = Sensor(volts=volts, exposure_time=_DEF_EXPOSURE, wave=wave, name=kind)

    # Default quantum efficiency and pixel size information
    s.qe = np.ones(s.wave.size, dtype=float)
    s.pixel_size = float(_DEF_PIXEL_SIZE)
    s.filter_color_letters = letters
    s.n_colors = n_colors
    return s
