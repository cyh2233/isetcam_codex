# mypy: ignore-errors
"""Utility to remove optional attributes from a VCImage."""

from __future__ import annotations

from .vcimage_class import VCImage

# Attributes that may be attached to VCImage instances by helpers or
# user interfaces. These are removed by :func:`ip_clear_data`.
_OPTIONAL_ATTRS = [
    "processed_rgb",
]


def ip_clear_data(ip: VCImage) -> VCImage:
    """Remove cached or optional attributes from ``ip``.

    Parameters
    ----------
    ip : VCImage
        Image processing object to clean.

    Returns
    -------
    VCImage
        The same ``ip`` instance with extraneous attributes removed.
    """
    for attr in _OPTIONAL_ATTRS:
        if hasattr(ip, attr):
            delattr(ip, attr)
    # Remove any arbitrary attributes not part of VCImage dataclass
    for key in list(vars(ip).keys()):
        if key not in {"rgb", "wave", "name"}:
            delattr(ip, key)
    return ip


__all__ = ["ip_clear_data"]
