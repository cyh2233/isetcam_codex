import numpy as np
from isetcam.imgproc import image_esser_transform


def test_simple_transform():
    wave = np.array([1.0, 2.0, 3.0])
    sensor_qe = np.array([[1, 0], [0, 1], [0, 0]], dtype=float)
    target_qe = np.array([[0, 1], [1, 0], [0, 0]], dtype=float)
    surfaces = np.eye(3)
    T = image_esser_transform(
        sensor_qe,
        target_qe,
        wave,
        illuminant=np.ones_like(wave),
        surfaces=surfaces,
    )
    expected = np.array([[0, 1], [1, 0]], dtype=float)
    assert np.allclose(T, expected)
