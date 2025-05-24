import numpy as np
from pathlib import Path
from scipy.io import loadmat

from isetcam import iset_root_path

from isetcam import (
    energy_to_quanta,
    ie_xyz_from_energy,
    ie_xyz_from_photons,
    chromaticity,
    cct,
)


def _expected_xyz(wave: np.ndarray, energy: np.ndarray) -> np.ndarray:
    root = iset_root_path()
    mat = loadmat(root / 'data' / 'human' / 'XYZ.mat')
    src_wave = mat['wavelength'].ravel()
    data = mat['data']
    cmf = np.vstack([
        np.interp(wave, src_wave, data[:, i], left=0.0, right=0.0)
        for i in range(3)
    ]).T
    binwidth = wave[1] - wave[0] if len(wave) > 1 else 10
    xw = energy.reshape(-1, len(wave))
    xyz = 683 * xw.dot(cmf) * binwidth
    return xyz.reshape(energy.shape[:-1] + (3,))


def test_ie_xyz_from_energy_xw():
    wave = np.arange(400, 701, 10)
    energy = np.ones((1, len(wave)))
    xyz = ie_xyz_from_energy(energy, wave)
    expected = _expected_xyz(wave, energy)
    assert np.allclose(xyz, expected)


def test_ie_xyz_from_energy_rgb():
    wave = np.arange(400, 701, 10)
    energy = np.ones((1, 1, len(wave)))
    xyz = ie_xyz_from_energy(energy, wave)
    expected = _expected_xyz(wave, energy.reshape(1, len(wave)))
    assert np.allclose(xyz, expected.reshape(1, 1, 3))


def test_ie_xyz_from_photons():
    wave = np.arange(400, 701, 10)
    energy = np.ones((1, len(wave)))
    photons = energy_to_quanta(wave, energy.T).T
    xyz = ie_xyz_from_photons(photons, wave)
    expected = _expected_xyz(wave, energy)
    assert np.allclose(xyz, expected)


def test_chromaticity_xw_and_rgb():
    wave = np.arange(400, 701, 10)
    energy = np.ones((1, len(wave)))
    xyz = _expected_xyz(wave, energy)
    xy = chromaticity(xyz)
    s = xyz.sum(axis=1)
    expected_xy = np.stack([xyz[:, 0] / s, xyz[:, 1] / s], axis=1)
    assert np.allclose(xy, expected_xy)

    xyz_rgb = xyz.reshape(1, 1, 3)
    xy_rgb = chromaticity(xyz_rgb)
    assert np.allclose(xy_rgb, expected_xy.reshape(1, 1, 2))


def test_cct():
    uv = np.array([[0.1978, 0.2000], [0.3122, 0.3000]])
    temps = cct(uv)
    assert temps.shape == (2,)
    assert temps[0] > 6000 and temps[0] < 7000

