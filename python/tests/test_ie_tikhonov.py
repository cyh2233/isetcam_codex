import numpy as np

from isetcam import ie_tikhonov


A = np.array([[1.0, 0.0, 2.0],
              [0.0, 1.0, 1.0],
              [2.0, 3.0, 0.0],
              [1.0, 0.0, 1.0]])

b = np.array([1.0, 2.0, 3.0, 4.0])


def test_no_regularization():
    x, x_ols = ie_tikhonov(A, b)
    expected = np.linalg.solve(A.T @ A, A.T @ b)
    lstsq = np.linalg.lstsq(A, b, rcond=None)[0]
    assert np.allclose(x, expected)
    assert np.allclose(x_ols, lstsq)


def test_minnorm():
    lam = 0.2
    x, _ = ie_tikhonov(A, b, minnorm=lam)
    expected = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ b)
    assert np.allclose(x, expected)


def test_smoothness():
    lam = 0.3
    D2 = np.diff(np.eye(A.shape[1]), 2, axis=0)
    x, _ = ie_tikhonov(A, b, smoothness=lam)
    expected = np.linalg.solve(A.T @ A + lam * (D2.T @ D2), A.T @ b)
    assert np.allclose(x, expected)
