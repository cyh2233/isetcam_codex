import numpy as np

from isetcam.sensor import Sensor, sensor_set_size_to_fov
from isetcam.opticalimage import OpticalImage
from isetcam.optics import Optics


def _sensor():
    s = Sensor(volts=np.zeros((4, 4)), wave=np.array([550]), exposure_time=0.01)
    s.pixel_size = 1e-6
    s.filter_color_letters = "rggb"
    return s


def _oi():
    oi = OpticalImage(photons=np.zeros((1, 1, 1)), wave=np.array([550]))
    oi.optics = Optics(f_number=4.0, f_length=1e-3, wave=oi.wave)
    return oi


def test_sensor_set_size_to_fov_scalar():
    s = _sensor()
    oi = _oi()
    s.data = "cache"
    sensor_set_size_to_fov(s, 0.45836379150820084, oi)
    assert s.volts.shape == (8, 8)
    assert not hasattr(s, "data")


def test_sensor_set_size_to_fov_vector_and_cfa():
    s = _sensor()
    oi = _oi()
    sensor_set_size_to_fov(
        s,
        (0.28647830073661307, 0.22918281247557193),
        oi,
    )
    assert s.volts.shape == (4, 6)
