import numpy as np
from isetcam import ie_responsivity_convert


def test_e2q_q2e_round_trip():
    wave = np.arange(400, 501, 20)
    resp = np.random.rand(len(wave), 3)
    resp_q, _ = ie_responsivity_convert(resp, wave, 'e2q')
    resp_e, _ = ie_responsivity_convert(resp_q, wave, 'q2e')
    assert np.allclose(resp_e, resp)


def test_q2e_e2q_round_trip():
    wave = np.arange(450, 551, 25)
    resp = np.random.rand(len(wave), 2)
    resp_e, _ = ie_responsivity_convert(resp, wave, 'q2e')
    resp_q, _ = ie_responsivity_convert(resp_e, wave, 'e2q')
    assert np.allclose(resp_q, resp)
