import numpy as np
from isetcam.opticalimage import (
    OpticalImage,
    oi_add,
    get_photons,
    set_photons,
)


def _simple_oi(scale: float) -> OpticalImage:
    wave = np.array([500, 510])
    photons = np.ones((2, 2, 2)) * scale
    return OpticalImage(photons=photons, wave=wave)


def test_oi_add_pair_add():
    o1 = _simple_oi(1.0)
    o2 = _simple_oi(2.0)
    out = oi_add(o1, o2, "add")
    assert np.allclose(get_photons(out), get_photons(o1) + get_photons(o2))


def test_oi_add_pair_average():
    o1 = _simple_oi(1.0)
    o2 = _simple_oi(3.0)
    out = oi_add(o1, o2, "average")
    expected = (get_photons(o1) + get_photons(o2)) / 2
    assert np.allclose(get_photons(out), expected)


def test_oi_add_pair_remove_spatial_mean():
    wave = np.array([500, 510])
    base = np.zeros((2, 2, 2))
    pattern = np.stack(
        [np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])], axis=2
    )
    o1 = OpticalImage(photons=base, wave=wave)
    o2 = OpticalImage(photons=pattern, wave=wave)
    out = oi_add(o1, o2, "remove spatial mean")
    expected = pattern - pattern.mean(axis=(0, 1), keepdims=True)
    assert np.allclose(get_photons(out), expected)


def test_oi_add_weighted_list():
    o1 = _simple_oi(1.0)
    o2 = _simple_oi(2.0)
    out = oi_add([o1, o2], [0.5, 0.25], "add")
    expected = 0.5 * get_photons(o1) + 0.25 * get_photons(o2)
    assert np.allclose(get_photons(out), expected)
