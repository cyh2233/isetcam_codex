import numpy as np
from scipy.io import loadmat

from isetcam.sensor import Sensor, sensor_ccm
from isetcam.data_path import data_path


def _make_sensor(patch_size: int, transform: np.ndarray) -> tuple[Sensor, np.ndarray, np.ndarray, np.ndarray]:
    mat = loadmat(data_path("surfaces/charts/macbethChartLinearRGB.mat"))
    ideal = mat["mcc"][0, 0]["lrgbValuesMCC"].astype(float)
    meas = ideal @ transform
    h = patch_size * 4
    w = patch_size * 6
    volts = np.zeros((h, w, 3), dtype=float)
    idx = 0
    for r in range(4):
        for c in range(6):
            patch = meas[idx]
            volts[r*patch_size:(r+1)*patch_size, c*patch_size:(c+1)*patch_size, :] = patch
            idx += 1
    sensor = Sensor(volts=volts, wave=np.array([550]), exposure_time=0.01)
    corners = np.array([[0, h], [w, h], [w, 0], [0, 0]], dtype=float)
    return sensor, corners, ideal, meas


def test_sensor_ccm_macbeth():
    A = np.array(
        [
            [0.6, 0.2, 0.1],
            [0.0, 1.1, 0.1],
            [0.2, 0.1, 0.9],
        ],
        dtype=float,
    )
    sensor, cp, ideal, meas = _make_sensor(8, A)
    L = sensor_ccm(sensor, cp)
    assert L.shape == (3, 3)
    pred = meas @ L
    assert np.allclose(pred, ideal, atol=1e-6)
