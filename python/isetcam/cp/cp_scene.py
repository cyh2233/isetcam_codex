# mypy: ignore-errors
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Sequence

import shutil
from pathlib import Path


from ..scene import Scene, scene_from_pbrt
from ..iset_root_path import iset_root_path


@dataclass(init=False)
class CPScene:
    """Container for PBRT or ISETCam scenes."""

    scenes: List[Scene] = field(default_factory=list)
    scene_type: str = "pbrt"
    scene_path: Optional[str] = None
    lens_file: Optional[str] = None

    def __init__(
        self,
        scenes: Optional[Sequence[Scene]] = None,
        *,
        scene_type: str = "pbrt",
        scene_path: Optional[str] = None,
        lens_file: Optional[str] = None,
    ) -> None:
        self.scenes = list(scenes or [])
        self.scene_type = scene_type
        self.scene_path = scene_path
        self.lens_file = lens_file

    def preview(self) -> Scene:
        """Return the first scene in the sequence."""
        return self.scenes[0]

    def render(self, exp_times: Sequence[float]) -> List[Scene | object]:
        """Return scenes or optical images for ``exp_times``."""

        exp_list = list(exp_times)

        if self.scene_type == "pbrt" and self.scene_path is not None:
            path = Path(self.scene_path)
            computed_dir = iset_root_path() / "data" / "computed"
            computed_dir.mkdir(parents=True, exist_ok=True)
            outputs: List[Scene | object] = []
            for ii, t in enumerate(exp_list, start=1):
                sc, oi, _ = scene_from_pbrt(path)
                exr_path = path.with_suffix(".exr")
                if exr_path.exists():
                    dest = computed_dir / f"{exr_path.stem}-{ii:03d}-{int(round(t*1000))}{exr_path.suffix}"
                    shutil.move(exr_path, dest)
                outputs.append(oi if oi is not None else sc)
            return outputs

        if len(self.scenes) == len(exp_list):
            return list(self.scenes)
        if len(self.scenes) == 1:
            return [self.scenes[0] for _ in exp_list]
        raise ValueError("Number of scenes does not match exposure times")
