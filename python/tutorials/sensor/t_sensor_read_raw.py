from isetcam import data_path
from isetcam.sensor import sensor_dng_read, sensor_crop
from isetcam.display import display_create
from isetcam.ip import ip_compute


def main():
    """Load a DNG file into a sensor and crop the data."""
    path = data_path("images/rawcamera/MCC-centered.dng")
    sensor = sensor_dng_read(path)
    cropped = sensor_crop(sensor, (500, 1000, 2500, 2500))

    disp = display_create(wave=cropped.wave)
    ip = ip_compute(cropped, disp)
    return cropped.volts.shape, ip.rgb.shape


if __name__ == "__main__":
    main()
