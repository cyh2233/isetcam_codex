# mypy: ignore-errors
"""Gateway for human spatio-temporal sensitivity models."""

from __future__ import annotations

import numpy as np

from .kelly_space_time import kelly_space_time, _DEF_FS, _DEF_FT
from .watson_impulse_response import watson_impulse_response
from .poirson_spatio_chromatic import poirson_spatio_chromatic


def human_space_time(
    model: str = "kelly79",
    fs: np.ndarray | None = None,
    ft: np.ndarray | None = None,
):
    """Return spatio-temporal sensitivity for the specified ``model``."""
    if fs is None:
        fs = _DEF_FS.copy()
    else:
        fs = np.asarray(fs, dtype=float)
    if ft is None:
        ft = _DEF_FT.copy()
    else:
        ft = np.asarray(ft, dtype=float)

    flag = model.lower()
    if flag in {"kelly79", "kellyspacetime", "kellyspacetimefrequencydomain"}:
        sens, fs, ft = kelly_space_time(fs, ft)
    elif flag == "watsonimpulseresponse":
        sens, _, _, _ = watson_impulse_response(ft)
        fs = None
    elif flag == "watsontmtf":
        lowest_f = float(ft.min())
        period = 1.0 if lowest_f == 0 else 1.0 / lowest_f
        t = np.arange(0.001, period + 0.001, 0.001)
        _, _, t_mtf, all_ft = watson_impulse_response(t)
        sens = np.interp(ft, all_ft, t_mtf)
        fs = None
    elif flag in {"poirsoncolor", "wandellpoirsoncolorspace"}:
        lum, rg, by, positions = poirson_spatio_chromatic()
        sens = {"lum": lum, "rg": rg, "by": by}
        fs = positions
    else:
        raise ValueError("Unknown model")

    return sens, fs, ft
