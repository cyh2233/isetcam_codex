# mypy: ignore-errors
"""Initialize spatial properties of a :class:`Scene`."""

from __future__ import annotations

from .scene_class import Scene

_DEFAULT_FOV = 10.0  # degrees


def scene_init_spatial(scene: Scene) -> Scene:
    """Assign default ``fov`` to ``scene`` if missing."""
    if getattr(scene, "fov", None) is None:
        scene.fov = _DEFAULT_FOV
    return scene


__all__ = ["scene_init_spatial"]
