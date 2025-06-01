import numpy as np

from isetcam.opticalimage import OpticalImage, oi_translate


def _simple_oi(width: int = 3, height: int = 3, n_wave: int = 1) -> OpticalImage:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    return OpticalImage(photons=photons, wave=wave)


def test_oi_translate_positive():
    oi = _simple_oi(3, 3, 1)
    out = oi_translate(oi, 1, 1, fill=-1)
    expected = np.full_like(oi.photons, -1)
    expected[1:, 1:, :] = oi.photons[:-1, :-1, :]
    assert np.array_equal(out.photons, expected)
    assert np.array_equal(out.wave, oi.wave)
    assert out.name == oi.name


def test_oi_translate_negative():
    oi = _simple_oi(3, 3, 1)
    out = oi_translate(oi, -1, -1, fill=0)
    expected = np.zeros_like(oi.photons)
    expected[:-1, :-1, :] = oi.photons[1:, 1:, :]
    assert np.array_equal(out.photons, expected)


def test_oi_translate_outside():
    oi = _simple_oi(2, 2, 1)
    out = oi_translate(oi, 5, 0, fill=2)
    expected = np.full_like(oi.photons, 2)
    assert np.array_equal(out.photons, expected)

