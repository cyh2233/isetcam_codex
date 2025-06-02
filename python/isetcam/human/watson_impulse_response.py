# mypy: ignore-errors
"""Watson temporal impulse response model."""

from __future__ import annotations

import math
import numpy as np


_DEF_T = np.arange(0.001, 1.001, 0.002)


def watson_impulse_response(
    t: np.ndarray | None = None, transient_factor: float = 0.5
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return impulse response and its temporal MTF."""
    if t is None:
        t = _DEF_T.copy()
    else:
        t = np.asarray(t, dtype=float)
    t = t[t > 0]

    tau = 0.00494
    kappa = 1.33
    n1 = 9
    n2 = 10

    h1 = (t / tau) ** (n1 - 1) * np.exp(-t / tau) / (t * math.factorial(n1 - 1))
    h2 = (t / (kappa * tau)) ** (n2 - 1) * np.exp(-t / (kappa * tau)) / (
        t * math.factorial(n2 - 1)
    )
    imp = h1 - transient_factor * h2
    imp = imp / imp.sum()

    t_mtf = np.abs(np.fft.fft(imp))
    freq = (1 / t.max()) * np.arange(1, t.size + 1)
    return imp, t, t_mtf, freq
