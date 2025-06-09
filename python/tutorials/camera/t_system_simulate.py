import numpy as np
from isetcam import ie_init, data_path
from isetcam.scene import (
    scene_create,
    scene_adjust_illuminant,
    scene_adjust_luminance,
    scene_show_image,
    scene_slanted_bar,
)
from isetcam.optics import optics_create, optics_set
from isetcam.opticalimage import oi_compute, oi_show_image
from isetcam.sensor import (
    Sensor,
    sensor_create,
    sensor_set,
    sensor_compute,
    sensor_add_noise,
    sensor_gain_offset,
    sensor_show_image,
)
from isetcam.display import display_create
from isetcam.ip import ip_compute, ip_set, ip_plot
from isetcam.metrics import iso12233_sfr


def build_sensor(rows: int, cols: int) -> Sensor:
    """Create and configure a simple Bayer sensor."""
    sensor = sensor_create()
    sensor.volts = np.zeros((rows, cols), dtype=float)
    sensor.pixel_size = 2.2e-6
    sensor.fill_factor = 0.45
    sensor_set(sensor, "gain_sd", 22.18)
    sensor_set(sensor, "offset_sd", 0.0010)
    return sensor


def main() -> None:
    ie_init()

    wave = np.arange(400, 711, 5)

    scene = scene_create("macbeth d65", patch_size=64, wave=wave)
    scene = scene_adjust_illuminant(scene, data_path("lights/Tungsten.mat"))
    scene = scene_adjust_luminance(scene, "mean", 200.0)
    scene.fov = 26.5
    scene_show_image(scene)

    optics = optics_create()
    optics_set(optics, "f_number", 4.0)
    optics_set(optics, "off axis method", "cos4th")
    optics_set(optics, "f_length", 3e-3)

    oi = oi_compute(scene, optics)

    sensor = build_sensor(466, 642)
    sensor = sensor_compute(sensor, oi)
    sensor_add_noise(sensor)
    sensor_gain_offset(sensor, gain=1.0, offset=0.0)
    disp = display_create(wave=sensor.wave)
    sensor_show_image(sensor, disp)
    oi_show_image(oi, disp)
    ip = ip_compute(sensor, disp)
    ip_plot(ip, kind="image")

    ip2 = ip_compute(sensor, disp)
    ip_set(ip2, "internalCS", "XYZ")
    ip_set(ip2, "conversion method sensor", "MCC Optimized")
    ip_set(ip2, "illuminant correction method", "Gray World")
    ip_plot(ip2, kind="image")

    bar_scene = scene_slanted_bar()
    bar_oi = oi_compute(bar_scene, optics)
    bar_sensor = build_sensor(512, 512)
    bar_sensor = sensor_compute(bar_sensor, bar_oi)
    disp.wave = bar_sensor.wave
    bar_ip = ip_compute(bar_sensor, disp)
    freq, mtf = iso12233_sfr(bar_ip.rgb)
    print("ISO12233 SFR frequencies:", freq)
    print("ISO12233 SFR values:", mtf)


if __name__ == "__main__":
    main()
