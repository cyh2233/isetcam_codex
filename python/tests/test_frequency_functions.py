import numpy as np

from isetcam.scene import (
    Scene,
    scene_frequency_support,
    scene_frequency_resample,
)
from isetcam.opticalimage import (
    OpticalImage,
    oi_frequency_support,
    oi_frequency_resample,
)


def _simple_scene() -> Scene:
    wave = np.array([550])
    photons = np.arange(16, dtype=float).reshape(4, 4, 1)
    sc = Scene(photons=photons, wave=wave)
    sc.sample_spacing = 1e-3
    return sc


def _simple_oi() -> OpticalImage:
    wave = np.array([550])
    photons = np.arange(9, dtype=float).reshape(3, 3, 1)
    oi = OpticalImage(photons=photons, wave=wave)
    oi.sample_spacing = 2e-3
    return oi


def test_scene_frequency_support_size():
    sc = _simple_scene()
    sup = scene_frequency_support(sc)
    assert sup["fx"].size == sc.photons.shape[1]
    assert sup["fy"].size == sc.photons.shape[0]


def test_scene_frequency_resample_fov():
    sc = _simple_scene()
    out = scene_frequency_resample(sc, 8, 8)
    assert out.photons.shape[:2] == (8, 8)
    old_width = sc.photons.shape[1] * sc.sample_spacing
    new_width = out.photons.shape[1] * out.sample_spacing
    assert np.isclose(old_width, new_width)


def test_oi_frequency_support_and_resample():
    oi = _simple_oi()
    sup = oi_frequency_support(oi)
    assert sup["fx"].size == oi.photons.shape[1]
    out = oi_frequency_resample(oi, 6, 6)
    assert out.photons.shape[:2] == (6, 6)
    old_width = oi.photons.shape[1] * oi.sample_spacing
    new_width = out.photons.shape[1] * out.sample_spacing
    assert np.isclose(old_width, new_width)
