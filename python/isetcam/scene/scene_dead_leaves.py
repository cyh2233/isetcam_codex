# mypy: ignore-errors
import numpy as np

from .scene_class import Scene
from .imgtargets.img_dead_leaves import img_dead_leaves


def scene_dead_leaves(patch_size: int = 256, noise_level: float = 0.0, seed: int | None = None) -> Scene:
    """Return a Scene containing a dead-leaves chart.

    Parameters
    ----------
    patch_size: int
        Size in pixels of the square image.
    noise_level: float
        Standard deviation of optional additive Gaussian noise.
    seed: int, optional
        Seed for the random number generator.
    """
    img = img_dead_leaves(patch_size=patch_size, noise_level=noise_level, seed=seed)
    wave = np.array([550.0], dtype=float)
    photons = img[:, :, None]
    sc = Scene(photons=photons, wave=wave, name="Dead leaves")
    sc.fov = 10.0
    return sc


__all__ = ["scene_dead_leaves"]
