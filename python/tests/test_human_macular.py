import numpy as np
from scipy.io import loadmat

from isetcam import iset_root_path
from isetcam.opticalimage import OpticalImage
from isetcam.human import human_macular_transmittance


def test_human_macular_transmittance_basic():
    wave = np.arange(400, 701, 10)
    photons = np.ones((1, 1, len(wave)))
    oi = OpticalImage(photons=photons, wave=wave)

    out = human_macular_transmittance(oi, density=0.35)

    root = iset_root_path()
    mat = loadmat(root / 'data' / 'human' / 'macularPigment.mat')
    src_wave = mat['wavelength'].ravel()
    data = mat['data'].ravel()
    unit = np.interp(wave, src_wave, data, left=0.0, right=0.0) / 0.3521
    trans = 10 ** (-unit * 0.35)
    expected = photons * trans.reshape(1, 1, len(wave))

    assert np.allclose(out.photons, expected)
    assert np.array_equal(out.wave, wave)
