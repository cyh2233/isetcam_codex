"""Read DNG images using rawpy."""

from __future__ import annotations

from pathlib import Path

import numpy as np

try:  # pragma: no cover - optional dependency
    import rawpy  # type: ignore
except Exception:  # pragma: no cover - library may not be present
    rawpy = None  # type: ignore


def dng_read(path: str | Path) -> np.ndarray:
    """Load ``path`` and return the raw pixel data.

    Parameters
    ----------
    path:
        File to read.

    Returns
    -------
    numpy.ndarray
        ``(H, W)`` array of ``uint16`` values containing the raw sensor data.
    """
    if rawpy is None:  # pragma: no cover - dependency missing
        raise RuntimeError("rawpy library is not available")
    p = Path(path)
    with rawpy.imread(str(p)) as raw:
        data = np.asarray(raw.raw_image, dtype=np.uint16)
    return data
