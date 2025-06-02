# mypy: ignore-errors
"""Pad an :class:`OpticalImage`'s photon data."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .oi_class import OpticalImage


def oi_pad(oi: OpticalImage, pad_size: int | Sequence[int], value: float = 0) -> OpticalImage:  # noqa: E501
    """Pad ``oi`` by ``pad_size`` pixels on all sides.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image to pad.
    pad_size : int or sequence of int
        Amount of padding. If an integer, the same value is used on all
        sides. If a sequence of two integers, the first specifies padding
        for the top and bottom, and the second for the left and right.
        A sequence of four integers specifies ``(top, bottom, left, right)``.
    value : float, optional
        Value used to fill the padded region. Defaults to 0.

    Returns
    -------
    OpticalImage
        New optical image containing the padded photon data with the same
        wavelength samples.
    """

    if isinstance(pad_size, Sequence) and not isinstance(pad_size, (int, float)):
        pad = list(pad_size)
        if len(pad) == 2:
            top = bottom = int(pad[0])
            left = right = int(pad[1])
        elif len(pad) == 4:
            top, bottom, left, right = [int(v) for v in pad]
        else:
            raise ValueError("pad_size must be a scalar or have length 2 or 4")
    else:
        top = bottom = left = right = int(pad_size)

    pad_width = ((top, bottom), (left, right), (0, 0))
    padded = np.pad(oi.photons, pad_width, mode="constant", constant_values=value)
    return OpticalImage(photons=padded, wave=oi.wave, name=oi.name)
