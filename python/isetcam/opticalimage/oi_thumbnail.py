"""Create a thumbnail RGB image for an :class:`OpticalImage`."""

from __future__ import annotations

import numpy as np
from skimage.transform import resize

from .oi_class import OpticalImage
from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb


def oi_thumbnail(oi: OpticalImage, size: tuple[int, int] = (128, 128)) -> np.ndarray:
    """Return a downscaled sRGB rendering of ``oi``."""
    xyz = ie_xyz_from_photons(oi.photons, oi.wave)
    srgb, _, _ = xyz_to_srgb(xyz)
    img = np.clip(srgb, 0.0, 1.0)
    rows, cols = int(size[0]), int(size[1])
    thumb = resize(img, (rows, cols, 3), order=1, mode="reflect", anti_aliasing=True, preserve_range=True)
    return thumb.astype(float)
