import numpy as np
from isetcam.imgproc import image_illuminant_correction


def test_gray_world_means_equalized():
    img = np.array(
        [
            [[1.0, 2.0, 4.0], [1.0, 2.0, 4.0]],
            [[1.0, 2.0, 4.0], [1.0, 2.0, 4.0]],
        ]
    )
    corrected, T = image_illuminant_correction(img, "gray world")
    expected_T = np.diag([1.0, 0.5, 0.25])
    assert np.allclose(T, expected_T)
    avg = corrected.mean(axis=(0, 1))
    assert np.allclose(avg, [1.0, 1.0, 1.0])


def test_none_returns_identity():
    img = np.random.rand(2, 2, 3)
    corrected, T = image_illuminant_correction(img, "none")
    assert np.allclose(corrected, img)
    assert np.allclose(T, np.eye(3))
