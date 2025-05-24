import numpy as np
from isetcam.metrics import scielab, sc_params, SCIELABParams
from isetcam import xyz_to_lab

WHITEPOINT = np.array([0.95047, 1.0, 1.08883])


def test_scielab_identical():
    img = np.random.rand(4, 4, 3)
    params = sc_params()
    de = scielab(img, img, WHITEPOINT, params)
    assert np.allclose(de, 0)


def test_scielab_matches_deltae2000():
    img1 = np.array([[[0.5, 0.5, 0.5]]])
    img2 = np.array([[[0.4, 0.4, 0.4]]])
    params = SCIELABParams()
    de = scielab(img1, img2, WHITEPOINT, params)
    lab1 = xyz_to_lab(img1, WHITEPOINT)
    lab2 = xyz_to_lab(img2, WHITEPOINT)
    # internal helper for deltaE2000
    from isetcam.metrics.scielab import _delta_e_2000

    expected = _delta_e_2000(lab1, lab2)
    assert np.allclose(de, expected)


def test_scielab_symmetry():
    img1 = np.random.rand(2, 3, 3)
    img2 = np.random.rand(2, 3, 3)
    params = sc_params()
    d1 = scielab(img1, img2, WHITEPOINT, params)
    d2 = scielab(img2, img1, WHITEPOINT, params)
    assert np.allclose(d1, d2)
