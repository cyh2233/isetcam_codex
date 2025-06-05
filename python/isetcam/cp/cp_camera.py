# mypy: ignore-errors
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence, Optional

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
        focus_dists: Sequence[float] | float | None = None,
        render_flags: Sequence[bool] | bool | None = None,
    ) -> List:
        """Capture ``scene`` using ``exposure_times`` for each frame."""
        if isinstance(exposure_times, Sequence) and not isinstance(exposure_times, (str, bytes)):
            exp_list = list(exposure_times)
        else:
            exp_list = [float(exposure_times)]

        if focus_dists is not None:
            if isinstance(focus_dists, Sequence) and not isinstance(focus_dists, (str, bytes)):
                focus_list = list(focus_dists)
            else:
                focus_list = [float(focus_dists)]
        else:
            focus_list = None

        if render_flags is not None:
            if isinstance(render_flags, Sequence) and not isinstance(render_flags, (str, bytes)):
                render_list = list(render_flags)
            else:
                render_list = [bool(render_flags)]
        else:
            render_list = None

        scenes = scene.render(exp_list, focus_dists=focus_list, render_flags=render_list)
        all_images: List = []
        for module in self.modules:
            all_images.extend(module.compute(scenes, exp_list))
        return all_images
