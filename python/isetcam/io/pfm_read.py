"""Read images in Portable FloatMap (PFM) format."""

from __future__ import annotations

from pathlib import Path

import numpy as np


def pfm_read(path: str | Path) -> np.ndarray:
    """Load ``path`` and return a ``float32`` array.

    Parameters
    ----------
    path:
        Location of the PFM file to read.

    Returns
    -------
    numpy.ndarray
        ``(H, W)`` array for grayscale images or ``(H, W, 3)`` array for color
        images.  Values are returned as ``float32``.
    """

    p = Path(path)
    with p.open("rb") as f:
        header = f.readline().decode("ascii").rstrip()
        if header == "PF":
            n_chan = 3
        elif header == "Pf":
            n_chan = 1
        else:
            raise ValueError("Not a PFM file")

        dims = f.readline().decode("ascii").strip()
        while dims.startswith("#"):
            dims = f.readline().decode("ascii").strip()
        width, height = map(int, dims.split())

        scale = float(f.readline().decode("ascii").strip())
        endian = "<" if scale < 0 else ">"
        scale = abs(scale)

        data = np.fromfile(f, endian + "f", width * height * n_chan)
        data = data.reshape((height, width, n_chan))
        data = np.flipud(data) * scale

    if n_chan == 1:
        return data[:, :, 0]
    return data

