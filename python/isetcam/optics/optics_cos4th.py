from __future__ import annotations

import numpy as np


def optics_cos4th(
    x: np.ndarray,
    y: np.ndarray,
    image_distance: float,
    image_diagonal: float,
    f_number: float,
    magnification: float = 1.0,
) -> np.ndarray:
    """Calculate cos4th off-axis falloff.

    Parameters
    ----------
    x, y : array-like
        Spatial support coordinates in meters.
    image_distance : float
        Distance from lens to image plane in meters.
    image_diagonal : float
        Diagonal size of the image in meters.
    f_number : float
        Lens f-number.
    magnification : float, optional
        Magnification factor used for the near-field case. Defaults to 1.0.

    Returns
    -------
    np.ndarray
        Relative illumination falloff for each ``(x, y)`` position.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    s_factor = np.sqrt(image_distance ** 2 + (x ** 2 + y ** 2))
    if image_distance > 10 * image_diagonal:
        spatial_fall = (image_distance / s_factor) ** 4
    else:
        cos_phi = image_distance / s_factor
        sin_phi = np.sqrt(1.0 - cos_phi ** 2)
        tan_phi = sin_phi / cos_phi
        sin_theta = 1.0 / (1.0 + 4.0 * (f_number * (1.0 - magnification)) ** 2)
        cos_theta = np.sqrt(1.0 - sin_theta ** 2)
        tan_theta = sin_theta / cos_theta
        spatial_fall = (
            (np.pi / 2.0)
            * (
                1.0
                - (1.0 - tan_theta ** 2 + tan_phi ** 2)
                / np.sqrt(
                    tan_phi ** 4
                    + 2 * tan_phi ** 2 * (1.0 - tan_theta ** 2)
                    + 1.0 / cos_theta ** 4
                )
            )
        )
        spatial_fall /= np.pi * sin_theta ** 2
    return spatial_fall
