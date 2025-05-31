import numpy as np

from isetcam.scene import Scene, scene_clear_data


def _simple_scene() -> Scene:
    wave = np.array([500, 510])
    photons = np.ones((2, 2, 2), dtype=float)
    return Scene(photons=photons, wave=wave)


def test_scene_clear_data_removes_fields():
    sc = _simple_scene()
    sc.depth_map = np.ones((2, 2))
    sc.ui = object()
    sc.crop_rect = (0, 0, 1, 1)
    sc.full_size = (2, 2)
    sc.sample_spacing = 0.5

    out = scene_clear_data(sc)
    assert out is sc
    for fld in [
        "depth_map",
        "ui",
        "crop_rect",
        "full_size",
        "sample_spacing",
    ]:
        assert not hasattr(out, fld)


def test_scene_clear_data_no_fields():
    sc = _simple_scene()
    out = scene_clear_data(sc)
    assert out is sc
    assert np.array_equal(out.photons, sc.photons)
    assert np.array_equal(out.wave, sc.wave)
