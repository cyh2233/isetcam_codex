import numpy as np
from isetcam import ie_init
from isetcam.scene import scene_create, scene_set
from isetcam.optics import optics_create, optics_set
from isetcam.opticalimage import (
    oi_compute,
    oi_get,
    oi_set,
    oi_plot,
)


def main():
    ie_init()

    scene = scene_create("gridlines", size=256, spacing=64)

    optics = optics_create()
    oi = oi_compute(scene, optics)
    oi_set(oi, "name", "Small f number")

    fn_small = oi_get(oi, "optics f number")

    optics_big = optics_create()
    optics_set(optics_big, "f_number", fn_small * 3)
    oi_big = oi_compute(scene, optics_big)
    oi_set(oi_big, "name", "Big f number")


    return fn_small, oi_get(oi_big, "optics f number")


if __name__ == "__main__":
    main()
