"""Write images to OpenEXR files."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

import numpy as np

try:  # pragma: no cover - optional dependency
    import OpenEXR  # type: ignore
    import Imath  # type: ignore
except Exception:  # pragma: no cover - library may not be present
    OpenEXR = None  # type: ignore
    Imath = None  # type: ignore

import imageio.v2 as iio


def _write_with_openexr(path: Path, channels: Mapping[str, np.ndarray]) -> None:
    assert OpenEXR is not None and Imath is not None
    keys = list(channels.keys())
    arrays = [np.asarray(channels[k], dtype=np.float32) for k in keys]
    height, width = arrays[0].shape
    for arr in arrays:
        if arr.shape != (height, width):
            raise ValueError("All channels must have the same shape")
    header = OpenEXR.Header(width, height)
    for name in keys:
        header["channels"][name] = Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT))
    exr = OpenEXR.OutputFile(str(path), header)
    exr.writePixels({name: arr.tobytes() for name, arr in zip(keys, arrays)})
    exr.close()


def _write_with_imageio(path: Path, channels: Mapping[str, np.ndarray]) -> None:
    keys = list(channels.keys())
    arrays = [np.asarray(channels[k], dtype=np.float32) for k in keys]
    height, width = arrays[0].shape
    for arr in arrays:
        if arr.shape != (height, width):
            raise ValueError("All channels must have the same shape")
    if len(arrays) > 4:
        raise ValueError("imageio backend supports at most 4 channels")
    data = np.stack(arrays, axis=-1)
    iio.imwrite(str(path), data, format="EXR-FI")


def openexr_write(path: str | Path, channels: Mapping[str, np.ndarray]) -> None:
    """Save ``channels`` to ``path`` as an OpenEXR file."""
    p = Path(path)
    if OpenEXR is not None:
        _write_with_openexr(p, channels)
    else:
        _write_with_imageio(p, channels)
