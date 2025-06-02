import numpy as np
from scipy.io import loadmat

from isetcam.sensor import Sensor
from isetcam.metrics import iso_speed_saturation
from isetcam.illuminant import illuminant_create
from isetcam.energy_to_quanta import energy_to_quanta
from isetcam.quanta2energy import quanta_to_energy
from isetcam.data_path import data_path


def _expected_illuminance(wave, photons):
    energy = quanta_to_energy(wave, photons)
    mat = loadmat(data_path("human/luminosity.mat"))
    V = np.interp(wave, mat["wavelength"].ravel(), mat["data"].ravel(), left=0.0, right=0.0)
    bw = wave[1] - wave[0] if len(wave) > 1 else 10
    xw = energy.reshape(-1, len(wave))
    lum = 683 * xw.dot(V) * bw
    return lum.reshape(1, 1)


def _expected_iso(sensor):
    wave = sensor.wave
    ill = illuminant_create("D65", wave)
    photons = energy_to_quanta(wave, ill.spd)
    qe = getattr(sensor, "qe", np.ones_like(wave))
    electrons = np.sum(photons * qe) * sensor.exposure_time
    lux = float(_expected_illuminance(wave, photons))
    lux_sec = lux * sensor.exposure_time
    sat = lux_sec * (sensor.well_capacity / electrons)
    return 10.0 / ((sat / np.sqrt(2.0)) * 0.14)


def test_iso_speed_saturation_single_channel():
    wave = np.array([550.0])
    s = Sensor(volts=np.zeros((1,)), wave=wave, exposure_time=0.01)
    s.well_capacity = 5000.0
    s.qe = np.array([1.0])
    iso = iso_speed_saturation(s)
    exp_iso = _expected_iso(s)
    assert np.isclose(iso, exp_iso)


def test_iso_speed_saturation_multi_channel():
    wave = np.array([500.0, 510.0, 520.0])
    s = Sensor(volts=np.zeros((1,)), wave=wave, exposure_time=0.02)
    s.well_capacity = 10000.0
    s.qe = np.array([0.3, 0.5, 0.9])
    iso = iso_speed_saturation(s)
    exp_iso = _expected_iso(s)
    assert np.isclose(iso, exp_iso)

