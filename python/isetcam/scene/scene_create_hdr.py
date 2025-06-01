"""Factory for basic HDR :class:`Scene` types."""

from __future__ import annotations

from .scene_class import Scene
from .scene_hdr_image import scene_hdr_image
from .scene_hdr_chart import scene_hdr_chart
from .scene_hdr_lights import scene_hdr_lights


_VALID = {
    "hdrimage": scene_hdr_image,
    "hdrchart": scene_hdr_chart,
    "hdrlights": scene_hdr_lights,
}


def scene_create_hdr(name: str, **kwargs) -> Scene:
    """Create a high dynamic range :class:`Scene` by name."""

    key = name.lower().replace(" ", "")
    if key not in _VALID:
        raise ValueError(f"Unknown HDR scene type '{name}'")
    return _VALID[key](**kwargs)


__all__ = ["scene_create_hdr"]
