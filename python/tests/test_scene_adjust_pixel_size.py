import math
import numpy as np

from isetcam.scene import Scene, scene_adjust_pixel_size
from isetcam.opticalimage import OpticalImage


def _simple_scene() -> Scene:
    wave = np.array([550])
    photons = np.ones((2, 4, 1))
    sc = Scene(photons=photons, wave=wave)
    sc.sample_spacing = 1e-3
    sc.distance = 1.0
    return sc


def _simple_oi() -> OpticalImage:
    wave = np.array([550])
    photons = np.ones((2, 4, 1))
    return OpticalImage(photons=photons, wave=wave)


def test_scene_adjust_pixel_size_smaller():
    sc = _simple_scene()
    oi = _simple_oi()
    pixel = 0.5e-3
    out, new_d = scene_adjust_pixel_size(sc, oi, pixel)
    assert math.isclose(new_d, 0.5)
    assert math.isclose(out.distance, new_d)
    expected_fov = 2 * math.degrees(math.atan(pixel * 4 / (2 * new_d)))
    assert math.isclose(out.fov, expected_fov)


def test_scene_adjust_pixel_size_larger():
    sc = _simple_scene()
    oi = _simple_oi()
    pixel = 2e-3
    out, new_d = scene_adjust_pixel_size(sc, oi, pixel)
    assert math.isclose(new_d, 2.0)
    expected_fov = 2 * math.degrees(math.atan(pixel * 4 / (2 * new_d)))
    assert math.isclose(out.fov, expected_fov)


