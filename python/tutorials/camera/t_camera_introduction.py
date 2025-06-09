import numpy as np
from isetcam import ie_init
from isetcam.scene import scene_create, scene_show_image
from isetcam.camera import camera_create, camera_compute, camera_get, camera_set
from isetcam.optics import optics_set
from isetcam.opticalimage import oi_show_image
from isetcam.sensor import sensor_show_image
from isetcam.display import display_create
from isetcam.ip import ip_compute, ip_set, ip_plot


def main() -> None:
    ie_init()

    # Create a camera with default optics and sensor
    cam = camera_create()

    # Create a simple Macbeth chart scene and set the field of view
    scene = scene_create("macbeth d65")
    scene.fov = 8.0
    scene_show_image(scene)

    # Compute the camera output from the scene
    camera_compute(cam, scene)

    # Visualize the intermediate objects
    disp = display_create(wave=cam.sensor.wave)
    oi_show_image(camera_get(cam, "oi"), disp)
    sensor_show_image(camera_get(cam, "sensor"), disp)

    # Render to an sRGB image using the same display model
    ip = ip_compute(cam.sensor, disp)
    ip_plot(ip, kind="image")

    # Retrieve the processed sRGB data from the VCImage
    srgb = ip.rgb
    _ = srgb  # placeholder to mimic the MATLAB tutorial

    # A shorter way using camera_get to obtain the sensor
    sensor = camera_get(cam, "sensor")
    ip2 = ip_compute(sensor, disp)
    srgb2 = ip2.rgb
    _ = srgb2

    # Modify an optics parameter using camera_set
    optics_set(cam.optics, "f_number", 16.0)
    camera_compute(cam, scene)
    ip3 = ip_compute(cam.sensor, disp)
    ip_plot(ip3, kind="image")

    # Adjust an IP parameter and recompute
    ip_set(ip3, "illuminant correction method", "gray world")
    ip4 = ip_compute(cam.sensor, disp)
    ip_plot(ip4, kind="image")

    # Re-run the pipeline starting from different stages
    camera_compute(cam, scene)
    camera_compute(cam, "oi")
    camera_compute(cam, "sensor")

    # Final display of the result
    ip_final = ip_compute(cam.sensor, disp)
    ip_plot(ip_final, kind="image")


if __name__ == "__main__":
    main()
