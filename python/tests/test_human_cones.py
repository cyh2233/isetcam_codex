import numpy as np
from scipy.io import loadmat

from isetcam.human import human_cones
from isetcam import ie_read_spectra, data_path


def test_human_cones_no_macular():
    wave = np.arange(370, 731)
    cones, mac, out_wave = human_cones('stockmanAbs', wave)
    data, _, _, _ = ie_read_spectra(data_path('human/stockmanAbs.mat'), wave)
    assert np.array_equal(out_wave, wave)
    assert np.allclose(mac, 1.0)
    assert np.allclose(cones, data)


def test_human_cones_with_macular():
    wave = np.arange(370, 731)
    cones, mac, _ = human_cones('stockmanAbs', wave, macular_density=0.6, included_density=0.35)
    cone_data, _, _, _ = ie_read_spectra(data_path('human/stockmanAbs.mat'), wave)
    mat = loadmat(data_path('human/macularPigment.mat'))
    unit = np.interp(
        wave, mat['wavelength'].ravel(), mat['data'].ravel(), left=0.0, right=0.0
    ) / 0.3521
    expected_mac = 10 ** (-(unit * (0.6 - 0.35)))
    expected_cones = cone_data * expected_mac[:, None]
    assert np.allclose(mac, expected_mac)
    assert np.allclose(cones, expected_cones)
