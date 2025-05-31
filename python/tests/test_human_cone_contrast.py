import numpy as np
from isetcam.display import display_create
from isetcam.human import human_cone_isolating, human_cone_contrast


def test_human_cone_contrast_example():
    dsp = display_create('LCD-Apple')
    iso, sig_spd = human_cone_isolating(dsp)
    bg_spd = dsp.spd @ (0.5 * np.ones(3))
    contrast = human_cone_contrast(sig_spd, bg_spd, dsp.wave)

    expected = np.array([
        [-0.40720624, 0.59435214, 0.0252326],
        [-0.68956722, 0.75893057, 0.06778289],
        [0.00689323, -0.07968389, 0.91977398],
    ])

    assert contrast.shape == (3, 3)
    assert np.allclose(contrast, expected, atol=3e-5)
