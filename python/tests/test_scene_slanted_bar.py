import numpy as np

from isetcam.scene import scene_slanted_bar
from isetcam.scene.imgtargets import img_slanted_bar
from isetcam.energy_to_quanta import energy_to_quanta


def _estimate_slope(photons: np.ndarray, ill_val: float) -> float:
    h = (photons.shape[0] - 1) // 2
    xs, ys = [], []
    for j, x in enumerate(range(-h, h + 1)):
        col = photons[:, j, 0]
        if np.any(col == ill_val) and np.any(col == ill_val * 1e-6):
            idx = np.argmax(col == ill_val)
            xs.append(x)
            ys.append(idx - h)
    if len(xs) < 2:
        return float("nan")
    return float(np.polyfit(xs, ys, 1)[0])


def test_img_slanted_bar_size():
    img = img_slanted_bar(im_size=32)
    assert img.shape == (33, 33)
    assert img.max() == 1.0
    assert img.min() >= 1e-6


def test_scene_slanted_bar_properties():
    slope = 2.6
    sc = scene_slanted_bar(im_size=32, bar_slope=slope, field_of_view=3)
    h = (sc.photons.shape[0] - 1) // 2
    assert sc.photons.shape[:2] == (2 * h + 1, 2 * h + 1)
    assert sc.photons.shape[2] == sc.wave.size
    assert sc.fov == 3

    ill = energy_to_quanta(sc.wave, np.ones_like(sc.wave)).ravel()
    col = h
    assert np.allclose(sc.photons[h + 1, col, :], ill)
    assert np.allclose(sc.photons[h - 1, col, :], ill * 1e-6)

    est = _estimate_slope(sc.photons, ill[0])
    assert np.isclose(est, slope, rtol=0.02)
