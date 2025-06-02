# mypy: ignore-errors
"""Utilities for saving :class:`VCImage` objects to disk."""

from __future__ import annotations

from pathlib import Path

from scipy.io import savemat

from .vcimage_class import VCImage


def ip_to_file(ip: VCImage, path: str | Path) -> None:
    """Save ``ip`` to ``path`` as a MATLAB ``.mat`` file.

    The RGB data and wavelength samples are stored using the variables
    ``rgb`` and ``wave``.  When present, the ``name`` field is also saved.
    """
    data = {
        "rgb": ip.rgb,
        "wave": ip.wave,
    }
    if getattr(ip, "name", None) is not None:
        data["name"] = ip.name
    savemat(str(Path(path)), data)
