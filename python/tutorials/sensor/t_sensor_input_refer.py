import numpy as np
from isetcam import ie_init
from isetcam.vc_constants import vc_constants
from isetcam.scene import scene_create, scene_adjust_luminance
from isetcam.optics import optics_create
from isetcam.opticalimage import oi_compute, oi_get
from isetcam.sensor import sensor_create, sensor_compute, sensor_set


def main():
    """Relate scene luminance to photon absorptions."""
    ie_init()

    target = 3.0
    scene = scene_create("uniform monochromatic", wavelength=550, size=64)
    scene = scene_adjust_luminance(scene, "mean", 1.0)
    optics = optics_create()
    oi = oi_compute(scene, optics)

    sensor = sensor_create()
    sensor.volts = np.zeros(oi.photons.shape[:2], dtype=float)
    sensor_set(sensor, "exposure_time", 1.0)
    sensor = sensor_compute(sensor, oi)
    electrons = sensor.volts.mean()

    new_lum = 1.0 * (target / electrons)
    scene = scene_adjust_luminance(scene, "mean", new_lum)
    oi = oi_compute(scene, optics)
    lum_img = oi_get(oi, "luminance")
    ill = float(lum_img.mean())
    sensor = sensor_compute(sensor, oi)
    electrons_new = sensor.volts.mean()

    q = vc_constants("q")
    return electrons, new_lum, electrons_new, ill, q


if __name__ == "__main__":
    main()
