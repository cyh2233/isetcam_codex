import numpy as np

from isetcam.opticalimage import oi_create, OpticalImage


def test_oi_create_default():
    oi = oi_create()
    assert isinstance(oi, OpticalImage)
    assert oi.photons.shape == (128, 128, oi.wave.size)
    assert np.allclose(oi.photons, 1.0)


def test_oi_create_custom():
    wave = np.array([500, 510, 520])
    oi = oi_create(name="demo", size=4, wave=wave)
    assert oi.name == "demo"
    assert np.array_equal(oi.wave, wave)
    assert oi.photons.shape == (4, 4, wave.size)
    assert np.allclose(oi.photons, 1.0)
