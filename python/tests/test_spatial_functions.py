import numpy as np

from isetcam.scene import (
    Scene,
    scene_spatial_support,
    scene_spatial_resample,
)
from isetcam.opticalimage import (
    OpticalImage,
    oi_spatial_support,
    oi_spatial_resample,
)


def _simple_scene() -> Scene:
    wave = np.array([550])
    photons = np.arange(16, dtype=float).reshape(4, 4, 1)
    sc = Scene(photons=photons, wave=wave)
    sc.sample_spacing = 1e-3  # 1 mm per pixel
    return sc


def _simple_oi() -> OpticalImage:
    wave = np.array([550])
    photons = np.arange(9, dtype=float).reshape(3, 3, 1)
    oi = OpticalImage(photons=photons, wave=wave)
    oi.sample_spacing = 2e-3  # 2 mm per pixel
    return oi


def test_scene_spatial_support_units():
    sc = _simple_scene()
    sup_m = scene_spatial_support(sc)
    expected = np.array([-1.5e-3, -0.5e-3, 0.5e-3, 1.5e-3])
    assert np.allclose(sup_m["x"], expected)
    assert np.allclose(sup_m["y"], expected)
    sup_mm = scene_spatial_support(sc, "mm")
    assert np.allclose(sup_mm["x"], expected * 1e3)


def test_scene_spatial_resample_fov():
    sc = _simple_scene()
    out = scene_spatial_resample(sc, 0.5e-3, method="nearest")
    assert out.photons.shape[:2] == (8, 8)
    old_width = sc.photons.shape[1] * sc.sample_spacing
    new_width = out.photons.shape[1] * out.sample_spacing
    assert np.isclose(old_width, new_width)


def test_scene_spatial_resample_methods():
    sc = _simple_scene()
    lin = scene_spatial_resample(sc, 0.5e-3, method="linear")
    near = scene_spatial_resample(sc, 0.5e-3, method="nearest")
    assert lin.photons.shape == near.photons.shape
    assert not np.allclose(lin.photons, near.photons)


def test_oi_spatial_support_and_resample():
    oi = _simple_oi()
    sup = oi_spatial_support(oi)
    expected_x = np.array([-2e-3, 0.0, 2e-3])
    assert np.allclose(sup["x"], expected_x)
    out = oi_spatial_resample(oi, 1e-3)
    assert out.photons.shape[:2] == (6, 6)
    old_width = oi.photons.shape[1] * oi.sample_spacing
    new_width = out.photons.shape[1] * out.sample_spacing
    assert np.isclose(old_width, new_width)

