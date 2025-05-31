import numpy as np

from isetcam.scene import Scene, scene_thumbnail
from isetcam.opticalimage import OpticalImage, oi_thumbnail


def test_scene_thumbnail_size():
    wave = np.array([500, 600, 700])
    photons = np.ones((32, 16, 3))
    sc = Scene(photons=photons, wave=wave)
    thumb = scene_thumbnail(sc, size=(8, 4))
    assert thumb.shape == (8, 4, 3)
    assert thumb.min() >= 0 and thumb.max() <= 1


def test_oi_thumbnail_size():
    wave = np.array([500, 600, 700])
    photons = np.ones((16, 16, 3))
    oi = OpticalImage(photons=photons, wave=wave)
    thumb = oi_thumbnail(oi, size=(4, 4))
    assert thumb.shape == (4, 4, 3)
    assert thumb.min() >= 0 and thumb.max() <= 1
