import numpy as np

from isetcam.scene import scene_create, Scene
from isetcam.luminance_from_photons import luminance_from_photons


def test_scene_create_macbeth_basic():
    sc = scene_create("macbeth d65", patch_size=4)
    assert isinstance(sc, Scene)
    assert sc.photons.shape[0] == 4 * 4
    assert sc.photons.shape[1] == 6 * 4
    assert sc.photons.shape[2] == sc.wave.size


def test_scene_create_macbeth_mean_luminance():
    sc = scene_create("macbeth d65", patch_size=4, mean_luminance=5.0)
    lum = luminance_from_photons(sc.photons, sc.wave)
    assert np.isclose(lum.mean(), 5.0, atol=1e-6)


def test_scene_create_uniform_monochromatic():
    sc = scene_create("uniform monochromatic", wavelength=600, size=10)
    assert sc.wave.size == 1 and sc.wave[0] == 600
    assert sc.photons.shape == (10, 10, 1)
    assert np.allclose(sc.photons, 1.0)


def test_scene_create_whitenoise():
    sc = scene_create("whitenoise", size=8, contrast=0.1)
    assert sc.photons.shape == (8, 8, 1)
    assert sc.photons.min() >= 0


def test_scene_create_frequency_sweep():
    sc = scene_create("frequency sweep", size=32, max_freq=8)
    assert sc.photons.shape == (32, 32, 1)
    # Higher variance in the top row than the bottom row
    top_var = sc.photons[0, :, 0].var()
    bottom_var = sc.photons[-1, :, 0].var()
    assert top_var > bottom_var


def test_scene_create_grid_lines():
    sc = scene_create("grid lines", size=32, spacing=8, thickness=1)
    assert sc.photons.shape == (32, 32, 1)
    mid = 8 // 2
    # Check that a grid line exists at the expected location
    assert np.allclose(sc.photons[mid, :, 0], sc.photons.max())
    assert np.allclose(sc.photons[:, mid, 0], sc.photons.max())


def test_scene_create_macbeth_tungsten_different():
    sc_d65 = scene_create("macbeth d65", patch_size=4)
    sc_t = scene_create("macbeth tungsten", patch_size=4)
    assert sc_d65.photons.shape == sc_t.photons.shape
    assert not np.allclose(sc_d65.photons, sc_t.photons)

