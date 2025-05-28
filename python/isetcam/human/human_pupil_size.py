"""Estimate human pupil diameter and area."""

from __future__ import annotations

import numpy as np


def human_pupil_size(lum: float | np.ndarray = 100, model: str = 'wy', **kwargs):
    """Return pupil diameter and area in mm and mm^2.

    Parameters
    ----------
    lum : float or array-like, optional
        Mean luminance in cd/m^2. Defaults to 100.
    model : {'ms', 'dg', 'sd', 'wy'}, optional
        Model used for the calculation. Defaults to ``'wy'`` (Watson and
        Yellott, 2012).
    **kwargs :
        Additional parameters required by some models:

        ``area`` : field area in deg^2 used by the ``'sd'`` and ``'wy'`` models.
        ``age`` : observer age in years for the ``'wy'`` model (default 28).
        ``eye_num`` : number of eyes (1 or 2) for the ``'wy'`` model
            (default 1).

    Returns
    -------
    diam : np.ndarray
        Pupil diameter in millimeters.
    area : np.ndarray
        Pupil area in square millimeters.
    """

    lum_arr = np.asarray(lum, dtype=float)
    flag = model.lower()

    if flag == 'ms':
        diam = 4.9 - 3 * np.tanh(0.4 * np.log10(lum_arr) + 1)
    elif flag == 'dg':
        diam = 10 ** (0.8558 - 0.000401 * (np.log10(lum_arr) + 8.6) ** 3)
    elif flag == 'sd':
        area = kwargs.get('area')
        if area is None:
            raise ValueError("'area' is required for sd model")
        F = lum_arr * float(area)
        diam = 7.75 - 5.75 * (F / 846) ** 0.41 / ((F / 846) ** 0.41 + 2)
    elif flag == 'wy':
        age = kwargs.get('age', 28)
        area = kwargs.get('area', 4)
        eye_num = kwargs.get('eye_num', 1)
        me = 0.1 if eye_num == 1 else 1.0
        F = lum_arr * float(area) * me
        Dsd, _ = human_pupil_size(F, 'sd', area=1)
        diam = Dsd + (float(age) - 28.58) * (0.02132 - 0.009562 * Dsd)
    else:
        raise ValueError(f"Unknown model '{model}'")

    area_out = np.pi * (diam / 2) ** 2
    return diam, area_out
