from pathlib import Path
import sys
import numpy as np
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
    path = base / "tutorials" / "camera" / "t_camera_noise.py"

    import isetcam
    from isetcam.scene import scene_from_file, scene_adjust_luminance, scene_show_image
    from isetcam.camera import camera_create, camera_compute
    from isetcam.optics import optics_set
    from isetcam.display import display_create
    from isetcam.ip import ip_compute
    from isetcam.sensor import sensor_set, sensor_photon_noise
    from isetcam import data_path

    isetcam.scene_from_file = scene_from_file
    isetcam.scene_adjust_luminance = scene_adjust_luminance
    isetcam.scene_show_image = scene_show_image
    isetcam.camera_create = camera_create
    isetcam.camera_compute = camera_compute
    isetcam.optics_set = optics_set
    isetcam.display_create = display_create
    isetcam.ip_compute = ip_compute
    isetcam.sensor_set = sensor_set
    isetcam.sensor_photon_noise = sensor_photon_noise
    isetcam.data_path = data_path

    import importlib.util

    spec = importlib.util.spec_from_file_location("t_camera_noise", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.skipif(not _mpl_available(), reason="matplotlib not installed")
def test_t_camera_noise_pipeline():
    tut = _load_tutorial()

    tut.ie_init()
    cam = tut.camera_create()
    tut.optics_set(cam.optics, "f_number", 2)

    fpath = tut.data_path("images/faces/faceMale.jpg")
    scene = tut.scene_from_file(fpath, wave=np.array([450, 550, 650]))

    cam.sensor.wave = scene.wave
    cam.sensor.qe = np.ones_like(scene.wave, dtype=float)

    tut.sensor_set(cam.sensor, "gain_sd", 0)
    tut.sensor_set(cam.sensor, "offset_sd", 0)
    cam.sensor.exposure_time = 0.01
    tut.camera_compute(cam, scene)

    disp = tut.display_create()
    disp.wave = cam.sensor.wave
    ip_no = tut.ip_compute(cam.sensor, disp)

    tut.sensor_set(cam.sensor, "gain_sd", 0)
    tut.sensor_set(cam.sensor, "offset_sd", 0)
    sc_low = tut.scene_adjust_luminance(scene, "mean", 5)
    tut.camera_compute(cam, sc_low)
    tut.sensor_photon_noise(cam.sensor)
    ip_p = tut.ip_compute(cam.sensor, disp)

    tut.sensor_set(cam.sensor, "gain_sd", 5)
    tut.sensor_set(cam.sensor, "offset_sd", 0.01)
    sc_hi = tut.scene_adjust_luminance(scene, "mean", 100)
    tut.camera_compute(cam, sc_hi)
    tut.sensor_photon_noise(cam.sensor)
    ip_all = tut.ip_compute(cam.sensor, disp)

    assert ip_no.rgb.shape == (scene.photons.shape[0], scene.photons.shape[1], 3)
    assert ip_p.rgb.shape == ip_no.rgb.shape
    assert ip_all.rgb.shape == ip_no.rgb.shape
