import numpy as np
from isetcam import ie_init
from isetcam.scene import scene_create
from isetcam.optics import optics_create
from isetcam.opticalimage import oi_compute
from isetcam.sensor import (
    sensor_create,
    sensor_compute,
    sensor_photon_noise,
    sensor_add_noise,
    sensor_set,
)


def main():
    """Illustrate sensor noise components."""
    ie_init()

    scene = scene_create("uniform monochromatic", wavelength=550, size=128)
    scene.fov = 8.0
    optics = optics_create()
    oi = oi_compute(scene, optics)

    sensor = sensor_create()
    sensor.volts = np.zeros(oi.photons.shape[:2], dtype=float)
    sensor = sensor_compute(sensor, oi)
    base = sensor.volts.copy()

    # Photon noise only
    sensor.volts = base.copy()
    sensor_photon_noise(sensor)
    photon_only = sensor.volts.copy()

    # Photon noise + fixed pattern noise
    sensor.volts = base.copy()
    sensor_set(sensor, "gain_sd", 5.0)
    sensor_set(sensor, "offset_sd", 0.05)
    sensor_photon_noise(sensor)
    sensor_add_noise(sensor)
    fpn = sensor.volts.copy()

    return base.mean(), photon_only.var(), fpn.var()


if __name__ == "__main__":
    main()
