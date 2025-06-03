import numpy as np
from isetcam import ie_init
from isetcam.scene import scene_create
from isetcam.camera import camera_create, camera_compute
from isetcam.sensor import sensor_create
from isetcam.display import display_create
from isetcam.ip import ip_compute


def main():
    ie_init()
    scene = scene_create("macbeth tungsten")
    cam = camera_create(sensor_create())
    cam.sensor.volts = np.zeros((340, 420), dtype=float)
    camera_compute(cam, scene)

    disp = display_create()
    disp.wave = cam.sensor.wave
    ip = ip_compute(cam.sensor, disp)
    return ip.rgb.shape


if __name__ == "__main__":
    main()
