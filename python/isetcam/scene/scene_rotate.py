# mypy: ignore-errors
"""Rotate the photon data of a Scene."""

from __future__ import annotations

from scipy.ndimage import rotate as nd_rotate

from .scene_class import Scene


def scene_rotate(scene: Scene, angle: float, fill: float = 0) -> Scene:
    """Rotate ``scene`` by ``angle`` degrees.

    Parameters
    ----------
    scene : Scene
        Input scene to rotate.
    angle : float
        Rotation angle in degrees. Positive values rotate counter-clockwise.
    fill : float, optional
        Value used to fill areas created by the rotation. Defaults to 0.

    Returns
    -------
    Scene
        New scene containing the rotated photon data with the same wavelength
        samples and name.
    """

    photons = scene.photons
    rotated = nd_rotate(
        photons,
        angle,
        axes=(1, 0),
        reshape=True,
        order=1,
        mode="constant",
        cval=float(fill),
    )
    return Scene(photons=rotated, wave=scene.wave, name=scene.name)
