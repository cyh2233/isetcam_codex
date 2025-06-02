# mypy: ignore-errors
"""Utility to remove optional attributes from a Scene."""

from __future__ import annotations

from .scene_class import Scene

# Attributes that may be attached to Scene instances by various helpers
# or user interfaces. These are removed by :func:`scene_clear_data`.
_OPTIONAL_ATTRS = [
    "depth_map",
    "ui",
    "crop_rect",
    "full_size",
    "sample_spacing",
    "pad_size",
]


def scene_clear_data(scene: Scene) -> Scene:
    """Remove cached or optional attributes from ``scene``.

    Parameters
    ----------
    scene : Scene
        Scene object to clean.

    Returns
    -------
    Scene
        The same ``scene`` instance with extraneous attributes removed.
    """

    for attr in _OPTIONAL_ATTRS:
        if hasattr(scene, attr):
            delattr(scene, attr)
    return scene


__all__ = ["scene_clear_data"]
