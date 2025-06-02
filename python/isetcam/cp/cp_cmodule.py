# mypy: ignore-errors
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import List

import numpy as np

from ..sensor import Sensor, sensor_compute
from ..optics import Optics
from ..opticalimage import OpticalImage, oi_compute
from ..scene import Scene


@dataclass
class CPCModule:
    """Simple camera module holding :class:`Sensor` and :class:`Optics`."""

    sensor: Sensor
    optics: Optics

    def compute(self, scenes: List[Scene], exp_times: List[float]) -> List[Sensor]:
        """Return sensor captures for each scene and exposure time."""
        outputs: List[Sensor] = []
        for sc, t in zip(scenes, exp_times):
            oi = oi_compute(sc, self.optics)
            s = replace(self.sensor)
            s.exposure_time = float(t)
            s = sensor_compute(s, oi)
            outputs.append(s)
        return outputs
