import numpy as np
from isetcam.opticalimage import OpticalImage, oi_photon_noise


def test_oi_photon_noise_gaussian():
    np.random.seed(0)
    photons = np.full((100, 100, 1), 20.0, dtype=float)
    oi = OpticalImage(photons=photons.copy(), wave=np.array([550]))
    noisy, noise = oi_photon_noise(oi)

    assert noisy.shape == photons.shape
    assert np.allclose(noisy - photons, noise)
    assert abs(noise.mean()) < 0.1
    assert abs(noise.var() - 20.0) < 2.0


def test_oi_photon_noise_poisson():
    np.random.seed(1)
    photons = np.full((100, 100, 1), 5.0, dtype=float)
    oi = OpticalImage(photons=photons.copy(), wave=np.array([550]))
    noisy, noise = oi_photon_noise(oi)

    assert abs(noisy.mean() - 5.0) < 0.1
    assert abs(noise.mean()) < 0.1
    assert abs(noise.var() - 5.0) < 1.0
