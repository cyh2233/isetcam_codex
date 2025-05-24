import numpy as np

from isetcam import srgb_to_cct, ie_xyz_from_energy
from isetcam.srgb_xyz import xyz_to_srgb
from isetcam.illuminant import illuminant_blackbody

np.random.seed(0)


def _srgb_from_temp(temp: float) -> np.ndarray:
    wave = np.arange(400, 701, 10)
    spd = illuminant_blackbody(temp, wave)
    xyz = ie_xyz_from_energy(spd[np.newaxis, :], wave)
    srgb, _, _ = xyz_to_srgb(xyz)
    base = srgb.reshape(1, 1, 3)
    # create a small image with variation so percentile computation works
    scales = np.random.uniform(0.5, 1.0, (10, 10, 1))
    img = np.clip(base * scales, 0.0, 1.0)
    return img


def test_srgb_to_cct_basic():
    temps = [3500, 5500, 8000]
    expected = [4000, 6000, 6500]
    for t, exp in zip(temps, expected):
        srgb = _srgb_from_temp(t)
        est, _ = srgb_to_cct(srgb)
        assert np.isclose(est, exp, atol=500)


def test_srgb_to_cct_reuse_table():
    srgb = _srgb_from_temp(6500)
    est, table = srgb_to_cct(srgb)
    assert np.isclose(est, 6500, atol=500)
    srgb2 = _srgb_from_temp(4500)
    est2, table2 = srgb_to_cct(srgb2, table=table)
    assert table2 is table
    assert np.isclose(est2, 5000, atol=500)
