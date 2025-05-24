"""Utilities for saving :class:`Scene` objects to disk."""

from __future__ import annotations

from pathlib import Path

from scipy.io import savemat

from .scene_class import Scene


def scene_to_file(scene: Scene, path: str | Path) -> None:
    """Save ``scene`` to ``path`` as a MATLAB ``.mat`` file.

    Only the ``photons`` and ``wave`` fields are stored. The data is saved
    under the variable name ``'scene'``.

    Parameters
    ----------
    scene:
        Scene instance to be saved.
    path:
        Destination of the MAT-file.
    """
    data = {"photons": scene.photons, "wave": scene.wave}
    savemat(str(Path(path)), {"scene": data})

