import numpy as np
from isetcam import ie_init
from isetcam.scene import scene_create, scene_show_image
from isetcam.camera import camera_create, camera_compute, camera_show
from isetcam.sensor import sensor_show_image
from isetcam.display import display_create
from isetcam.ip import ip_compute


def main() -> None:
    """Simple camera creation and computation example."""
    ie_init()

    # Build a default scene and camera
    scene = scene_create("macbeth d65")
    scene_show_image(scene)

    cam = camera_create()

    # Run the basic pipeline
    camera_compute(cam, scene)

    # Render an sRGB image for display
    disp = display_create(wave=cam.sensor.wave)
    ip = ip_compute(cam.sensor, disp)
    cam.ip = ip

    # Visualize results
    camera_show(cam, "ip")
    sensor_show_image(cam.sensor, disp)


if __name__ == "__main__":
    main()
