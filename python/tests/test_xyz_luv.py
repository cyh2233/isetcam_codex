import numpy as np

from isetcam import xyz_to_uv, xyz_to_luv

WHITEPOINT = np.array([0.95047, 1.0, 1.08883])


def _expected_xyz_to_uv(xyz, mode="uvprime"):
    xw = xyz.reshape(-1, 3)
    B = xw[:, 0] + 15 * xw[:, 1] + 3 * xw[:, 2]
    u = np.zeros_like(B)
    v = np.zeros_like(B)
    nz = B > 0
    u[nz] = 4 * xw[nz, 0] / B[nz]
    v[nz] = 9 * xw[nz, 1] / B[nz]
    if mode == "uv":
        v = v / 1.5
    uv = np.stack([u, v], axis=1)
    return uv.reshape(xyz.shape[:-1] + (2,))


def _expected_y_to_lstar(Y, Yn):
    T = Y / Yn
    L = 116 * np.cbrt(T) - 16
    mask = T < 0.008856
    L[mask] = 903.3 * T[mask]
    return L


def _expected_xyz_to_luv(xyz, wp):
    L = _expected_y_to_lstar(xyz[..., 1], wp[1])
    uv = _expected_xyz_to_uv(xyz)
    un, vn = _expected_xyz_to_uv(wp.reshape(1, 3)).reshape(2)
    U = 13 * L * (uv[..., 0] - un)
    V = 13 * L * (uv[..., 1] - vn)
    return np.stack([L, U, V], axis=-1)


def _expected_luv_to_xyz(luv, wp):
    L = luv[..., 0]
    un, vn = _expected_xyz_to_uv(wp.reshape(1, 3)).reshape(2)
    Y = ((L + 16) / 116) ** 3 * wp[1]
    mask = L <= 8
    Y[mask] = wp[1] * L[mask] / 903.3
    u = luv[..., 1] / (13 * L) + un
    v = luv[..., 2] / (13 * L) + vn
    B = 9 * Y / v
    X = u * B / 4
    Z = (B - X - 15 * Y) / 3
    return np.stack([X, Y, Z], axis=-1)


def test_xyz_to_uv():
    xyz = np.random.rand(5, 3)
    uv = xyz_to_uv(xyz)
    expected = _expected_xyz_to_uv(xyz)
    assert np.allclose(uv, expected)


def test_xyz_luv_round_trip_xw():
    xyz = np.random.rand(10, 3)
    luv = xyz_to_luv(xyz, WHITEPOINT)
    xyz2 = _expected_luv_to_xyz(luv, WHITEPOINT)
    assert np.allclose(xyz2, xyz, atol=1e-6)


def test_xyz_luv_round_trip_rgb():
    xyz = np.random.rand(4, 5, 3)
    luv = xyz_to_luv(xyz, WHITEPOINT)
    xyz2 = _expected_luv_to_xyz(luv, WHITEPOINT)
    assert np.allclose(xyz2, xyz, atol=1e-6)
