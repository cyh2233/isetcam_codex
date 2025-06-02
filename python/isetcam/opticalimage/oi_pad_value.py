"""Pad an :class:`OpticalImage` with sample spacing adjustment."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .oi_class import OpticalImage


def oi_pad_value(
    oi: OpticalImage,
    pad_size: int | Sequence[int],
    value: float = 0,
) -> OpticalImage:
    """Pad ``oi`` on all sides and adjust ``sample_spacing``.

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
        Optical image padded with ``value``. The ``sample_spacing``
        attribute is updated so that the original field of view is
        preserved.
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

    out = OpticalImage(photons=padded, wave=oi.wave, name=oi.name)

    old_spacing = getattr(oi, "sample_spacing", 1.0)
    old_width_m = oi.photons.shape[1] * old_spacing
    new_width = oi.photons.shape[1] + left + right
    new_spacing = old_width_m / new_width

    out.sample_spacing = new_spacing
    return out


__all__ = ["oi_pad_value"]
