# mypy: ignore-errors
"""Add black grid lines to a Scene."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .scene_class import Scene


def scene_add_grid(scene: Scene, p_size: int | Sequence[int], g_width: int = 1) -> Scene:  # noqa: E501
    """Overlay black grid lines on ``scene`` photon data.

    Parameters
    ----------
    scene : Scene
        Input scene whose photons will be modified.
    p_size : int or sequence of int
        Grid spacing in pixels specified as ``(row_spacing, col_spacing)``.
        A single integer uses the same spacing in both dimensions.
    g_width : int, optional
        Width of the grid lines in pixels. Defaults to ``1``.

    Returns
    -------
    Scene
        New scene with grid lines added. Wavelength information is
        preserved and the scene name is appended with "with grid".
    """

    if isinstance(p_size, Sequence):
        spacing = list(p_size)
        if len(spacing) == 1:
            spacing = [int(spacing[0]), int(spacing[0])]
        elif len(spacing) >= 2:
            spacing = [int(spacing[0]), int(spacing[1])]
        else:
            raise ValueError("p_size must be an int or sequence of one or two ints")
    else:
        spacing = [int(p_size), int(p_size)]

    g_width = int(g_width)
    if g_width < 1:
        raise ValueError("g_width must be >= 1")

    photons = scene.photons.copy()
    rows, cols = photons.shape[:2]
    r_space, c_space = spacing

    # Row lines including edges
    photons[:g_width, :, :] = 0
    for r in range(r_space, rows - 1, r_space):
        photons[r : r + g_width, :, :] = 0
    photons[rows - g_width : rows, :, :] = 0

    # Column lines including edges
    photons[:, :g_width, :] = 0
    for c in range(c_space, cols - 1, c_space):
        photons[:, c : c + g_width, :] = 0
    photons[:, cols - g_width : cols, :] = 0

    name = f"{scene.name} with grid" if scene.name else "with grid"

    return Scene(photons=photons, wave=scene.wave, name=name)
