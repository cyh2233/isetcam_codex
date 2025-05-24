"""Apply simple distortions to an image."""

from __future__ import annotations

import numpy as np
from io import BytesIO
from typing import Any

from PIL import Image

from ..ie_param_format import ie_param_format


def image_distort(img: np.ndarray, d_method: str, *args: Any) -> np.ndarray:
    """Distort image data using the specified method.

    Parameters
    ----------
    img : np.ndarray
        Image data array. Can be ``uint8`` or floating point.
    d_method : str
        Distortion method. Supported values are ``'gaussian noise'``,
        ``'jpeg compress'`` and ``'scale contrast'``.
    *args : Any
        Optional parameters for the distortion method.

    Returns
    -------
    np.ndarray
        Distorted image in the same dtype as ``img``.
    """

    if img.size == 0:
        return img

    method = ie_param_format(d_method)

    if method == "gaussiannoise":
        if len(args) > 0:
            n_scale = float(args[0])
        else:
            n_scale = 0.05 * float(img.max())
        noise = n_scale * np.random.randn(*img.shape)

        if np.issubdtype(img.dtype, np.integer) and img.max() < 256:
            img_f = img.astype(float) + noise
            img_f = np.clip(img_f, 0, 255)
            return img_f.astype(np.uint8)
        else:
            return img.astype(float) + noise

    if method == "jpegcompress":
        if len(args) > 0:
            quality = int(args[0])
        else:
            quality = 75
        pil_img = Image.fromarray(img)
        with BytesIO() as buf:
            pil_img.save(buf, format="JPEG", quality=quality)
            buf.seek(0)
            out = np.array(Image.open(buf))
        return out.astype(img.dtype)

    if method == "scalecontrast":
        if len(args) > 0:
            scale = float(args[0])
        else:
            scale = 0.1
        return img * (1 + scale)

    raise ValueError(f"Unknown method: {d_method}")
