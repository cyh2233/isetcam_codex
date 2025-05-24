import numpy as np

from isetcam import init_default_spectrum
from isetcam.scene import Scene
from isetcam.sensor import Sensor
from isetcam.opticalimage import OpticalImage


def test_default_multispectral():
    obj = Scene(photons=np.zeros((1, 1, 31)), wave=None)
    init_default_spectrum(obj)
    assert np.array_equal(obj.wave, np.arange(400, 701, 10))


def test_default_monochrome():
    obj = Sensor(volts=np.zeros((1, 1, 1)), wave=None, exposure_time=0.0)
    init_default_spectrum(obj, spectral_type="monochrome")
    assert np.array_equal(obj.wave, np.array([550.0]))


def test_custom_wave():
    custom = np.array([450, 550, 650])
    obj = OpticalImage(photons=np.zeros((1, 1, 3)), wave=None)
    init_default_spectrum(obj, spectral_type="custom", wave=custom)
    assert np.array_equal(obj.wave, custom)
