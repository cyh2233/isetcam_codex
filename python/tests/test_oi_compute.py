import numpy as np
from isetcam.scene import Scene
from isetcam.optics import Optics
from isetcam.opticalimage import oi_compute


def _simple_scene() -> Scene:
    wave = np.array([500, 510, 520], dtype=float)
    photons = np.array([[[1.0, 2.0, 3.0]]])
    return Scene(photons=photons, wave=wave)


def test_oi_compute_interpolation():
    sc = _simple_scene()
    optics_wave = np.array([500, 505, 515, 520], dtype=float)
    optics = Optics(f_number=2.0, f_length=2.0, wave=optics_wave)
    oi = oi_compute(sc, optics)
    expected = np.array([np.interp(optics_wave, sc.wave, sc.photons[0, 0])])
    expected = expected.reshape(1, 1, optics_wave.size)
    assert np.allclose(oi.photons, expected)
    assert np.array_equal(oi.wave, optics_wave)


def test_oi_compute_transmittance_and_scale():
    sc = _simple_scene()
    trans = np.array([0.5, 2.0, 1.0], dtype=float)
    optics = Optics(f_number=1.0, f_length=2.0, wave=sc.wave, transmittance=trans)
    oi = oi_compute(sc, optics)
    scale = (optics.f_length / optics.f_number) ** 2
    expected = sc.photons * trans * scale
    assert np.allclose(oi.photons, expected)
    assert np.array_equal(oi.wave, sc.wave)


