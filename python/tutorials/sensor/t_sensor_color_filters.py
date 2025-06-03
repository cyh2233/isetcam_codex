import numpy as np
from isetcam import ie_init, data_path, ie_read_color_filter
from isetcam.scene import scene_create
from isetcam.optics import optics_create
from isetcam.opticalimage import oi_compute
from isetcam.sensor import sensor_create, sensor_compute


def main():
    """Demonstrate loading color filters and computing sensor response."""
    ie_init()

    sensor = sensor_create()
    wave = sensor.wave
    filt_path = data_path("sensor/colorfilters/RGB.mat")
    spectra, names, _ = ie_read_color_filter(filt_path, wave)
    sensor.filter_spectra = spectra
    sensor.filter_names = names

    scene = scene_create("uniform monochromatic", wavelength=550, size=64)
    scene.fov = 2.0
    optics = optics_create()
    oi = oi_compute(scene, optics)
    sensor.volts = np.zeros(oi.photons.shape[:2], dtype=float)
    sensor = sensor_compute(sensor, oi)

    return sensor.filter_spectra.shape, sensor.filter_names, sensor.volts.mean()


if __name__ == "__main__":
    main()
