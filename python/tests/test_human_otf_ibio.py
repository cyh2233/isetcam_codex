import numpy as np
from isetcam.human import human_otf_ibio, ijspeert


def test_human_otf_ibio_center():
    otf, fs, wave = human_otf_ibio(wave=np.array([550]))
    assert otf.shape[2] == 1
    assert np.isclose(otf[0, 0, 0], 1.0)
    center = tuple(s // 2 for s in fs.shape[:2])
    assert otf[center[0], center[1], 0] == 0.0


def test_ijspeert_psf_mtf():
    age = 30
    pupil = 3.0
    pig = 0.16
    q = np.array([0, 10, 20])
    phi = np.linspace(0.0, 0.1, 6)
    mtf, psf, lsf = ijspeert(age, pupil, pig, q, phi)
    expected_mtf = np.array([1.0, 0.34677202, 0.25422147])
    expected_psf = np.array([
        1.17493834e07,
        8.95813104e00,
        1.45078897e00,
        5.81181966e-01,
        3.13392710e-01,
        1.94609463e-01,
    ])
    expected_lsf = np.array([
        1.94364933e03,
        4.56622089e-01,
        1.89883575e-01,
        1.28781366e-01,
        1.01152741e-01,
        8.54575077e-02,
    ])
    assert np.allclose(mtf, expected_mtf)
    assert np.allclose(psf, expected_psf)
    assert np.allclose(lsf, expected_lsf)
