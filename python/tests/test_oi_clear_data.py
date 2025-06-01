import numpy as np

from isetcam.opticalimage import OpticalImage, oi_clear_data


def _simple_oi() -> OpticalImage:
    wave = np.array([500, 510])
    photons = np.ones((2, 2, 2), dtype=float)
    return OpticalImage(photons=photons, wave=wave)


def test_oi_clear_data_removes_fields():
    oi = _simple_oi()
    oi.depth_map = np.ones((2, 2))
    oi.wangular = 1.0
    oi.optics_psf = np.ones((3, 3))
    oi.crop_rect = (0, 0, 1, 1)
    oi.full_size = (2, 2)
    oi.sample_spacing = 0.5

    out = oi_clear_data(oi)
    assert out is oi
    for fld in [
        "depth_map",
        "wangular",
        "optics_psf",
        "crop_rect",
        "full_size",
        "sample_spacing",
    ]:
        assert not hasattr(out, fld)


def test_oi_clear_data_no_fields():
    oi = _simple_oi()
    out = oi_clear_data(oi)
    assert out is oi
    assert np.array_equal(out.photons, oi.photons)
    assert np.array_equal(out.wave, oi.wave)
