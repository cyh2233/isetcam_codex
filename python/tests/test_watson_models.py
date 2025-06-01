import numpy as np

from isetcam.human import watson_impulse_response, watson_rgc_spacing


def test_watson_impulse_response_default():
    imp, t, mtf, freq = watson_impulse_response()
    assert t.size == 500
    assert np.isclose(imp.sum(), 1.0)
    assert np.allclose(imp[:5], [
        1.64341760e-09,
        2.39250786e-06,
        5.68669063e-05,
        3.98655496e-04,
        1.53883323e-03,
    ])
    assert np.allclose(mtf[:3], [1.0, 1.00990868, 1.03712801])
    assert np.allclose(freq[:3], [1.001001, 2.002002, 3.003003])


def test_watson_rgc_spacing_basic():
    smf0, r, smf1d = watson_rgc_spacing(5)
    assert r.size == 1000
    assert smf1d.shape == (4, r.size)
    assert np.allclose(smf1d[:, 0], [
        0.00653927,
        0.00654839,
        0.00652906,
        0.00656183,
    ])
    assert np.isclose(smf0[3, 3], 0.014671495492619382)
    assert smf0.shape == (6, 6)
