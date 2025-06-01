import numpy as np
from scipy.io import loadmat

from isetcam.scene import Scene, scene_calculate_luminance
from isetcam import data_path
from isetcam.quanta2energy import quanta_to_energy


def _expected_luminance(wave: np.ndarray, photons: np.ndarray) -> np.ndarray:
    mat = loadmat(data_path('human/luminosity.mat'))
    V = np.interp(wave, mat['wavelength'].ravel(), mat['data'].ravel(), left=0.0, right=0.0)
    energy = quanta_to_energy(wave, photons)
    binwidth = wave[1] - wave[0] if len(wave) > 1 else 10
    xw = energy.reshape(-1, len(wave))
    lum = 683 * xw.dot(V) * binwidth
    return lum.reshape(photons.shape[:2])


def test_scene_calculate_luminance_basic():
    wave = np.array([500, 510, 520])
    photons = np.array([
        [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
        [[7.0, 8.0, 9.0], [10.0, 11.0, 12.0]],
    ])
    sc = Scene(photons=photons, wave=wave)
    lum, mean_lum = scene_calculate_luminance(sc)
    expected = _expected_luminance(wave, photons)
    assert np.allclose(lum, expected)
    assert np.isclose(mean_lum, expected.mean())


def test_scene_calculate_luminance_single_wave():
    wave = np.array([550])
    photons = np.ones((1, 1, 1))
    sc = Scene(photons=photons, wave=wave)
    lum, mean_lum = scene_calculate_luminance(sc)
    expected = _expected_luminance(wave, photons)
    assert lum.shape == (1, 1)
    assert np.allclose(lum, expected)
    assert np.isclose(mean_lum, expected.mean())
