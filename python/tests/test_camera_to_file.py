import numpy as np
import scipy.io

from isetcam.sensor import Sensor
from isetcam.opticalimage import OpticalImage
from isetcam.camera import Camera, camera_to_file


def test_camera_to_file_nested(tmp_path):
    sensor = Sensor(volts=np.ones((2, 2)), exposure_time=0.1, wave=np.array([500, 600]), name="s")
    oi = OpticalImage(photons=np.ones((2, 2, 2)), wave=np.array([500, 600]), name="oi")
    cam = Camera(sensor=sensor, optical_image=oi, name="cam")
    path = tmp_path / "cam.mat"
    camera_to_file(cam, path)

    mat = scipy.io.loadmat(path, squeeze_me=True, struct_as_record=False)
    assert "camera" in mat
    saved = mat["camera"]
    assert np.allclose(saved.sensor.volts, sensor.volts)
    assert np.array_equal(saved.sensor.wave.reshape(-1), sensor.wave)
    assert np.allclose(saved.optical_image.photons, oi.photons)
    assert saved.name == "cam"
