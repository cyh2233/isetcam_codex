# mypy: ignore-errors
"""Write images to Portable FloatMap (PFM) files."""

from __future__ import annotations

from pathlib import Path

import numpy as np


def pfm_write(path: str | Path, data: np.ndarray) -> None:
    """Save ``data`` to ``path`` in PFM format.

    Parameters
    ----------
    path:
        Destination file.
    data:
        ``(H, W)`` or ``(H, W, 3)`` array of ``float32`` values.
    """

    arr = np.asarray(data, dtype=np.float32)
    if arr.ndim == 2:
        header = "Pf"
    elif arr.ndim == 3 and arr.shape[2] == 3:
        header = "PF"
    else:
        raise ValueError("data must have shape (H, W) or (H, W, 3)")

    height, width = arr.shape[:2]

    p = Path(path)
    with p.open("wb") as f:
        f.write(f"{header}\n".encode("ascii"))
        f.write(f"{width} {height}\n".encode("ascii"))
        f.write(b"-1.0\n")  # little-endian with scale 1.0
        flipped = np.flipud(arr)
        flipped.tofile(f)

