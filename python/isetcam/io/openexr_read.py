# mypy: ignore-errors
"""Read OpenEXR images with optional OpenEXR bindings."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np

try:  # pragma: no cover - optional dependency
    import OpenEXR  # type: ignore
    import Imath  # type: ignore
except Exception:  # pragma: no cover - library may not be present
    OpenEXR = None  # type: ignore
    Imath = None  # type: ignore

import imageio.v2 as iio


def _read_with_openexr(path: Path) -> Dict[str, np.ndarray]:
    """Read using the OpenEXR Python bindings."""
    assert OpenEXR is not None and Imath is not None
    exr = OpenEXR.InputFile(str(path))
    header = exr.header()
    dw = header["dataWindow"]
    width = dw.max.x - dw.min.x + 1
    height = dw.max.y - dw.min.y + 1
    channels: Dict[str, np.ndarray] = {}
    for name in header["channels"].keys():
        pt = Imath.PixelType(Imath.PixelType.FLOAT)
        raw = exr.channel(name, pt)
        arr = np.frombuffer(raw, dtype=np.float32)
        channels[name] = arr.reshape(height, width)
    exr.close()
    return channels


def _read_with_imageio(path: Path) -> Dict[str, np.ndarray]:
    """Read using the imageio FreeImage backend."""
    arr = np.asarray(iio.imread(str(path)), dtype=np.float32)
    if arr.ndim == 2:
        arr = arr[:, :, None]
    n_chan = arr.shape[2]
    if n_chan == 1:
        names = ["Y"]
    elif n_chan == 3:
        names = ["R", "G", "B"]
    elif n_chan == 4:
        names = ["R", "G", "B", "A"]
    else:
        names = [f"channel{i}" for i in range(n_chan)]
    return {name: arr[:, :, i] for i, name in enumerate(names)}


def openexr_read(path: str | Path) -> Dict[str, np.ndarray]:
    """Load an OpenEXR image from ``path``.

    Parameters
    ----------
    path:
        File to read.

    Returns
    -------
    dict
        Mapping of channel names to 2-D ``float32`` arrays.
    """
    p = Path(path)
    if OpenEXR is not None:
        return _read_with_openexr(p)
    return _read_with_imageio(p)
