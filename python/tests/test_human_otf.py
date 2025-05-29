import numpy as np
from isetcam.human import human_otf


def test_human_otf_center():
    otf, fs, wave = human_otf(wave=np.array([550]))
    r, c = fs.shape[:2]
    center = otf[r // 2, c // 2, 0]
    assert np.isclose(center, 1.0)
    assert otf.shape[2] == 1
    assert fs.shape[0] == fs.shape[1]
