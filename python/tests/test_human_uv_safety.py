import numpy as np
from isetcam.human import human_uv_safety


def test_human_uv_safety_eye():
    wave = np.arange(300, 401, 10, dtype=float)
    energy = np.ones_like(wave) * 0.01
    val, level, safe = human_uv_safety(energy, wave, method="eye", duration=100)
    assert isinstance(val, (bool, np.bool_))
    assert level > 0
    assert isinstance(safe, (bool, np.bool_))
