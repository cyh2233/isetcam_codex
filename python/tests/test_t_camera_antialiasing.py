from pathlib import Path
import sys
import pytest
import matplotlib

matplotlib.use("Agg")


def _mpl_available() -> bool:
    try:
        import matplotlib.pyplot as _

        return True
    except Exception:
        return False


def _load_tutorial():
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "camera" / "t_camera_antialiasing.py"

    import isetcam
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

    isetcam.scene_freq_orient = scene_freq_orient
    isetcam.scene_show_image = scene_show_image
    isetcam.optics_create = optics_create
    isetcam.optics_set = optics_set
    isetcam.oi_compute = oi_compute
    isetcam.oi_diffuser = oi_diffuser
    isetcam.oi_birefringent_diffuser = oi_birefringent_diffuser
    isetcam.sensor_create = sensor_create
    isetcam.sensor_set_size_to_fov = sensor_set_size_to_fov
    isetcam.sensor_compute = sensor_compute
    isetcam.sensor_show_image = sensor_show_image
    isetcam.display_create = display_create
    isetcam.ip_compute = ip_compute
    isetcam.ip_plot = ip_plot

    import importlib.util

    spec = importlib.util.spec_from_file_location("t_camera_antialiasing", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.skipif(not _mpl_available(), reason="matplotlib not installed")
def test_t_camera_antialiasing_pipeline():
    tut = _load_tutorial()

    tut.ie_init()
    scene = tut.scene_freq_orient({"block_size": 64})
    scene.fov = 6.0

    optics = tut.optics_create()
    tut.optics_set(optics, "f_number", 2)
    oi = tut.oi_compute(scene, optics)
    oi.optics = optics

    sensor = tut.sensor_create()
    sensor.pixel_size = 1.5e-6
    sensor = tut.sensor_set_size_to_fov(sensor, 5, oi)
    sensor = tut.sensor_compute(sensor, oi)

    disp = tut.display_create()
    disp.wave = sensor.wave
    ip = tut.ip_compute(sensor, disp)

    oi_blur = tut.oi_diffuser(oi, sensor.pixel_size * 1e6, method="gaussian")
    sensor = tut.sensor_compute(sensor, oi_blur)
    ip_blur = tut.ip_compute(sensor, disp)

    oi_bire = tut.oi_birefringent_diffuser(oi, sensor.pixel_size * 1e6)
    sensor = tut.sensor_compute(sensor, oi_bire)
    ip_bire = tut.ip_compute(sensor, disp)

    assert ip.rgb.shape == (sensor.volts.shape[0], sensor.volts.shape[1], 3)
    assert ip_blur.rgb.shape == ip.rgb.shape
    assert ip_bire.rgb.shape == ip.rgb.shape
