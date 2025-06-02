import numpy as np

from isetcam.opticalimage import OpticalImage, oi_make_even_row_col


def _simple_oi(width: int, height: int, n_wave: int = 1) -> OpticalImage:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    oi = OpticalImage(photons=photons, wave=wave)
    oi.sample_spacing = 1e-3  # 1 mm per pixel
    return oi


def test_make_even_no_change():
    oi = _simple_oi(4, 4, 1)
    out = oi_make_even_row_col(oi)
    assert out.photons.shape == oi.photons.shape
    assert getattr(out, "sample_spacing") == getattr(oi, "sample_spacing")


def test_make_even_pad_and_spacing():
    oi = _simple_oi(5, 3, 1)
    out = oi_make_even_row_col(oi)
    assert out.photons.shape[:2] == (4, 6)
    old_width = oi.photons.shape[1] * oi.sample_spacing
    new_width = out.photons.shape[1] * out.sample_spacing
    assert np.isclose(old_width, new_width)
    assert np.array_equal(out.photons[:-1, :-1, :], oi.photons)
