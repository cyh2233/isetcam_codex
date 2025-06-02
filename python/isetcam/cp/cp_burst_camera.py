from __future__ import annotations

from typing import List


def cp_burst_camera(
    n_frames: int,
    base_exposure: float,
    mode: str = "burst",
    *,
    ev_step: float = 1.0,
) -> List[float]:
    """Return exposure times for a burst or HDR capture.

    Parameters
    ----------
    n_frames:
        Number of frames in the burst.
    base_exposure:
        Reference exposure time for HDR sequences.
    mode:
        Either ``"burst"`` or ``"hdr"``.
    ev_step:
        Spacing in exposure value (EV) between successive frames when in
        ``"hdr"`` mode. ``ev_step=1`` corresponds to powers of two.
    """

    mode = mode.lower()
    if n_frames < 1:
        raise ValueError("n_frames must be positive")
    if mode == "hdr":
        offset = (n_frames - 1) / 2
        exp = [base_exposure * (2 ** ((i - offset) * ev_step)) for i in range(n_frames)]
    else:  # burst
        exp = [base_exposure / n_frames for _ in range(n_frames)]
    return exp
