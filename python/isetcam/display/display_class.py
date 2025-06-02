# mypy: ignore-errors
"""Basic :class:`Display` dataclass."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..ie_xyz_from_energy import ie_xyz_from_energy


@dataclass
class Display:
    """Minimal representation of an ISETCam display."""

    spd: np.ndarray
    wave: np.ndarray
    gamma: np.ndarray | None = None
    name: str | None = None
    max_luminance: float | None = None
    white_point: np.ndarray | None = None

    def __post_init__(self) -> None:
        if self.white_point is None:
            try:
                self.white_point = ie_xyz_from_energy(self.spd.sum(axis=1), self.wave).reshape(3)
            except Exception:
                self.white_point = np.zeros(3)
        if self.max_luminance is None:
            self.max_luminance = float(self.white_point[1])
