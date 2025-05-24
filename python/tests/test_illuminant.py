import numpy as np

from isetcam.illuminant import Illuminant, illuminant_blackbody, illuminant_create


def test_illuminant_create_d65_peak():
    illum = illuminant_create('D65')
    peak_wave = illum.wave[illum.spd.argmax()]
    assert peak_wave == 460


def test_illuminant_create_interp():
    wave = np.array([400, 500, 600])
    illum = illuminant_create('D65', wave)
    assert np.array_equal(illum.wave, wave)
    assert illum.spd.shape == wave.shape


def test_blackbody_shape():
    wave = np.arange(400, 701, 10)
    spd = illuminant_blackbody(6500, wave)
    assert spd.shape == wave.shape
    assert np.all(spd >= 0)
