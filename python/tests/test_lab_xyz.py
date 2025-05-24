import numpy as np

from isetcam import xyz_to_lab, lab_to_xyz


WHITEPOINT = np.array([0.95047, 1.0, 1.08883])


def test_xyz_lab_round_trip_xw():
    xyz = np.random.rand(10, 3)
    lab = xyz_to_lab(xyz, WHITEPOINT)
    xyz2 = lab_to_xyz(lab, WHITEPOINT)
    assert np.allclose(xyz2, xyz, atol=1e-6)


def test_xyz_lab_round_trip_rgb():
    xyz = np.random.rand(4, 5, 3)
    lab = xyz_to_lab(xyz, WHITEPOINT)
    xyz2 = lab_to_xyz(lab, WHITEPOINT)
    assert np.allclose(xyz2, xyz, atol=1e-6)
