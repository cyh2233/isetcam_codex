"""Write DNG images using rawpy."""

from __future__ import annotations

from pathlib import Path

import numpy as np

try:  # pragma: no cover - optional dependency
    import rawpy  # type: ignore
except Exception:  # pragma: no cover - library may not be present
    rawpy = None  # type: ignore


def dng_write(path: str | Path, data: np.ndarray) -> None:
    """Save ``data`` to ``path`` as a DNG file."""
    if rawpy is None:  # pragma: no cover - dependency missing
        raise RuntimeError("rawpy library is not available")
    arr = np.asarray(data, dtype=np.uint16)
    rawpy.enhance.write_dng(str(path), arr)
