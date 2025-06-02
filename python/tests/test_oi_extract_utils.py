import numpy as np
import pytest

from isetcam.opticalimage import (
    OpticalImage,
    oi_extract_bright,
    oi_extract_mask,
)


def _simple_oi(width: int = 3, height: int = 3, n_wave: int = 2) -> OpticalImage:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    return OpticalImage(photons=photons, wave=wave)


def test_oi_extract_bright():
    oi = _simple_oi(2, 2, 1)
    out = oi_extract_bright(oi, 2)
    expected = np.where(oi.photons >= 2, oi.photons, 0)
    assert np.array_equal(out.photons, expected)
    assert np.array_equal(out.wave, oi.wave)


def test_oi_extract_mask_2d():
    oi = _simple_oi(2, 2, 2)
    mask = np.array([[True, False], [False, True]])
    out = oi_extract_mask(oi, mask)
    expected = np.where(mask[:, :, None], oi.photons, 0)
    assert np.array_equal(out.photons, expected)


def test_oi_extract_mask_invalid():
    oi = _simple_oi(2, 2, 1)
    mask = np.ones((3, 3), dtype=bool)
    with pytest.raises(ValueError):
        oi_extract_mask(oi, mask)
