import numpy as np

from isetcam.display import (
    Display,
    display_description,
    display_reflectance,
    display_set_max_luminance,
    display_set_white_point,
)
from isetcam.ie_xyz_from_energy import ie_xyz_from_energy


def test_display_description():
    wave = np.array([500, 510, 520])
    spd = np.ones((3, 3))
    gamma = np.linspace(0, 1, 4).reshape(4, 1).repeat(3, axis=1)
    disp = Display(spd=spd, wave=wave, gamma=gamma, name="demo")
    desc = display_description(disp)
    assert "demo" in desc
    assert "# primaries" in desc
    assert "Color bit depth" in desc


def test_display_set_max_luminance():
    wave = np.linspace(400, 700, 10)
    spd = np.ones((len(wave), 3))
    disp = Display(spd=spd.copy(), wave=wave)
    display_set_max_luminance(disp, 200)
    white_xyz = ie_xyz_from_energy(disp.spd.sum(axis=1), disp.wave).reshape(3)
    assert np.isclose(white_xyz[1], 200, atol=1e-4)
    assert disp.max_luminance == 200


def test_display_set_white_point():
    wave = np.array([500, 510, 520])
    spd = np.eye(3)
    disp = Display(spd=spd.copy(), wave=wave)
    display_set_max_luminance(disp, 100)
    xy_before = disp.white_point[:2] / disp.white_point.sum()
    display_set_white_point(disp, (0.4, 0.4))
    xy_after = disp.white_point[:2] / disp.white_point.sum()
    assert not np.allclose(xy_before, xy_after)


def test_display_reflectance_basic():
    disp, prim, ill = display_reflectance(6500)
    assert isinstance(disp, Display)
    assert prim.shape[1] == 3
    assert ill.ndim == 1 and ill.size == prim.shape[0]
    assert disp.max_luminance is not None
