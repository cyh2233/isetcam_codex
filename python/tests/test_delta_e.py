import numpy as np

from isetcam.metrics import (
    delta_e_ab,
    delta_e_94,
    delta_e_2000,
    delta_e_uv,
)


def test_delta_e_2000_known_example():
    lab1 = np.array([50.0, 2.6772, -79.7751])
    lab2 = np.array([50.0, 0.0, -82.7485])
    expected = 2.0425
    val = float(delta_e_2000(lab1, lab2))
    assert np.isclose(val, expected, atol=1e-4)


def test_delta_e_94_basic():
    lab1 = np.array([60.0, 20.0, 30.0])
    lab2 = np.array([60.0, 20.0, 30.0])
    assert delta_e_94(lab1, lab2) == 0


def test_delta_e_uv_simple():
    luv1 = np.array([[50.0, 10.0, -20.0], [70.0, 5.0, 5.0]])
    luv2 = luv1 + 1
    expected = np.sqrt(np.sum((luv1 - luv2) ** 2, axis=1))
    assert np.allclose(delta_e_uv(luv1, luv2), expected)


def test_delta_e_ab_versions():
    lab1 = np.array([[50.0, 2.0, 3.0], [20.0, -5.0, 1.0]])
    lab2 = lab1 + 1
    assert np.allclose(delta_e_ab(lab1, lab2, "2000"), delta_e_2000(lab1, lab2))
    assert np.allclose(delta_e_ab(lab1, lab2, "1994"), delta_e_94(lab1, lab2))
    diff = np.sqrt(np.sum((lab1 - lab2) ** 2, axis=1))
    assert np.allclose(delta_e_ab(lab1, lab2, "1976"), diff)
