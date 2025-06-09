import numpy as np

from isetcam.display import display_create


def test_display_create_default():
    disp = display_create()
    assert disp.name == "LCD-Apple"
    assert disp.spd.shape[0] == disp.wave.shape[0]
    assert disp.gamma is not None
    assert disp.gamma.shape[1] == disp.spd.shape[1]


def test_display_create_specific():
    disp = display_create("lcdExample")
    assert disp.name == "lcdExample"
    assert disp.spd.shape[0] == disp.wave.shape[0]
    assert disp.gamma is not None


def test_display_create_custom_wave():
    new_wave = np.arange(400, 701, 10)
    disp = display_create(wave=new_wave)
    assert np.array_equal(disp.wave, new_wave)
    assert disp.spd.shape[0] == len(new_wave)
