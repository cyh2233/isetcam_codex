import numpy as np

from isetcam.opticalimage import OpticalImage, oi_adjust_illuminance
from isetcam.luminance_from_photons import luminance_from_photons


def _simple_oi(scale: float) -> OpticalImage:
    wave = np.array([500, 510])
    photons = np.ones((2, 2, 2)) * scale
    return OpticalImage(photons=photons, wave=wave)


def test_oi_adjust_illuminance_scale_up():
    oi = _simple_oi(1.0)
    target = 10.0
    out = oi_adjust_illuminance(oi, target)
    illum = luminance_from_photons(out.photons, out.wave)
    assert np.isclose(illum.mean(), target)


def test_oi_adjust_illuminance_scale_down():
    oi = _simple_oi(5.0)
    target = 1.0
    out = oi_adjust_illuminance(oi, target)
    illum = luminance_from_photons(out.photons, out.wave)
    assert np.isclose(illum.mean(), target)
