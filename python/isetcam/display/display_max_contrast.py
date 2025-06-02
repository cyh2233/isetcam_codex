# mypy: ignore-errors
"""Compute the Michelson contrast between two signals."""

from __future__ import annotations

import numpy as np



def display_max_contrast(signal_dir: np.ndarray, back_dir: np.ndarray) -> float:
    """Return the maximum Michelson contrast of ``signal_dir`` vs ``back_dir``.

    ``signal_dir`` and ``back_dir`` should be arrays of the same shape.
    The function computes ``(max(signal) - min(background)) / (max(signal) + min(background))``.  # noqa: E501
    When either input contains only zeros the contrast is zero.
    """
    sig = np.asarray(signal_dir, dtype=float)
    back = np.asarray(back_dir, dtype=float)
    if sig.shape != back.shape:
        raise ValueError("signal_dir and back_dir must have the same shape")
    s_max = sig.max()
    b_min = back.min()
    denom = s_max + b_min
    if denom == 0:
        return 0.0
    return float((s_max - b_min) / denom)


__all__ = ["display_max_contrast"]
