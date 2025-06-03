import numpy as np
from isetcam import ie_init
from isetcam.scene import scene_create
from isetcam.camera import camera_create, camera_compute
from isetcam.sensor import sensor_create
from isetcam.ip import ip_demosaic


def main():
    ie_init()
    scene = scene_create("macbeth d65")
    cam = camera_create(sensor_create())
    camera_compute(cam, scene)
    mosaic = cam.sensor.volts
    pattern = getattr(cam.sensor, "filter_color_letters", "rggb")
    rgb_bilinear = ip_demosaic(mosaic, pattern, method="bilinear")
    rgb_nn = ip_demosaic(mosaic, pattern, method="nearest")
    return rgb_bilinear.shape, rgb_nn.shape


if __name__ == "__main__":
    main()
