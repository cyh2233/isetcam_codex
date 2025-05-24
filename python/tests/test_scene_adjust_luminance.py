import numpy as np

from isetcam.scene import Scene, scene_adjust_luminance
from isetcam.luminance_from_photons import luminance_from_photons


def _simple_scene(scale: float) -> Scene:
    wave = np.array([500, 510])
    photons = np.ones((2, 2, 2)) * scale
    return Scene(photons=photons, wave=wave)


def test_scene_adjust_luminance_mean():
    sc = _simple_scene(1.0)
    target = 10.0
    out = scene_adjust_luminance(sc, "mean", target)
    lum = luminance_from_photons(out.photons, out.wave)
    assert np.isclose(lum.mean(), target)


def test_scene_adjust_luminance_peak():
    wave = np.array([500, 510])
    photons = np.array(
        [[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]]
    )
    sc = Scene(photons=photons, wave=wave)
    target = 20.0
    out = scene_adjust_luminance(sc, "peak", target)
    lum = luminance_from_photons(out.photons, out.wave)
    assert np.isclose(lum.max(), target)

