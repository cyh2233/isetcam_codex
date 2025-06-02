import numpy as np

from isetcam import xyz_to_cct, ie_xyz_from_energy
from isetcam.illuminant import illuminant_blackbody


def _xyz_from_temp(temp: float) -> np.ndarray:
    wave = np.arange(400, 701, 10)
    spd = illuminant_blackbody(temp, wave)
    return ie_xyz_from_energy(spd[np.newaxis, :], wave)


def test_xyz_to_cct_xw():
    temps = np.array([4000, 6500, 8000])
    expected = np.array([
        4001.91716709,
        6505.23418953,
        7999.99130153,
    ])
    xyz = np.vstack([_xyz_from_temp(t) for t in temps])
    est = xyz_to_cct(xyz)
    assert np.allclose(est, expected, atol=1e-6)


def test_xyz_to_cct_rgb():
    temp = 6500
    expected = 6505.23418953
    xyz = _xyz_from_temp(temp).reshape(1, 1, 3)
    est = xyz_to_cct(xyz)
    assert est.shape == (1, 1)
    assert np.isclose(est[0, 0], expected, atol=1e-6)
