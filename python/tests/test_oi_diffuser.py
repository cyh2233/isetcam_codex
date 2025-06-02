import numpy as np
from scipy.ndimage import gaussian_filter, shift as nd_shift

from isetcam.opticalimage import (
    OpticalImage,
    oi_diffuser,
    oi_birefringent_diffuser,
)


def _simple_oi(width: int = 5, height: int = 4, n_wave: int = 1) -> OpticalImage:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    oi = OpticalImage(photons=photons, wave=wave)
    oi.sample_spacing = 1e-6  # 1 micron per pixel
    return oi


def test_oi_diffuser_gaussian():
    oi = _simple_oi(4, 4, 1)
    out = oi_diffuser(oi, 1.0, method="gaussian")
    sigma_pix = 1.0 / (oi.sample_spacing * 1e6)
    expected = gaussian_filter(oi.photons, sigma=(sigma_pix, sigma_pix, 0))
    assert np.allclose(out.photons, expected)
    assert np.array_equal(out.wave, oi.wave)


def test_oi_birefringent_diffuser():
    oi = _simple_oi(4, 4, 1)
    out = oi_birefringent_diffuser(oi, 1.0)
    delta = 1.0 / (oi.sample_spacing * 1e6)
    base = [
        (delta, delta),
        (-delta, delta),
        (delta, -delta),
        (-delta, -delta),
    ]
    expected = np.zeros_like(oi.photons, dtype=float)
    for dx, dy in base:
        shifted = nd_shift(
            oi.photons,
            shift=(dy, dx, 0),
            order=1,
            mode="constant",
            cval=0.0,
        )
        expected += shifted
    expected /= len(base)
    assert np.allclose(out.photons, expected)
    assert np.array_equal(out.wave, oi.wave)


def test_oi_diffuser_birefringent_dispatch():
    oi = _simple_oi(3, 3, 1)
    out1 = oi_diffuser(oi, 1.0, method="birefringent")
    out2 = oi_birefringent_diffuser(oi, 1.0)
    assert np.allclose(out1.photons, out2.photons)
    assert np.array_equal(out1.wave, out2.wave)
