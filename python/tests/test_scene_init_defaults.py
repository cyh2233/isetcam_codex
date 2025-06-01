import numpy as np

from isetcam.scene import Scene, scene_init_geometry, scene_init_spatial


def _simple_scene():
    wave = np.array([550], dtype=float)
    photons = np.ones((1, 1, 1), dtype=float)
    return Scene(photons=photons, wave=wave)


def test_defaults_assigned_when_missing():
    sc = _simple_scene()
    scene_init_geometry(sc)
    scene_init_spatial(sc)
    assert sc.distance == 1.2
    assert sc.fov == 10.0


def test_existing_values_preserved():
    sc = _simple_scene()
    sc.distance = 2.0
    sc.fov = 20.0
    scene_init_geometry(sc)
    scene_init_spatial(sc)
    assert sc.distance == 2.0
    assert sc.fov == 20.0
