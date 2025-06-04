from isetcam import ie_init
from isetcam.scene import scene_create
from isetcam.optics import optics_create
from isetcam.opticalimage import oi_compute
from isetcam.sensor import sensor_create, sensor_compute
from isetcam.display import display_create
from isetcam.ip import ip_compute


def main():
    """Demonstrate a basic ISETCam pipeline."""
    ie_init()

    # Create a simple scene
    scene = scene_create("macbeth d65")

    # Form the optical image using default optics
    optics = optics_create()
    oi = oi_compute(scene, optics)

    # Generate sensor data
    sensor = sensor_create()
    sensor = sensor_compute(sensor, oi)

    # Render to an sRGB image using a default display
    disp = display_create()
    disp.wave = sensor.wave
    ip = ip_compute(sensor, disp)

    return scene.photons.shape, oi.photons.shape, sensor.volts.shape, ip.rgb.shape


if __name__ == "__main__":
    main()
