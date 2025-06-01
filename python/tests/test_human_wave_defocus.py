import numpy as np
from isetcam.human import human_wave_defocus


def test_human_wave_defocus_defaults():
    out = human_wave_defocus()
    wave = np.arange(400, 701)
    q1 = 1.7312
    q2 = 0.63346
    q3 = 0.21410
    expected = q1 - (q2 / (wave * 1e-3 - q3))
    assert np.allclose(out, expected)
