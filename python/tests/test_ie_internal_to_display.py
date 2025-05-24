import numpy as np

from isetcam.imgproc import ie_internal_to_display


def test_matrix_computation():
    cmf = np.array([
        [0.2, 0.3, 0.1],
        [0.1, 0.2, 0.4],
        [0.3, 0.1, 0.2],
    ])
    spd = np.array([
        [0.5, 0.2, 0.1],
        [0.4, 0.1, 0.3],
        [0.2, 0.3, 0.6],
    ])
    T = ie_internal_to_display(cmf, spd)
    expected = np.linalg.inv(spd.T @ cmf)
    assert np.allclose(T, expected)


def test_round_trip():
    cmf = np.array([
        [0.2, 0.3, 0.1],
        [0.1, 0.2, 0.4],
        [0.3, 0.1, 0.2],
    ])
    spd = np.array([
        [0.5, 0.2, 0.1],
        [0.4, 0.1, 0.3],
        [0.2, 0.3, 0.6],
    ])
    T = ie_internal_to_display(cmf, spd)
    internal_values = np.random.rand(5, 3)
    display_rgb = internal_values @ T
    reconstructed = display_rgb @ spd.T @ cmf
    assert np.allclose(reconstructed, internal_values)
