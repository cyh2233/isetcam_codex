# mypy: ignore-errors
"""Export a list of scenes as a video."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np
import imageio.v2 as imageio

from .scene_class import Scene
from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb


def scene_make_video(
    scene_list: Sequence[Scene],
    output_path: str | Path,
    fps: int = 30,
) -> None:
    """Encode ``scene_list`` into a video at ``output_path``.

    Parameters
    ----------
    scene_list : Sequence[Scene]
        Scenes to render as video frames.
    output_path : str or Path
        Destination file path for the video.
    fps : int, optional
        Frames per second of the encoded video. Defaults to ``30``.
    """
    writer = imageio.get_writer(str(Path(output_path)), fps=int(fps))
    try:
        for sc in scene_list:
            xyz = ie_xyz_from_photons(sc.photons, sc.wave)
            srgb, _, _ = xyz_to_srgb(xyz)
            img = np.clip(srgb, 0.0, 1.0)
            arr = (img * 255).round().astype(np.uint8)
            writer.append_data(arr)
    finally:
        writer.close()
