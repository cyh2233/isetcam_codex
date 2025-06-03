# mypy: ignore-errors
"""Floyd-Steinberg style error diffusion halftoning."""

from __future__ import annotations

import numpy as np


def halftone_error_diffusion(FS: np.ndarray, image: np.ndarray) -> np.ndarray:
    """Apply error diffusion using diffusion matrix ``FS``.

    Parameters
    ----------
    FS : np.ndarray
        Diffusion matrix defining how the quantization error of each pixel is
        distributed to its neighbors. The matrix is normalized so that its sum
        equals ``1``. The current pixel corresponds to the center element of the
        first row.
    image : np.ndarray
        2-D grayscale image with values between ``0`` and ``1``.

    Returns
    -------
    np.ndarray
        Binary halftoned image of the same shape as ``image``.
    """
    fs = np.asarray(FS, dtype=float)
    fs /= fs.sum()

    img = np.asarray(image, dtype=float)
    img_r, img_c = img.shape
    fs_r, fs_c_total = fs.shape
    fs_c = fs_c_total // 2

    temp = np.zeros((img_r + fs_r, img_c + 2 * fs_c), dtype=float)
    temp[:img_r, fs_c : fs_c + img_c] = img

    for ir in range(img_r):
        for ic in range(fs_c, img_c):
            val = temp[ir, ic]
            temp[ir, ic] = np.round(val)
            err = val - temp[ir, ic]
            temp[ir : ir + fs_r, ic - fs_c : ic + fs_c + 1] += err * fs

        temp[ir : ir + fs_r, img_c : img_c + fs_c] += temp[ir + 1 : ir + fs_r + 1, :fs_c]

        for ic in range(img_c, img_c + fs_c):
            val = temp[ir, ic]
            temp[ir, ic] = np.round(val)
            err = val - temp[ir, ic]
            temp[ir : ir + fs_r, ic - fs_c : ic + fs_c + 1] += err * fs

        temp[ir + 1 : ir + fs_r + 1, fs_c : 2 * fs_c] += temp[ir : ir + fs_r, img_c + fs_c : img_c + 2 * fs_c]
        temp[:, :fs_c] = 0
        temp[:, img_c + fs_c :] = 0

    result = temp[:img_r, fs_c : fs_c + img_c]
    return result.astype(int)


__all__ = ["halftone_error_diffusion"]
