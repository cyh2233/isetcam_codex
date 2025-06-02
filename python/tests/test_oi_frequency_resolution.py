import numpy as np

from isetcam.opticalimage import (
    OpticalImage,
    oi_frequency_resolution,
)


def _simple_oi() -> OpticalImage:
    wave = np.array([550], dtype=float)
    photons = np.ones((4, 4, 1), dtype=float)
    oi = OpticalImage(photons=photons, wave=wave)
    oi.sample_spacing = 2e-3
    oi.wangular = 10.0
    return oi


def _unit_frequency_list(n: int) -> np.ndarray:
    idx = np.arange(n)
    mid = n // 2 if n % 2 == 0 else (n - 1) // 2
    c = idx - mid
    if c.max() == 0:
        return c.astype(float)
    return c / np.max(np.abs(c))


def test_resolution_cpd_values():
    oi = _simple_oi()
    res = oi_frequency_resolution(oi)
    max_fx = (oi.photons.shape[1] / 2) / oi.wangular
    expected_fx = _unit_frequency_list(oi.photons.shape[1]) * max_fx
    assert np.allclose(res["fx"], expected_fx)
    assert np.allclose(res["fy"], expected_fx)


def test_resolution_units_mm():
    oi = _simple_oi()
    res_cpd = oi_frequency_resolution(oi)
    res_mm = oi_frequency_resolution(oi, "mm")
    scale = (oi.wangular / (oi.sample_spacing * oi.photons.shape[1])) * 1e-3
    assert np.allclose(res_mm["fx"], res_cpd["fx"] * scale)
    assert np.allclose(res_mm["fy"], res_cpd["fy"] * scale)
