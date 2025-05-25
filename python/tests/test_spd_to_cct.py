import numpy as np

from isetcam import spd_to_cct
from isetcam.illuminant import illuminant_blackbody


def test_spd_to_cct_single():
    wave = np.arange(400, 701, 10)
    temp = 6500
    spd = illuminant_blackbody(temp, wave)
    est, uv = spd_to_cct(wave, spd)
    assert np.isclose(est, temp, atol=500)
    assert uv.shape == (1, 2)


def test_spd_to_cct_multi():
    wave = np.arange(400, 701, 10)
    temps = np.array([4000, 8000])
    spd = np.vstack([illuminant_blackbody(t, wave) for t in temps]).T
    est, uv = spd_to_cct(wave, spd)
    assert uv.shape == (len(temps), 2)
    assert np.allclose(est, temps, atol=500)
