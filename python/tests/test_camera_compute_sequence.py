import numpy as np
import pytest

from isetcam.camera import camera_create, camera_compute_sequence
from isetcam.scene import Scene


def _simple_scene(w: int = 2, h: int = 2, n_wave: int = 3) -> Scene:
    wave = np.arange(500, 500 + 10 * n_wave, 10)
    photons = np.arange(w * h * n_wave, dtype=float).reshape((h, w, n_wave))
    return Scene(photons=photons, wave=wave)


def test_camera_compute_sequence_single():
    cam = camera_create()
    sc = _simple_scene()
    cam, imgs = camera_compute_sequence(cam, scenes=sc, exposure_times=2.0)
    expected = sc.photons.sum(axis=2) * 2.0
    assert len(imgs) == 1
    assert np.allclose(imgs[0], expected)
    assert np.allclose(cam.sensor.volts, expected)


def test_camera_compute_sequence_multiple():
    cam = camera_create()
    sc1 = _simple_scene()
    sc2 = _simple_scene()
    cam, imgs = camera_compute_sequence(
        cam, scenes=[sc1, sc2], exposure_times=[1.0, 0.5]
    )
    exp1 = sc1.photons.sum(axis=2) * 1.0
    exp2 = sc2.photons.sum(axis=2) * 0.5
    assert len(imgs) == 2
    assert np.allclose(imgs[0], exp1)
    assert np.allclose(imgs[1], exp2)
    assert np.allclose(cam.sensor.volts, exp2)


def test_camera_compute_sequence_repeat_exposure():
    cam = camera_create()
    sc1 = _simple_scene()
    sc2 = _simple_scene()
    cam, imgs = camera_compute_sequence(
        cam, scenes=[sc1, sc2], exposure_times=1.5, n_frames=2
    )
    expected = sc1.photons.sum(axis=2) * 1.5
    assert len(imgs) == 2
    assert np.allclose(imgs[0], expected)
    assert np.allclose(imgs[1], expected)


def test_camera_compute_sequence_mismatch_error():
    cam = camera_create()
    sc1 = _simple_scene()
    sc2 = _simple_scene()
    with pytest.raises(ValueError):
        camera_compute_sequence(cam, scenes=[sc1, sc2], exposure_times=[1.0])

