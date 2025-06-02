# mypy: ignore-errors
"""Utility to remove optional attributes from an OpticalImage."""

from __future__ import annotations

from .oi_class import OpticalImage

# Attributes that may be attached to OpticalImage instances by various helpers
# or user interfaces. These are removed by :func:`oi_clear_data`.
_OPTIONAL_ATTRS = [
    "depth_map",
    "wangular",
    "crop_rect",
    "full_size",
    "sample_spacing",
    "pad_size",
    "psf",
    "otf",
    "optics_psf",
    "optics_otf",
]


def oi_clear_data(oi: OpticalImage) -> OpticalImage:
    """Remove cached or optional attributes from ``oi``.

    Parameters
    ----------
    oi : OpticalImage
        Optical image object to clean.

    Returns
    -------
    OpticalImage
        The same ``oi`` instance with extraneous attributes removed.
    """
    for attr in _OPTIONAL_ATTRS:
        if hasattr(oi, attr):
            delattr(oi, attr)
    return oi


__all__ = ["oi_clear_data"]
