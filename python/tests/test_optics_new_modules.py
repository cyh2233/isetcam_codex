import numpy as np

from isetcam.optics import (
    optics_airy_psf,
    optics_barrel_distortion,
    optics_fresnel,
)


def test_optics_airy_psf_normalized():
    psf = optics_airy_psf(64, 8.0)
    assert np.isclose(psf.sum(), 1.0)
    assert psf.max() <= 1.0


def test_optics_barrel_distortion_strength():
    x = np.array([1.0])
    y = np.array([0.0])
    xd, yd = optics_barrel_distortion(x, y, k1=-0.3)
    r_in = np.hypot(x, y)
    r_out = np.hypot(xd, yd)
    assert r_out < r_in


def test_optics_fresnel_delta():
    field = np.zeros((32, 32), dtype=complex)
    field[16, 16] = 1.0
    out = optics_fresnel(field, dx=1e-6, wavelength=500e-9, distance=0.01)
    energy_in = np.sum(np.abs(field) ** 2)
    energy_out = np.sum(np.abs(out) ** 2)
    assert np.isclose(energy_in, energy_out)
