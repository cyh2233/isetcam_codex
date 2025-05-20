import numpy as np
from isetcam import vc_constants, vc_get_image_format, quanta_to_energy

def test_vc_constants():
    assert np.isclose(vc_constants('h'), 6.626176e-34)
    assert np.isclose(vc_constants('q'), 1.602177e-19)
    assert np.isclose(vc_constants('c'), 2.99792458e8)
    assert np.isclose(vc_constants('j'), 1.380662e-23)
    assert np.isclose(vc_constants('mmPerDeg'), 0.3)


def test_vc_get_image_format():
    data_rgb = np.zeros((2, 2, 3))
    wave = np.array([500, 510, 520])
    assert vc_get_image_format(data_rgb, wave) == 'RGB'
    data_xw = np.zeros((4, 3))
    assert vc_get_image_format(data_xw, wave) == 'XW'


def test_quanta_to_energy():
    wave = np.array([500, 510, 520])
    photons = np.ones((1, 3))
    energy = quanta_to_energy(wave, photons)
    expected = (vc_constants('h') * vc_constants('c') / 1e-9) * photons / wave
    assert np.allclose(energy, expected)
