import numpy as np
from isetcam import ie_init, data_path, ie_read_color_filter
from isetcam.scene import scene_create
from isetcam.optics import optics_create
from isetcam.opticalimage import oi_compute
from isetcam.sensor import (
    sensor_create,
    sensor_compute,
)
from isetcam.display import display_create
from isetcam.ip import ip_compute, ip_set


def main():
    """Illustrate exposure changes causing color errors when saturated."""
    ie_init()

    scene = scene_create("macbeth d65")
    scene.fov = 8.0
    optics = optics_create()
    oi = oi_compute(scene, optics)

    sensor = sensor_create()
    sensor.volts = np.zeros(oi.photons.shape[:2], dtype=float)

    # Attach RGB color filters and exaggerate green sensitivity
    spec, names, _ = ie_read_color_filter(
        data_path("sensor/colorfilters/RGB.mat"), sensor.wave
    )
    spec[:, 1] *= 1.5
    sensor.filter_spectra = spec
    sensor.filter_names = names
    sensor.auto_exposure = True

    sensor = sensor_compute(sensor, oi)
    exp_time = sensor.exposure_time

    disp = display_create(wave=sensor.wave)
    ip = ip_compute(sensor, disp)
    ip_set(ip, "illuminant correction method", "gray world")
    rgb1 = ip.rgb.mean(axis=(0, 1))

    sensor.auto_exposure = False
    sensor.exposure_time = 3 * exp_time
    sensor = sensor_compute(sensor, oi)
    ip2 = ip_compute(sensor, disp)
    ip_set(ip2, "illuminant correction method", "gray world")
    rgb2 = ip2.rgb.mean(axis=(0, 1))

    return exp_time, rgb1, rgb2


if __name__ == "__main__":
    main()
