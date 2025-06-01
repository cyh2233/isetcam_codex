import numpy as np
from isetcam.human import human_core, human_achromatic_otf


def test_human_core_single_sf():
    sf = np.array([10])
    out = human_core(sf)
    wave = np.arange(400, 701)
    ach = human_achromatic_otf(sf)
    expected = np.ones((wave.size, 1)) * ach
    assert out.shape == expected.shape
    assert np.allclose(out, expected)
