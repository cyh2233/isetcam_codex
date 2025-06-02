# mypy: ignore-errors
"""Utility to remove optional attributes from an Optics."""

from __future__ import annotations

from .optics_class import Optics

# Attributes that may be attached to Optics instances by various helpers
# or user interfaces. These are removed by :func:`optics_clear_data`.
_OPTIONAL_ATTRS = [
    "otf_data",
    "cos4th_data",
]


def optics_clear_data(optics: Optics) -> Optics:
    """Remove cached or optional attributes from ``optics``.

    Parameters
    ----------
    optics : Optics
        Optics object to clean.

    Returns
    -------
    Optics
        The same ``optics`` instance with extraneous attributes removed.
    """
    for attr in _OPTIONAL_ATTRS:
        if hasattr(optics, attr):
            delattr(optics, attr)
    return optics


__all__ = ["optics_clear_data"]
