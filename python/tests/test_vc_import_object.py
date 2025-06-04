import numpy as np
import scipy.io
from dataclasses import asdict

from isetcam import vc_import_object
from isetcam.sensor import Sensor


def test_vc_import_object_sensor(tmp_path):
    s = Sensor(
        volts=np.array([[1.0, 2.0]]),
        exposure_time=0.01,
        wave=np.array([500, 600]),
        name="demo",
    )
    path = tmp_path / "sensor.mat"
    scipy.io.savemat(path, {"sensor": asdict(s)})

    loaded = vc_import_object("sensor", path)
    assert np.allclose(loaded.volts, s.volts)
    assert loaded.exposure_time == s.exposure_time
    assert np.array_equal(loaded.wave, s.wave)
