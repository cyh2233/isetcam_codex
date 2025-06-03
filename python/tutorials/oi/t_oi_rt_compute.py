from isetcam import ie_init
from isetcam.scene import scene_create
from isetcam.optics import optics_create
from isetcam.opticalimage import oi_compute, oi_get


def main():
    ie_init()
    scene = scene_create("gridlines")

    optics = optics_create()
    optics.model = "ray trace"
    oi = oi_compute(scene, optics)
    model = oi_get(oi, "optics model")
    return model


if __name__ == "__main__":
    main()
