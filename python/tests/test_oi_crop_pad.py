import numpy as np
import pytest

from isetcam.opticalimage import OpticalImage, oi_crop, oi_pad


def _simple_oi(width: int = 4, height: int = 4, n_wave: int = 2) -> OpticalImage:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    return OpticalImage(photons=photons, wave=wave)


def test_oi_crop_basic():
    oi = _simple_oi(4, 4, 2)
    out = oi_crop(oi, (1, 1, 2, 2))
    expected = oi.photons[1:3, 1:3, :]
    assert np.array_equal(out.photons, expected)
    assert np.array_equal(out.wave, oi.wave)
    assert out.crop_rect == (1, 1, 2, 2)
    assert out.full_size == (4, 4)


def test_oi_crop_out_of_bounds():
    oi = _simple_oi(4, 4, 1)
    with pytest.raises(ValueError):
        oi_crop(oi, (3, 3, 2, 2))


def test_oi_pad_scalar():
    oi = _simple_oi(2, 2, 1)
    out = oi_pad(oi, 1, value=-1)
    expected = np.pad(oi.photons, ((1, 1), (1, 1), (0, 0)), constant_values=-1)
    assert np.array_equal(out.photons, expected)
    assert np.array_equal(out.wave, oi.wave)


def test_oi_pad_tuple():
    oi = _simple_oi(2, 2, 1)
    out = oi_pad(oi, (1, 2, 3, 4), value=5)
    expected = np.pad(
        oi.photons,
        ((1, 2), (3, 4), (0, 0)),
        constant_values=5,
    )
    assert np.array_equal(out.photons, expected)
    assert np.array_equal(out.wave, oi.wave)

