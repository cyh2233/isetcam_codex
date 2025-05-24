import numpy as np

from isetcam import ctemp_to_srgb, ie_xyz_from_energy
from isetcam.illuminant import illuminant_blackbody
from isetcam.srgb_xyz import xyz_to_srgb


def _expected(temp: float, wave: np.ndarray) -> np.ndarray:
    spd = illuminant_blackbody(temp, wave)
    xyz = ie_xyz_from_energy(spd[np.newaxis, :], wave)
    srgb, _, _ = xyz_to_srgb(xyz)
    return srgb[0]


def _expected_multi(temps: np.ndarray, wave: np.ndarray) -> np.ndarray:
    spd = np.stack([illuminant_blackbody(t, wave) for t in temps], axis=0)
    xyz = ie_xyz_from_energy(spd, wave)
    srgb, _, _ = xyz_to_srgb(xyz)
    return srgb


def test_ctemp_to_srgb_default_wave():
    temps = [3000, 5500, 8000]
    for t in temps:
        srgb = ctemp_to_srgb(t)
        wave = np.arange(400, 701, 10)
        expected = _expected(t, wave)
        assert np.allclose(srgb, expected)


def test_ctemp_to_srgb_multi():
    wave = np.arange(420, 681, 20)
    temps = np.array([3500, 6500, 9000])
    srgb = ctemp_to_srgb(temps, wave)
    assert srgb.shape == (len(temps), 3)
    expected = _expected_multi(temps, wave)
    assert np.allclose(srgb, expected)

