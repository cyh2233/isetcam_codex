# mypy: ignore-errors
from __future__ import annotations

import numpy as np

from .scene_class import Scene


def scene_photon_noise(scene: Scene) -> tuple[np.ndarray, np.ndarray]:
    """Apply Poisson photon noise to ``scene``.

    A Gaussian approximation is used when the mean photon count is
    at least 15; otherwise samples are drawn from a Poisson
    distribution.

    Parameters
    ----------
    scene : Scene
        Scene providing the mean photon data.

    Returns
    -------
    tuple of np.ndarray
        ``(noisy_photons, noise)`` where ``noisy_photons`` are the photons
        with noise added and ``noise`` is the difference from the mean
        photons.
    """
    photons = np.asarray(scene.photons, dtype=float)

    noisy = np.empty_like(photons, dtype=float)
    noise = np.empty_like(photons, dtype=float)

    mask = photons >= 15
    if np.any(mask):
        g_noise = np.sqrt(photons[mask]) * np.random.randn(*photons[mask].shape)
        noisy[mask] = photons[mask] + g_noise
        noise[mask] = g_noise
    if np.any(~mask):
        samples = np.random.poisson(photons[~mask])
        noisy[~mask] = samples
        noise[~mask] = samples - photons[~mask]

    return noisy, noise
