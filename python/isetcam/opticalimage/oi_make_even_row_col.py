"""Ensure an :class:`OpticalImage` has even rows and columns."""

from __future__ import annotations
from .oi_class import OpticalImage
from .oi_pad import oi_pad


def oi_make_even_row_col(oi: OpticalImage, s_dist: float | None = None) -> OpticalImage:
    """Pad odd dimensions so that rows and columns are even.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image.
    s_dist : float, optional
        Scene distance in meters. Included for API compatibility but
        currently unused.

    Returns
    -------
    OpticalImage
        Optical image padded to have even row and column counts. The
        ``sample_spacing`` attribute is updated so that the field of view
        is preserved.
    """

    height, width = oi.photons.shape[:2]
    pad_bottom = height % 2
    pad_right = width % 2

    if pad_bottom == 0 and pad_right == 0:
        return oi

    padded = oi_pad(oi, (0, pad_bottom, 0, pad_right), value=0)

    old_spacing = getattr(oi, "sample_spacing", 1.0)
    old_width_m = width * old_spacing
    new_width = width + pad_right
    new_spacing = old_width_m / new_width

    padded.sample_spacing = new_spacing
    return padded
