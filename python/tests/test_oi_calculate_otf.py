import numpy as np
from isetcam.opticalimage import (
    OpticalImage,
    oi_calculate_otf,
    oi_frequency_support,
)
from isetcam.optics import Optics


def _simple_oi() -> OpticalImage:
    wave = np.array([550], dtype=float)
    photons = np.ones((4, 4, 1), dtype=float)
    oi = OpticalImage(photons=photons, wave=wave)
    oi.sample_spacing = 1e-3
    return oi


def _simple_optics() -> Optics:
    return Optics(f_number=4.0, f_length=0.005, wave=np.array([550], dtype=float))


def test_frequency_units_mm():
    oi = _simple_oi()
    optics = _simple_optics()
    otf, fs = oi_calculate_otf(oi, optics, units="mm")
    sup = oi_frequency_support(oi, "mm")
    assert np.allclose(fs[:, :, 0], np.meshgrid(sup["fx"], sup["fy"])[0])
    assert np.allclose(fs[:, :, 1], np.meshgrid(sup["fx"], sup["fy"])[1])
    nyquist_mm = (1.0 / (2 * oi.sample_spacing)) / 1e-3 * 0.5
    assert np.isclose(fs[:, -1, 0].max(), nyquist_mm)
    assert otf.shape[2] == 1


def test_defocus_reduces_contrast():
    oi = _simple_oi()
    optics = _simple_optics()
    otf0, _ = oi_calculate_otf(oi, optics)
    optics.defocus_diopters = np.array([0.5])
    otf_d, _ = oi_calculate_otf(oi, optics)
    assert not np.allclose(otf0, otf_d)
