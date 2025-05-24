"""Basic :class:`Camera` dataclass."""

from __future__ import annotations

from dataclasses import dataclass

from ..sensor import Sensor
from ..opticalimage import OpticalImage


@dataclass
class Camera:
    """Minimal representation of an ISETCam camera."""

    sensor: Sensor
    optical_image: OpticalImage
    name: str | None = None
