# mypy: ignore-errors
from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from ..scene import Scene


@dataclass
class CPScene:
    """Container for a sequence of :class:`Scene` objects."""

    scenes: List[Scene]

    def preview(self) -> Scene:
        """Return the first scene in the sequence."""
        return self.scenes[0]

    def render(self, exp_times: List[float]) -> List[Scene]:
        """Return scenes corresponding to ``exp_times``.

        If only a single scene is stored, it is replicated to match the
        number of exposure times.
        """
        if len(self.scenes) == len(exp_times):
            return list(self.scenes)
        if len(self.scenes) == 1:
            return [self.scenes[0] for _ in exp_times]
        raise ValueError("Number of scenes does not match exposure times")
