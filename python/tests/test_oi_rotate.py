import numpy as np
from scipy.ndimage import rotate as nd_rotate

from isetcam.opticalimage import OpticalImage, oi_rotate


def _simple_oi(width: int = 3, height: int = 3, n_wave: int = 1) -> OpticalImage:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    return OpticalImage(photons=photons, wave=wave, name="simple")


def test_oi_rotate_90():
    oi = _simple_oi(2, 3, 1)
    out = oi_rotate(oi, 90)
    expected = np.rot90(oi.photons, axes=(0, 1))
    assert np.array_equal(out.photons, expected)
    assert np.array_equal(out.wave, oi.wave)
    assert out.name == oi.name


def test_oi_rotate_general():
    oi = _simple_oi(3, 3, 1)
    angle = 30
    out = oi_rotate(oi, angle, fill=-1)
    expected = nd_rotate(
        oi.photons,
        angle,
        axes=(1, 0),
        reshape=True,
        order=1,
        mode="constant",
        cval=-1,
    )
    assert np.allclose(out.photons, expected)
    assert np.array_equal(out.wave, oi.wave)
    assert out.name == oi.name
