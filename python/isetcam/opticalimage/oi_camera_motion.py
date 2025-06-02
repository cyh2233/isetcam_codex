"""Apply camera motion blur to an :class:`OpticalImage`."""

from __future__ import annotations

from typing import Sequence, Mapping

import numpy as np

from .oi_class import OpticalImage
from .oi_translate import oi_translate


def oi_camera_motion(
    oi: OpticalImage,
    options: Mapping[str, object] | None = None,
) -> OpticalImage:
    """Blur ``oi`` using a motion path.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image to blur.
    options : mapping, optional
        Options controlling the motion blur. Recognized keys are:

        ``path`` : sequence of ``(dx, dy)``
            Pixel offsets describing the camera motion.  Positive ``dx`` moves
            the image to the right, positive ``dy`` moves it down.
        ``weights`` : sequence of float, optional
            Relative weight for each motion step.  Defaults to equal weights.
        ``fill`` : float, optional
            Value used to fill regions exposed by shifting.  Defaults to 0.

    Returns
    -------
    OpticalImage
        New optical image containing the blurred photon data.
    """

    if options is None:
        options = {}

    path = options.get("path")
    if path is None:
        raise ValueError("options must include a 'path' entry")

    path = np.asarray(list(path), dtype=float)
    if path.ndim != 2 or path.shape[1] != 2:
        raise ValueError("path must be an Nx2 sequence")

    weights = options.get("weights")
    if weights is None:
        weights = np.ones(path.shape[0], dtype=float)
    else:
        weights = np.asarray(weights, dtype=float)
        if weights.size != path.shape[0]:
            raise ValueError("weights length must match path length")

    fill = float(options.get("fill", 0))

    accum = np.zeros_like(oi.photons, dtype=float)

    for (dx, dy), w in zip(path, weights):
        shifted = oi_translate(oi, int(round(dx)), int(round(dy)), fill=fill)
        accum += w * shifted.photons

    total = float(np.sum(weights))
    if total > 0:
        accum /= total

    return OpticalImage(photons=accum, wave=oi.wave, name=oi.name)


__all__ = ["oi_camera_motion"]
