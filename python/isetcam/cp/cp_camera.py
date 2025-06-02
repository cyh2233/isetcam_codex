# mypy: ignore-errors
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence

from .cp_scene import CPScene
from .cp_cmodule import CPCModule


@dataclass
class CPCamera:
    """Simplified computational camera composed of one or more modules."""

    modules: List[CPCModule] = field(default_factory=list)

    def take_picture(
        self,
        scene: CPScene,
        *,
        exposure_times: Sequence[float] | float = 1.0,
    ) -> List:
        """Capture ``scene`` using ``exposure_times`` for each frame."""
        if isinstance(exposure_times, Sequence) and not isinstance(exposure_times, (str, bytes)):
            exp_list = list(exposure_times)
        else:
            exp_list = [float(exposure_times)]
        scenes = scene.render(exp_list)
        all_images: List = []
        for module in self.modules:
            all_images.extend(module.compute(scenes, exp_list))
        return all_images
