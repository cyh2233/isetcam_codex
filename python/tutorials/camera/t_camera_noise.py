import numpy as np
from isetcam import ie_init, data_path
from isetcam.scene import scene_from_file, scene_adjust_luminance, scene_show_image
from isetcam.camera import camera_create, camera_compute
from isetcam.optics import optics_set
from isetcam.display import display_create
from isetcam.ip import ip_compute
from isetcam.sensor import (
    sensor_set,
    sensor_photon_noise,
)


def main() -> None:
    """Demonstrate sensor noise effects using the camera pipeline."""
    ie_init()

    cam = camera_create()
    optics_set(cam.optics, "f_number", 2)

    # Load a face image scene
    fpath = data_path("images/faces/faceMale.jpg")
    scene = scene_from_file(fpath, wave=np.array([450, 550, 650]))
    scene_show_image(scene)

    # Ensure sensor wave matches the scene
    cam.sensor.wave = scene.wave
    cam.sensor.qe = np.ones_like(scene.wave, dtype=float)

    # ----- No noise -----
    sensor_set(cam.sensor, "gain_sd", 0)
    sensor_set(cam.sensor, "offset_sd", 0)
    cam.sensor.exposure_time = 0.01
    camera_compute(cam, scene)

    disp = display_create(wave=cam.sensor.wave)
    ip_no = ip_compute(cam.sensor, disp)
    ip_no.name = "No noise"

    # ----- Photon noise only -----
    sensor_set(cam.sensor, "gain_sd", 0)
    sensor_set(cam.sensor, "offset_sd", 0)
    scene_low = scene_adjust_luminance(scene, "mean", 5)
    camera_compute(cam, scene_low)
    sensor_photon_noise(cam.sensor)
    ip_photon = ip_compute(cam.sensor, disp)
    ip_photon.name = "Photon noise"

    # ----- All noise -----
    sensor_set(cam.sensor, "gain_sd", 5)
    sensor_set(cam.sensor, "offset_sd", 0.01)
    scene_high = scene_adjust_luminance(scene, "mean", 100)
    camera_compute(cam, scene_high)
    sensor_photon_noise(cam.sensor)
    ip_all = ip_compute(cam.sensor, disp)
    ip_all.name = "All noise"

    _ = (ip_no, ip_photon, ip_all)


if __name__ == "__main__":
    main()
