import numpy as np
from pathlib import Path
from scipy.io import loadmat

from isetcam import ie_color_transform
from isetcam.illuminant import illuminant_create


def synthetic_sensor_qe(wave):
    r = np.exp(-0.5 * ((wave - 650) / 20) ** 2)
    g = np.exp(-0.5 * ((wave - 550) / 20) ** 2)
    b = np.exp(-0.5 * ((wave - 450) / 20) ** 2)
    return np.stack([r, g, b], axis=1)


def _interp(src_wave, data, wave):
    out = np.zeros((len(wave), data.shape[1]))
    for i in range(data.shape[1]):
        out[:, i] = np.interp(wave, src_wave, data[:, i], left=0.0, right=0.0)
    return out


def test_ie_color_transform_xyz():
    wave = np.arange(400, 701, 10)
    sensor_qe = synthetic_sensor_qe(wave)
    illum = illuminant_create("D65", wave).spd
    T = ie_color_transform(sensor_qe, wave, "XYZ", illum)
    assert T.shape == (3, 3)

    root = Path(__file__).resolve().parents[2]
    sur = loadmat(root / "data" / "surfaces" / "reflectances" / "macbethChart.mat")
    sur_ref = _interp(sur["wavelength"].ravel(), sur["data"], wave)
    cmf = loadmat(root / "data" / "human" / "XYZ.mat")
    xyz = _interp(cmf["wavelength"].ravel(), cmf["data"], wave)
    sensor_resp = (sensor_qe.T @ (illum[:, None] * sur_ref)).T
    target_resp = (xyz.T @ (illum[:, None] * sur_ref)).T
    pred = sensor_resp @ T
    err = np.linalg.norm(pred - target_resp) / np.linalg.norm(target_resp)
    assert err < 0.3


def test_ie_color_transform_srgb():
    wave = np.arange(400, 701, 10)
    sensor_qe = synthetic_sensor_qe(wave)
    illum = illuminant_create("D65", wave).spd
    T = ie_color_transform(sensor_qe, wave, "srgb", illum)
    assert T.shape == (3, 3)
