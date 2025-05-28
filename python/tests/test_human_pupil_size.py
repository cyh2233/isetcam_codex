import numpy as np
from isetcam.human import human_pupil_size


def test_human_pupil_size_ms():
    diam, area = human_pupil_size(100, 'ms')
    expected = 4.9 - 3 * np.tanh(0.4 * np.log10(100) + 1)
    assert np.isclose(diam, expected)
    assert np.isclose(area, np.pi * (expected / 2) ** 2)


def test_human_pupil_size_dg():
    diam, _ = human_pupil_size(50, 'dg')
    expected = 10 ** (0.8558 - 0.000401 * (np.log10(50) + 8.6) ** 3)
    assert np.isclose(diam, expected)


def test_human_pupil_size_sd():
    diam, _ = human_pupil_size(20, 'sd', area=1)
    F = 20 * 1
    expected = 7.75 - 5.75 * (F / 846) ** 0.41 / ((F / 846) ** 0.41 + 2)
    assert np.isclose(diam, expected)


def test_human_pupil_size_wy():
    diam, _ = human_pupil_size(100, 'wy', age=30, area=4, eye_num=1)
    F = 100 * 4 * 0.1
    Dsd = 7.75 - 5.75 * (F / 846) ** 0.41 / ((F / 846) ** 0.41 + 2)
    expected = Dsd + (30 - 28.58) * (0.02132 - 0.009562 * Dsd)
    assert np.isclose(diam, expected)
