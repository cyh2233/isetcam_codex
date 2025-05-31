import numpy as np
import pytest
import matplotlib

matplotlib.use("Agg")

from isetcam.scene import Scene, scene_depth_overlay, scene_depth_range


def _matplotlib_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


def _simple_scene() -> Scene:
    wave = np.array([500, 600, 700])
    photons = np.ones((2, 2, 3))
    sc = Scene(photons=photons, wave=wave)
    sc.depth_map = np.array([[0.4, 0.5], [0.6, 0.7]])
    return sc


def test_scene_depth_range_masking():
    sc = _simple_scene()
    out, mask = scene_depth_range(sc, (0.45, 0.65))
    expected_mask = np.array([[False, True], [True, False]])
    assert np.array_equal(mask, expected_mask)
    expected_photons = np.ones_like(sc.photons)
    for i in range(expected_photons.shape[2]):
        expected_photons[:, :, i] = expected_mask
    assert np.array_equal(out.photons, expected_photons)
    assert np.array_equal(out.depth_map, sc.depth_map * expected_mask)


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_scene_depth_overlay_runs():
    sc = _simple_scene()
    ax = scene_depth_overlay(sc, n=3)
    assert ax is not None
