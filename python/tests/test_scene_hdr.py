import numpy as np

from isetcam.scene import (
    scene_hdr_image,
    scene_hdr_chart,
    scene_hdr_lights,
)


def test_scene_hdr_image_patches():
    wave = np.array([550.0])
    sc = scene_hdr_image(
        3,
        image_size=8,
        dynamic_range=1,
        patch_size=2,
        background=None,
        patch_shape="square",
        wave=wave,
    )
    levels = np.logspace(0, 1, 3)[::-1]
    row = (8 - 2) // 2
    assert np.allclose(sc.photons[row:row+2, 1:3, 0], levels[0])
    assert np.allclose(sc.photons[row:row+2, 3:5, 0], levels[1])
    assert np.allclose(sc.photons[row:row+2, 5:7, 0], levels[2])
    ratio = sc.photons[row, 1, 0] / sc.photons[row, 5, 0]
    assert np.isclose(ratio, 10)


def test_scene_hdr_chart_levels():
    wave = np.array([550.0])
    sc = scene_hdr_chart(dynamic_range=100, n_levels=3, cols_per_level=2, wave=wave)
    first = sc.photons[0, 0, 0]
    last = sc.photons[0, -1, 0]
    assert np.isclose(first / last, 100)
    assert np.allclose(sc.photons[:, 0:2, 0], first)
    assert np.allclose(sc.photons[:, 4:6, 0], last)


def test_scene_hdr_lights_dynamic_range():
    wave = np.array([550.0])
    sc = scene_hdr_lights(image_size=16, dynamic_range=1000, wave=wave)
    assert np.isclose(sc.photons.max(), 1000)
    assert np.isclose(sc.photons.min(), 1)
