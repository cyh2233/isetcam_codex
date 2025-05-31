import numpy as np

from isetcam.scene import Scene, scene_interpolate_w
from isetcam.opticalimage import OpticalImage, oi_interpolate_w
from isetcam.illuminant import Illuminant


def _scene() -> Scene:
    wave = np.array([500.0, 600.0])
    photons = np.arange(8, dtype=float).reshape(2, 2, 2)
    sc = Scene(photons=photons, wave=wave, name="demo")
    sc.sample_spacing = 1.0
    sc.extra = "meta"
    sc.illuminant = Illuminant(spd=np.array([1.0, 3.0]), wave=wave, name="illum")
    return sc


def _oi() -> OpticalImage:
    wave = np.array([500.0, 600.0])
    photons = np.arange(8, dtype=float).reshape(2, 2, 2)
    oi = OpticalImage(photons=photons, wave=wave, name="demo")
    oi.sample_spacing = 0.5
    oi.extra = "meta"
    oi.illuminant = Illuminant(spd=np.array([2.0, 4.0]), wave=wave, name="illum")
    return oi


def test_scene_interpolate_w():
    sc = _scene()
    new_wave = np.array([500.0, 550.0, 600.0])
    out = scene_interpolate_w(sc, new_wave)

    assert np.array_equal(out.wave, new_wave)
    assert out.name == sc.name
    assert getattr(out, "sample_spacing") == sc.sample_spacing
    assert getattr(out, "extra") == sc.extra

    for i in range(2):
        for j in range(2):
            expected = np.interp(new_wave, sc.wave, sc.photons[i, j, :])
            assert np.allclose(out.photons[i, j, :], expected)

    expected_illum = np.interp(new_wave, sc.illuminant.wave, sc.illuminant.spd)
    assert isinstance(out.illuminant, Illuminant)
    assert np.allclose(out.illuminant.spd, expected_illum)


def test_oi_interpolate_w():
    oi = _oi()
    new_wave = np.array([500.0, 550.0, 600.0])
    out = oi_interpolate_w(oi, new_wave)

    assert np.array_equal(out.wave, new_wave)
    assert out.name == oi.name
    assert getattr(out, "sample_spacing") == oi.sample_spacing
    assert getattr(out, "extra") == oi.extra

    for i in range(2):
        for j in range(2):
            expected = np.interp(new_wave, oi.wave, oi.photons[i, j, :])
            assert np.allclose(out.photons[i, j, :], expected)

    expected_illum = np.interp(new_wave, oi.illuminant.wave, oi.illuminant.spd)
    assert isinstance(out.illuminant, Illuminant)
    assert np.allclose(out.illuminant.spd, expected_illum)
