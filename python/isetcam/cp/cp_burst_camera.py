from __future__ import annotations

from typing import List


def cp_burst_camera(n_frames: int, base_exposure: float, mode: str = "burst") -> List[float]:
    """Return exposure times for a burst or HDR capture."""
    mode = mode.lower()
    if n_frames < 1:
        raise ValueError("n_frames must be positive")
    if mode == "hdr":
        if n_frames > 1 and n_frames % 2 == 0:
            n_frames += 1
        offset = (n_frames - 1) / 2
        exp = [base_exposure * (2 ** (i - offset)) for i in range(n_frames)]
    else:  # burst
        exp = [base_exposure / n_frames for _ in range(n_frames)]
    return exp
