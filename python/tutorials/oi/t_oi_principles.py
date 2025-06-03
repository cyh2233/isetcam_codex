from isetcam import ie_init, data_path
from isetcam.scene import scene_from_file, scene_set
from isetcam.optics import optics_create, optics_set
from isetcam.opticalimage import oi_compute, oi_get


def main():
    ie_init()

    img_path = data_path("images/rgb/eagle.jpg")
    scene = scene_from_file(img_path, mean_luminance=100)

    optics = optics_create()
    oi = oi_compute(scene, optics)
    power1 = oi_get(oi, "optics diopters")

    optics_set(optics, "f_length", 0.002)
    oi2 = oi_compute(scene, optics)
    power2 = oi_get(oi2, "optics diopters")

    return power1, power2


if __name__ == "__main__":
    main()
