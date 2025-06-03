# mypy: ignore-errors
"""Basic :class:`VCImage` dataclass."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class VCImage:
    """Minimal view controller image container."""

    rgb: np.ndarray
    wave: np.ndarray
    name: str | None = None
    internal_cs: str | None = None
    conversion_method_sensor: str | None = None
    illuminant_correction_method: str | None = None
