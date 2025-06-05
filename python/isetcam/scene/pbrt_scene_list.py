# mypy: ignore-errors
"""List PBRT scenes from ISET3D resources."""

from __future__ import annotations

from pathlib import Path
from typing import List


def pbrt_scene_list() -> List[str]:
    """Return available PBRT scene names.

    The helper relies on the optional :mod:`iset3d` package which provides
    :func:`piDirGet` for locating PBRT resources. When the package is not
    installed an :class:`ImportError` is raised.
    """

    try:  # pragma: no cover - optional dependency
        import iset3d  # type: ignore
    except Exception as exc:  # pragma: no cover - library may not be present
        raise ImportError("iset3d required for PBRT scene listing") from exc

    base = Path(iset3d.piDirGet("scenes"))  # type: ignore[attr-defined]
    names: list[str] = []
    if base.exists():
        for path in base.rglob("*.pbrt"):
            if path.is_file():
                names.append(path.stem)
    return sorted(set(names))


__all__ = ["pbrt_scene_list"]
