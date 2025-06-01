import numpy as np
from pathlib import Path

from isetcam.scene import scene_from_file, Scene
from isetcam import luminance_from_energy, data_path


def test_scene_from_file_rgb():
    fpath = data_path('images/rgb/adelson.png')
    wave = np.array([450, 550, 650, 750])
    sc = scene_from_file(fpath, wave=wave)
    assert isinstance(sc, Scene)
    assert sc.photons.dtype == float
    assert sc.photons.ndim == 3 and sc.photons.shape[2] == 4
    assert np.array_equal(sc.wave, wave)


def test_scene_from_file_mean_luminance():
    fpath = data_path('images/rgb/adelson.png')
    wave = np.array([450, 550, 650, 750])
    target = 10.0
    sc = scene_from_file(fpath, mean_luminance=target, wave=wave)
    lum = luminance_from_energy(sc.photons, sc.wave)
    assert np.isclose(lum.mean(), target, atol=1e-6)


def test_scene_from_file_gray():
    fpath = data_path('images/targets/usaf1951/USAF1951-72dpi.jpg')
    wave = np.array([550])
    sc = scene_from_file(fpath, wave=wave)
    assert sc.photons.ndim == 3 and sc.photons.shape[2] == 1
    assert np.array_equal(sc.wave, wave)


def test_scene_from_file_uint8_scaling():
    fpath = data_path('images/rgb/adelson.png')
    sc = scene_from_file(fpath)
    assert sc.photons.dtype == float
    assert sc.photons.min() >= 0.0
    assert sc.photons.max() <= 1.0
