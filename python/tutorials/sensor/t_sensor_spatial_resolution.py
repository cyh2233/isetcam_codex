import numpy as np
from isetcam import ie_init
from isetcam.scene import scene_create
from isetcam.optics import optics_create
from isetcam.opticalimage import oi_compute
from isetcam.sensor import sensor_create, sensor_compute


def main():
    """Show effect of pixel size on spatial aliasing."""
    ie_init()

    scene = scene_create("frequency sweep", size=256)
    scene.fov = 1.0
    optics = optics_create()
    oi = oi_compute(scene, optics)

    coarse = sensor_create()
    coarse.pixel_size = 6e-6
    coarse.volts = np.zeros(oi.photons.shape[:2], dtype=float)
    coarse = sensor_compute(coarse, oi)

    fine = sensor_create()
    fine.pixel_size = 2e-6
    fine.volts = np.zeros(oi.photons.shape[:2], dtype=float)
    fine = sensor_compute(fine, oi)

    return coarse.volts.shape, fine.volts.shape


if __name__ == "__main__":
    main()
