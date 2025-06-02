"""Encode optical images as a preview video."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np
import imageio.v2 as imageio

from .oi_class import OpticalImage
from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb


def oi_preview_video(
    ois: Sequence[OpticalImage],
    output_path: str | Path,
    fps: int = 30,
) -> None:
    """Write ``ois`` to ``output_path`` as a video or GIF.

    Parameters
    ----------
    ois:
        Sequence of optical images to render.
    output_path:
        Destination video file path (e.g. ``.mp4`` or ``.gif``).
    fps:
        Frames per second of the output. Defaults to ``30``.
    """
    writer = imageio.get_writer(str(Path(output_path)), fps=int(fps))
    try:
        for oi in ois:
            xyz = ie_xyz_from_photons(oi.photons, oi.wave)
            srgb, _, _ = xyz_to_srgb(xyz)
            arr = np.clip(srgb, 0.0, 1.0)
            writer.append_data((arr * 255).round().astype(np.uint8))
    finally:
        writer.close()
