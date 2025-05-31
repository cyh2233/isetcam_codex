import numpy as np
from isetcam.display import display_create
from isetcam.human import human_cone_isolating


def test_human_cone_isolating_basic():
    dsp = display_create('LCD-Apple')
    iso, spd = human_cone_isolating(dsp)

    expected_iso = np.array([
        [0.5, -0.15395504, -0.00267701],
        [-0.49142262, 0.5, -0.02156203],
        [0.0343801, -0.07811632, 0.5],
    ])

    assert iso.shape == (3, 3)
    assert spd.shape == (dsp.wave.size, 3)
    assert np.allclose(iso, expected_iso, atol=1e-5)
    assert np.allclose(
        spd[0],
        [-9.21315187e-07, 1.97421203e-06, 2.03042851e-06],
        atol=1e-10,
    )
    assert np.allclose(
        spd[-1],
        [1.46054133e-05, 7.27774837e-06, 1.68922615e-05],
        atol=1e-9,
    )
