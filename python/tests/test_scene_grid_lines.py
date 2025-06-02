import numpy as np

from isetcam.scene import scene_grid_lines
from isetcam.illuminant import illuminant_create
from isetcam.energy_to_quanta import energy_to_quanta


_DEF_WAVE = np.arange(400, 701, 10, dtype=float)


def test_scene_grid_lines_spacing():
    sc = scene_grid_lines(size=16, spacing=4, spectral_type="ep", line_thickness=1)
    half = 4 // 2
    # Check horizontal and vertical lines at expected positions
    assert np.allclose(sc.photons[half, :, 0], 1.0)
    assert np.allclose(sc.photons[:, half, 0], 1.0)
    # Interior not on grid should be near zero
    assert np.isclose(sc.photons[0, 0, 0], 1e-5)


def test_scene_grid_lines_spectral_types():
    sc_d65 = scene_grid_lines(size=8, spacing=4, spectral_type="d65")
    d65 = illuminant_create("D65", _DEF_WAVE).spd.astype(float)
    center = 4 // 2
    assert np.array_equal(sc_d65.wave, _DEF_WAVE)
    assert np.allclose(sc_d65.photons[center, center, :], d65)
    assert np.allclose(sc_d65.illuminant, d65)

    sc_ee = scene_grid_lines(size=8, spacing=4, spectral_type="ee")
    ee = energy_to_quanta(_DEF_WAVE, np.ones_like(_DEF_WAVE)).ravel()
    assert np.allclose(sc_ee.photons[center, center, :], ee)
    assert np.allclose(sc_ee.illuminant, ee)
