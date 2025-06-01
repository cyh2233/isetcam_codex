"""Initialize geometric properties of a :class:`Scene`."""

from __future__ import annotations

from .scene_class import Scene

_DEFAULT_DISTANCE = 1.2  # meters


def scene_init_geometry(scene: Scene) -> Scene:
    """Assign default ``distance`` to ``scene`` if missing."""
    if getattr(scene, "distance", None) is None:
        scene.distance = _DEFAULT_DISTANCE
    return scene


__all__ = ["scene_init_geometry"]
