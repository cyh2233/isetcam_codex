"""Basic :class:`Pixel` dataclass."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Pixel:
    """Minimal representation of an ISETCam pixel."""

    width: float
    height: float
    well_capacity: float
    fill_factor: float
