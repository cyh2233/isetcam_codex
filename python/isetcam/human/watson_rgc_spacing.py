# mypy: ignore-errors
"""Watson retinal ganglion cell spacing model."""

from __future__ import annotations

import math
import numpy as np


_PARAMS = np.array(
    [
        [0.9851, 1.058, 22.14],
        [0.9935, 1.035, 16.35],
        [0.9729, 1.084, 7.633],
        [0.9960, 0.9932, 12.13],
    ]
)
_DGF0 = 33163.2


def watson_rgc_spacing(
    fov_cols: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return midget RGC spacing across the field of view."""
    r = np.arange(0.05, 100.0 + 1e-9, 0.1)
    dgf = np.zeros((4, r.size))
    for k in range(4):
        a, r2, re = _PARAMS[k]
        dgf[k] = _DGF0 * (a * (1 + r / r2) ** -2 + (1 - a) * np.exp(-r / re))

    fr = (1 / 1.12) * (1 + r / 41.03) ** -1
    dmf1d = fr * dgf
    smf1d = np.sqrt(2.0 / (np.sqrt(3.0) * dmf1d))

    deg_start = -fov_cols / 2
    deg_end = fov_cols / 2
    degarr = np.linspace(deg_start, deg_end, fov_cols + 1)
    convert = math.sqrt(2.0)
    smf0 = np.zeros((degarr.size, degarr.size))
    for ix, x in enumerate(degarr):
        for iy, y in enumerate(degarr):
            rxy = math.hypot(x, y)
            if rxy == 0:
                smf0[ix, iy] = 0.0
                continue
            if x <= 0 and y >= 0:
                karr = (0, 1)
            elif x > 0 and y > 0:
                karr = (2, 1)
            elif x > 0 and y < 0:
                karr = (2, 3)
            else:
                karr = (0, 3)
            smf = []
            for kk in karr:
                a, r2, re = _PARAMS[kk]
                dgf_e = _DGF0 * (a * (1 + rxy / r2) ** -2 + (1 - a) * np.exp(-rxy / re))
                fr_e = (1 / 1.12) * (1 + rxy / 41.03) ** -1
                dmf_e = fr_e * dgf_e
                smf.append(math.sqrt(2.0 / (math.sqrt(3.0) * dmf_e)))
            smf0[ix, iy] = (
                convert
                * (1 / rxy)
                * math.sqrt(x * x * smf[0] ** 2 + y * y * smf[1] ** 2)
            )

    return smf0, r, smf1d
