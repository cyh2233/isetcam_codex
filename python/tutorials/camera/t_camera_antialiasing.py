from isetcam import ie_init
from isetcam.scene import scene_freq_orient, scene_show_image
from isetcam.optics import optics_create, optics_set
from isetcam.opticalimage import oi_compute, oi_diffuser, oi_birefringent_diffuser
from isetcam.sensor import (
    sensor_create,
    sensor_set_size_to_fov,
    sensor_compute,
    sensor_show_image,
)
from isetcam.display import display_create
from isetcam.ip import ip_compute, ip_plot


def main() -> None:
    """Illustrate the effect of anti-aliasing filters."""
    ie_init()

    # High frequency orientation scene
    scene = scene_freq_orient({"block_size": 64})
    scene.fov = 6.0
    scene_show_image(scene)

    # Diffraction limited optics
    optics = optics_create()
    optics_set(optics, "f_number", 2)
    oi = oi_compute(scene, optics)
    oi.optics = optics

    # High resolution sensor (1.5 micron pixels)
    sensor = sensor_create()
    sensor.pixel_size = 1.5e-6
    sensor = sensor_set_size_to_fov(sensor, 5, oi)
    sensor = sensor_compute(sensor, oi)
    sensor_show_image(sensor)

    disp = display_create()
    disp.wave = sensor.wave
    ip = ip_compute(sensor, disp)
    ip.name = "No anti-aliasing filter"
    ip_plot(ip, kind="image")

    # Gaussian blur anti-aliasing filter
    oi_blur = oi_diffuser(oi, sensor.pixel_size * 1e6, method="gaussian")
    sensor = sensor_compute(sensor, oi_blur)
    ip_blur = ip_compute(sensor, disp)
    ip_blur.name = "Anti-aliasing blur filter"
    ip_plot(ip_blur, kind="image")

    # Birefringent anti-aliasing filter
    oi_bire = oi_birefringent_diffuser(oi, sensor.pixel_size * 1e6)
    sensor = sensor_compute(sensor, oi_bire)
    ip_bire = ip_compute(sensor, disp)
    ip_bire.name = "Anti-aliasing birefringent filter"
    ip_plot(ip_bire, kind="image")


if __name__ == "__main__":
    main()
