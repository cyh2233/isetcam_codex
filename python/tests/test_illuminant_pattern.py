import numpy as np

from isetcam.scene import Scene, scene_illuminant_pattern, scene_illuminant_ss
from isetcam.opticalimage import OpticalImage, oi_illuminant_pattern, oi_illuminant_ss


def _simple_scene() -> Scene:
    wave = np.array([500, 510])
    photons = np.ones((2, 3, 2), dtype=float)
    sc = Scene(photons=photons, wave=wave)
    sc.illuminant = np.array([1.0, 2.0])
    return sc


def _simple_oi() -> OpticalImage:
    wave = np.array([500, 510])
    photons = np.ones((2, 3, 2), dtype=float)
    oi = OpticalImage(photons=photons, wave=wave)
    oi.illuminant = np.array([1.0, 2.0])
    return oi


def test_scene_illuminant_ss():
    sc = _simple_scene()
    out = scene_illuminant_ss(sc)
    expected = np.tile(sc.illuminant.reshape(1, 1, -1), (2, 3, 1))
    assert np.allclose(out.illuminant, expected)


def test_scene_illuminant_pattern():
    sc = scene_illuminant_ss(_simple_scene())
    pattern = np.array([[1.0, 2.0, 3.0], [0.5, 0.5, 0.5]])
    out = scene_illuminant_pattern(sc, pattern)
    assert np.allclose(out.photons, sc.photons * pattern[:, :, None])
    assert np.allclose(out.illuminant, sc.illuminant * pattern[:, :, None])


def test_oi_illuminant_ss():
    oi = _simple_oi()
    out = oi_illuminant_ss(oi)
    expected = np.tile(oi.illuminant.reshape(1, 1, -1), (2, 3, 1))
    assert np.allclose(out.illuminant, expected)


def test_oi_illuminant_pattern():
    oi = oi_illuminant_ss(_simple_oi())
    pattern = np.array([[2.0, 2.0, 1.0], [1.0, 0.5, 0.5]])
    out = oi_illuminant_pattern(oi, pattern)
    assert np.allclose(out.photons, oi.photons * pattern[:, :, None])
    assert np.allclose(out.illuminant, oi.illuminant * pattern[:, :, None])
