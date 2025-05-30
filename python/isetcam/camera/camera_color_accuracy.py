from __future__ import annotations

import numpy as np

from .camera_class import Camera
from .camera_compute import camera_compute
from ..scene import scene_create, scene_adjust_luminance
from ..luminance_from_photons import luminance_from_photons


_DEF_LUMINANCE = 100.0


def _patch_means(img: np.ndarray, patch_size: int) -> np.ndarray:
    means = []
    for r in range(4):
        for c in range(6):
            patch = img[r*patch_size:(r+1)*patch_size, c*patch_size:(c+1)*patch_size]
            means.append(np.mean(patch))
    return np.array(means, dtype=float)


def camera_color_accuracy(camera: Camera, lum: float = _DEF_LUMINANCE,
                          patch_size: int = 16) -> tuple[dict[str, np.ndarray], Camera]:
    """Compute a simple color accuracy metric for ``camera``."""
    sc = scene_create("macbeth d65", patch_size=patch_size)
    sc = scene_adjust_luminance(sc, "mean", lum)
    camera_compute(camera, sc)

    sensor_means = _patch_means(camera.sensor.volts, patch_size)
    ref_lum = luminance_from_photons(sc.photons, sc.wave)
    ref_means = _patch_means(ref_lum, patch_size)

    scale = ref_means[3] / sensor_means[3]
    scaled = sensor_means * scale
    delta_e = np.abs(scaled - ref_means)

    result = {
        "deltaE": delta_e,
        "sensor_means": sensor_means,
        "reference_means": ref_means,
    }
    return result, camera


__all__ = ["camera_color_accuracy"]
