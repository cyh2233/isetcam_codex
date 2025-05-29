import numpy as np
from isetcam.human import human_lsf


def test_human_lsf_units():
    lsf_mm, x_mm, wave = human_lsf(wave=np.array([550]), unit="mm")
    lsf_um, x_um, _ = human_lsf(wave=np.array([550]), unit="um")
    assert lsf_mm.shape == lsf_um.shape
    assert np.allclose(x_um, x_mm * 1e3)
    center_idx = x_mm.size // 2
    assert lsf_mm[0, center_idx] == lsf_mm[0].max()
