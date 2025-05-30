import numpy as np
from isetcam import (
    color_transform_matrix_create,
    color_transform_matrix,
    iset_root_path,
)


def test_color_transform_matrix_create_arrays():
    src = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    true_T = np.array([[1.0, 2.0], [-1.0, 0.5]])
    dst = src @ true_T
    T = color_transform_matrix_create(src, dst)
    assert np.allclose(T, true_T)


def test_color_transform_matrix_create_files():
    root = iset_root_path()
    xyz_file = root / "data" / "human" / "XYZ.mat"
    stock_file = root / "data" / "human" / "stockman.mat"
    wave = np.arange(400, 701, 5)
    T = color_transform_matrix_create(xyz_file, stock_file, wave)
    expected = color_transform_matrix("xyz2sto")
    assert T.shape == (3, 3)
    assert np.allclose(T, expected, rtol=5e-4, atol=5e-05)
