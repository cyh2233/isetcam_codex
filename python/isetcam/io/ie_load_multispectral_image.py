# mypy: ignore-errors
"""Load multispectral image data saved by :func:`ie_save_multispectral_image`."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import numpy as np
from scipy.io import loadmat


def ie_load_multispectral_image(path: str | Path) -> Dict[str, Any]:
    """Load ``path`` and return a dictionary of multispectral image data."""
    mat = loadmat(str(Path(path)), squeeze_me=True, struct_as_record=False)
    data: Dict[str, Any] = {}
    if "coefficients" in mat:
        data["coefficients"] = np.asarray(mat["coefficients"])
    if "basis" in mat:
        data["basis"] = np.asarray(mat["basis"])
    if "comment" in mat:
        value = mat["comment"]
        if isinstance(value, np.ndarray):
            value = str(value.squeeze())
        data["comment"] = value
    if "img_mean" in mat:
        data["img_mean"] = np.asarray(mat["img_mean"])
    if "illuminant" in mat:
        data["illuminant"] = mat["illuminant"]
    if "fov" in mat:
        data["fov"] = float(mat["fov"])
    if "distance" in mat:
        data["distance"] = float(mat["distance"])
    if "name" in mat:
        value = mat["name"]
        if isinstance(value, np.ndarray):
            value = str(value.squeeze())
        data["name"] = value
    return data
