# mypy: ignore-errors
"""Color space transformation matrices and data-driven fitting."""

from __future__ import annotations

import numpy as np

from .ie_param_format import ie_param_format


# Predefined 3x3 matrices in row-vector form
_LMS2OPP = np.array([
    [0.9900, -0.6690, -0.2120],
    [-0.1060, 0.7420, -0.3540],
    [-0.0940, -0.0270, 0.9110],
])
_OPP2LMS = np.linalg.inv(
    np.array([
        [0.9900, -0.1060, -0.0940],
        [-0.6690, 0.7420, -0.0270],
        [-0.2120, -0.3540, 0.9110],
    ])
).T
_HPE2XYZ = np.linalg.inv(
    np.array([
        [0.4002, 0.7076, -0.0808],
        [-0.2263, 1.1653, 0.0457],
        [0.0, 0.0, 0.9182],
    ])
).T
_XYZ2HPE = np.array([
    [0.4002, -0.2263, 0.0],
    [0.7076, 1.1653, 0.0],
    [-0.0808, 0.0457, 0.9182],
])
_XYZ2STO = np.array([
    [0.2689, -0.3962, 0.0214],
    [0.8518, 1.1770, -0.0247],
    [-0.0358, 0.1055, 0.5404],
])
_STO2XYZ = np.array([
    [1.7910, 0.6068, -0.0432],
    [-1.2884, 0.4097, 0.0697],
    [0.3702, -0.0398, 1.8340],
])
_XYZ2OPP_10 = np.array([
    [0.2885613, -0.4648864, 0.0798787],
    [0.6597617, 0.3262702, -0.5547976],
    [-0.1305654, 0.0624200, 0.4814746],
])
_OPP2XYZ_10 = np.linalg.inv(_XYZ2OPP_10).T
_XYZ2OPP_2 = np.array([
    [0.2787336, -0.4487736, 0.0859513],
    [0.7218031, 0.2898056, -0.5899859],
    [-0.1065520, 0.0771569, 0.5011089],
])
_OPP2XYZ_2 = np.linalg.inv(_XYZ2OPP_2).T
_XYZ2YIQ = np.array([
    [0.0, 1.4070, 0.9320],
    [1.0, -0.8420, -1.1890],
    [0.0, -0.4510, 0.2330],
])
_YIQ2XYZ = np.linalg.inv(
    np.array([
        [0.0, 1.0, 0.0],
        [1.4070, -0.8420, -0.4510],
        [0.9320, -1.1890, 0.2330],
    ])
).T
_RGB2YUV = np.array([
    [0.2990, -0.1687, 0.5000],
    [0.5870, -0.3313, -0.4187],
    [0.1140, 0.5000, -0.0813],
])
_YUV2RGB = np.linalg.inv(
    np.array([
        [0.2990, 0.5870, 0.1140],
        [-0.1687, -0.3313, 0.5000],
        [0.5000, -0.4187, -0.0813],
    ])
).T
_XYZ2SRGB = np.array([
    [3.2410, -0.9692, 0.0556],
    [-1.5374, 1.8760, -0.2040],
    [-0.4986, 0.0416, 1.0570],
])
_SRGB2XYZ = np.linalg.inv(
    np.array([
        [3.2410, -1.5374, -0.4986],
        [-0.9692, 1.8760, 0.0416],
        [0.0556, -0.2040, 1.0570],
    ])
).T
_CMY2RGB = np.array([
    [0.0, 1.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 1.0, 0.0],
])


def _matrix_from_name(matrixtype: str, spacetype: int | None) -> np.ndarray:
    """Return predefined transformation matrix."""
    key = ie_param_format(matrixtype)
    if key in {"lms2opp"}:
        return _LMS2OPP
    if key in {"opp2lms"}:
        return _OPP2LMS
    if key in {"hpe2xyz"}:
        return _HPE2XYZ
    if key in {"xyz2hpe"}:
        return _XYZ2HPE
    if key in {"xyz2sto", "xyz2stockman", "xyz2lms"}:
        return _XYZ2STO
    if key in {"stockman2xyz", "sto2xyz", "lms2xyz"}:
        return _STO2XYZ
    if key in {"xyz2yiq"}:
        return _XYZ2YIQ
    if key in {"yiq2xyz"}:
        return _YIQ2XYZ
    if key in {"rgb2yuv"}:
        return _RGB2YUV
    if key in {"yuv2rgb"}:
        return _YUV2RGB
    if key in {"xyz2srgb"}:
        return _XYZ2SRGB
    if key in {"srgb2xyz"}:
        return _SRGB2XYZ
    if key in {"xyz2lrgb"}:
        return _XYZ2SRGB
    if key in {"lrgb2xyz"}:
        return _SRGB2XYZ
    if key in {"cmy2rgb", "rgb2cmy"}:
        return _CMY2RGB
    if key in {"xyz2opp", "opp2xyz"}:
        st = 10 if spacetype is None else spacetype
        if st == 2:
            return _XYZ2OPP_2 if key.startswith("xyz") else _OPP2XYZ_2
        if st == 10:
            return _XYZ2OPP_10 if key.startswith("xyz") else _OPP2XYZ_10
        raise ValueError("spacetype must be 2 or 10")
    raise ValueError(f"Unknown matrix type '{matrixtype}'")


def color_transform_matrix(
    matrixtype: str | None = None,
    spacetype: int | None = None,
    src: np.ndarray | None = None,
    dst: np.ndarray | None = None,
    offset: bool = False,
) -> np.ndarray:
    """Return or fit a color transformation matrix.

    When ``src`` and ``dst`` are provided, a least-squares matrix that maps
    ``src`` to ``dst`` is returned. ``src`` and ``dst`` must have the same
    number of rows. If ``offset`` is ``True`` an additional column of ones is
    appended to ``src`` to fit an affine transform.

    Parameters
    ----------
    matrixtype : str, optional
        Name of a predefined transform matching MATLAB's
        ``colorTransformMatrix``. Ignored when ``src`` and ``dst`` are given.
    spacetype : int, optional
        Opponent space type for the ``xyz2opp``/``opp2xyz`` transforms.
    src, dst : np.ndarray, optional
        Training data matrices with shape ``(n_samples, n_channels)``.
    offset : bool, optional
        Fit an affine transform when ``True``. Default ``False``.
    """

    if src is not None or dst is not None:
        if src is None or dst is None:
            raise ValueError("src and dst must both be provided")
        src = np.asarray(src, dtype=float)
        dst = np.asarray(dst, dtype=float)
        if src.shape[0] != dst.shape[0]:
            raise ValueError("src and dst must have the same number of rows")
        X = src
        if offset:
            X = np.hstack([X, np.ones((X.shape[0], 1))])
        T, _, _, _ = np.linalg.lstsq(X, dst, rcond=None)
        return T

    if matrixtype is None:
        raise ValueError("matrixtype required when src/dst not provided")

    return _matrix_from_name(matrixtype, spacetype)
