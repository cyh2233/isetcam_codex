"""Write a sequence of images to an animated GIF."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np
import imageio.v2 as imageio


def _frame_to_uint8(frame: np.ndarray) -> np.ndarray:
    arr = np.asarray(frame)
    if arr.dtype.kind == "f":
        arr = np.clip(arr, 0.0, 1.0)
        arr = (arr * 255).round().astype(np.uint8)
    else:
        arr = arr.astype(np.uint8)
    return arr


def animated_gif(
    image_sequence: Sequence[np.ndarray] | np.ndarray,
    path: str | Path,
    fps: int = 10,
    loop: int = 0,
) -> None:
    """Save ``image_sequence`` to ``path`` as a GIF.

    Parameters
    ----------
    image_sequence:
        List of ``(H, W, 3)`` arrays or array of shape ``(N, H, W, 3)``.
    path:
        Destination GIF file path.
    fps:
        Frames per second. Defaults to ``10``.
    loop:
        Number of animation loops. ``0`` for infinite. Defaults to ``0``.
    """
    if isinstance(image_sequence, np.ndarray):
        if image_sequence.ndim != 4 or image_sequence.shape[-1] != 3:
            raise ValueError("image_sequence must have shape (N, H, W, 3)")
        frames = [image_sequence[i] for i in range(image_sequence.shape[0])]
    else:
        frames = list(image_sequence)
    writer = imageio.get_writer(str(Path(path)), fps=int(fps), loop=int(loop))
    try:
        for frame in frames:
            writer.append_data(_frame_to_uint8(frame))
    finally:
        writer.close()
