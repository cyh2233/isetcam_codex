# mypy: ignore-errors
"""Create an HDR scene of bright patches on a background image."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
from skimage.transform import resize

from .scene_class import Scene
from .scene_adjust_luminance import scene_adjust_luminance
from .scene_from_file import scene_from_file


_DEF_WAVE = np.arange(400, 701, 10, dtype=float)


def _background(image: str | None, size: int, wave: np.ndarray) -> Scene:
    if not image:
        photons = np.zeros((size, size, wave.size), dtype=float)
        return Scene(photons=photons, wave=wave, name="Background")

    img = scene_from_file(Path(image), wave=wave)
    if img.photons.shape[0] != size or img.photons.shape[1] != size:
        data = resize(
            img.photons,
            (size, size, wave.size),
            order=1,
            mode="reflect",
            anti_aliasing=True,
            preserve_range=True,
        )
        img = Scene(photons=data.astype(float), wave=wave, name=img.name)
    img = scene_adjust_luminance(img, "mean", 1.0)
    return img


def scene_hdr_image(
    n_patches: int,
    *,
    background: str | None = None,
    image_size: int = 512,
    dynamic_range: float = 3.0,
    patch_shape: str = "square",
    patch_size: Optional[int] = None,
    row: Optional[int] = None,
    wave: np.ndarray | None = None,
) -> Scene:
    """Return a scene with bright patches spanning ``dynamic_range`` log units."""

    if wave is None:
        wave = _DEF_WAVE
    else:
        wave = np.asarray(wave, dtype=float).reshape(-1)

    bg = _background(background, image_size, wave)
    photons = bg.photons.copy()
    rows, cols = photons.shape[:2]

    if patch_shape not in {"square", "circle"}:
        raise ValueError("patch_shape must be 'square' or 'circle'")

    levels = np.logspace(0, dynamic_range, n_patches)[::-1]

    if patch_shape == "square":
        if patch_size is None:
            patch_w = cols // (2 * n_patches)
        else:
            patch_w = int(patch_size)
        patch_h = patch_w
        spacing = cols / (n_patches + 1)
        centers = np.round(np.arange(1, n_patches + 1) * spacing).astype(int)
        r0 = int(row) if row is not None else (rows - patch_h) // 2
        for i, c in enumerate(centers):
            c0 = int(c) - patch_w // 2
            r_slice = slice(r0, r0 + patch_h)
            c_slice = slice(c0, c0 + patch_w)
            patch = np.full((patch_h, patch_w, wave.size), levels[i], dtype=float)
            photons[r_slice, c_slice, :] = photons[r_slice, c_slice, :] + patch
    else:  # circle
        if patch_size is None:
            radius = cols // (4 * n_patches)
        else:
            radius = int(patch_size)
        spacing = cols / (n_patches + 1)
        centers = np.round(np.arange(1, n_patches + 1) * spacing).astype(int)
        r_center = int(row) if row is not None else rows // 2
        yy, xx = np.ogrid[:rows, :cols]
        for i, c in enumerate(centers):
            mask = (xx - c) ** 2 + (yy - r_center) ** 2 <= radius ** 2
            photons[mask, :] = photons[mask, :] + levels[i]

    out = Scene(photons=photons, wave=wave, name="HDR image")
    return out
