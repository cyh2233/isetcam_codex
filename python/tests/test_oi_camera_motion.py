import numpy as np

from isetcam.opticalimage import OpticalImage, oi_camera_motion


def _simple_oi(width: int = 3, height: int = 3, n_wave: int = 1) -> OpticalImage:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    return OpticalImage(photons=photons, wave=wave, name="simple")


def test_camera_motion_average():
    oi = _simple_oi(3, 3, 1)
    path = [(0, 0), (1, 0)]
    out = oi_camera_motion(oi, {"path": path, "fill": 0})

    expected = np.zeros_like(oi.photons, dtype=float)
    # shift (0,0)
    expected += oi.photons
    # shift (1,0)
    shifted = np.zeros_like(oi.photons)
    shifted[:, 1:, :] = oi.photons[:, :-1, :]
    expected += shifted
    expected /= 2.0

    assert np.allclose(out.photons, expected)
    assert np.array_equal(out.wave, oi.wave)
    assert out.name == oi.name


def test_camera_motion_weighted():
    oi = _simple_oi(3, 3, 1)
    path = [(0, 0), (0, 1)]
    weights = [1, 2]
    out = oi_camera_motion(oi, {"path": path, "weights": weights, "fill": 0})

    shifted0 = oi.photons
    shifted1 = np.zeros_like(oi.photons)
    shifted1[1:, :, :] = oi.photons[:-1, :, :]
    expected = (weights[0] * shifted0 + weights[1] * shifted1) / sum(weights)

    assert np.allclose(out.photons, expected)

