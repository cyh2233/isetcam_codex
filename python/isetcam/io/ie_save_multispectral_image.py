# mypy: ignore-errors
"""Save multispectral image data to MATLAB MAT-files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
from scipy.io import savemat


def ie_save_multispectral_image(
    path: str | Path,
    coefficients: np.ndarray,
    basis: np.ndarray,
    *,
    comment: str | None = None,
    img_mean: np.ndarray | None = None,
    illuminant: Any | None = None,
    fov: float | None = None,
    distance: float | None = None,
    name: str | None = None,
) -> None:
    """Save multispectral image data to ``path``.

    Parameters
    ----------
    path:
        Destination file.
    coefficients:
        Coefficient array describing each pixel.
    basis:
        Basis matrix with spectra in rows.
    comment:
        Optional text description.
    img_mean:
        Mean spectrum used when computing the coefficients.
    illuminant:
        Illuminant information.
    fov:
        Field of view in degrees.
    distance:
        Distance to the scene in meters.
    name:
        Optional scene name.
    """
    data: dict[str, Any] = {
        "coefficients": np.asarray(coefficients, dtype=float),
        "basis": np.asarray(basis, dtype=float),
    }
    if comment is not None:
        data["comment"] = str(comment)
    if img_mean is not None:
        data["img_mean"] = np.asarray(img_mean, dtype=float)
    if illuminant is not None:
        data["illuminant"] = illuminant
    if fov is not None:
        data["fov"] = float(fov)
    if distance is not None:
        data["distance"] = float(distance)
    if name is not None:
        data["name"] = str(name)

    savemat(str(Path(path)), data)
