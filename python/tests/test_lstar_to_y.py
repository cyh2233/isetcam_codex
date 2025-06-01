import numpy as np

from isetcam import y_to_lstar, lstar_to_y

WHITE_Y = 100.0


def test_round_trip_xw():
    y = np.random.rand(10) * WHITE_Y
    L = y_to_lstar(y, WHITE_Y)
    y2 = lstar_to_y(L, WHITE_Y)
    assert np.allclose(y2, y, atol=1e-6)


def test_round_trip_rgb():
    y = np.random.rand(4, 5) * WHITE_Y
    L = y_to_lstar(y, WHITE_Y)
    y2 = lstar_to_y(L, WHITE_Y)
    assert np.allclose(y2, y, atol=1e-6)
