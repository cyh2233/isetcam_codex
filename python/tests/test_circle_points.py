import numpy as np

from isetcam import circle_points


def _expected_points(rad_spacing: float) -> tuple[np.ndarray, np.ndarray]:
    theta = np.arange(0.0, 2 * np.pi + rad_spacing / 2, rad_spacing)
    if theta[-1] > 2 * np.pi:
        theta = theta[:-1]
    if theta[-1] != 2 * np.pi:
        theta = np.append(theta, 2 * np.pi)
    return np.cos(theta), np.sin(theta)


def test_circle_points_default():
    x, y = circle_points()
    ex, ey = _expected_points(2 * np.pi / 60)
    assert np.allclose(x, ex)
    assert np.allclose(y, ey)


def test_circle_points_spacing():
    rad_spacing = 2 * np.pi / 25
    x, y = circle_points(rad_spacing)
    ex, ey = _expected_points(rad_spacing)
    assert np.allclose(x, ex)
    assert np.allclose(y, ey)
