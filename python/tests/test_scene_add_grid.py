import numpy as np

from isetcam.scene import Scene, scene_add_grid


def _simple_scene(width: int = 6, height: int = 5, n_wave: int = 1) -> Scene:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    return Scene(photons=photons, wave=wave, name="base")


def _expected_grid(data: np.ndarray, p_size, g_width):
    out = data.copy()
    rows, cols = data.shape[:2]
    r_space, c_space = p_size
    out[:g_width, :, :] = 0
    for r in range(r_space, rows - 1, r_space):
        out[r:r+g_width, :, :] = 0
    out[rows-g_width:rows, :, :] = 0
    out[:, :g_width, :] = 0
    for c in range(c_space, cols - 1, c_space):
        out[:, c:c+g_width, :] = 0
    out[:, cols-g_width:cols, :] = 0
    return out


def test_scene_add_grid_basic():
    sc = _simple_scene(6, 5, 1)
    out = scene_add_grid(sc, (2, 3), g_width=1)
    expected = _expected_grid(sc.photons, (2, 3), 1)
    assert np.array_equal(out.photons, expected)
    assert np.array_equal(out.wave, sc.wave)


def test_scene_add_grid_single_spacing_width():
    sc = _simple_scene(7, 7, 1)
    out = scene_add_grid(sc, 3, g_width=2)
    expected = _expected_grid(sc.photons, (3, 3), 2)
    assert np.array_equal(out.photons, expected)


def test_scene_add_grid_name():
    sc = _simple_scene(4, 4, 1)
    out = scene_add_grid(sc, 2, g_width=1)
    assert out.name != sc.name
    assert "grid" in out.name
