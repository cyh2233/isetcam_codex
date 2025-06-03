import importlib.util
from pathlib import Path
import sys

import numpy as np
import pytest
import matplotlib

matplotlib.use("Agg")


def _mpl_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


def _load_tutorial():
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "camera" / "t_camera_introduction.py"

    import isetcam
    from isetcam.scene import scene_create, scene_show_image
    from isetcam.camera import (
        camera_create,
        camera_compute,
        camera_get,
        camera_set,
    )
    from isetcam.optics import optics_set
    from isetcam.opticalimage import oi_show_image
    from isetcam.sensor import sensor_show_image
    from isetcam.display import display_create
    from isetcam.ip import ip_compute, ip_set, ip_plot

    # Provide missing symbols expected by the tutorial
    isetcam.scene_create = scene_create
    isetcam.scene_show_image = scene_show_image
    isetcam.camera_create = camera_create
    isetcam.camera_compute = camera_compute
    isetcam.camera_get = camera_get
    isetcam.camera_set = camera_set
    isetcam.optics_set = optics_set
    isetcam.oi_show_image = oi_show_image
    isetcam.sensor_show_image = sensor_show_image
    isetcam.display_create = display_create
    isetcam.ip_compute = ip_compute
    isetcam.ip_set = ip_set
    isetcam.ip_plot = ip_plot

    spec = importlib.util.spec_from_file_location("t_camera_introduction", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.skipif(not _mpl_available(), reason="matplotlib not installed")
def test_t_camera_introduction_pipeline():
    tut = _load_tutorial()

    tut.ie_init()
    cam = tut.camera_create()

    scene = tut.scene_create("macbeth d65")
    scene.fov = 8.0

    tut.camera_compute(cam, scene)

    tut.optics_set(cam.optics, "f_number", 16.0)
    tut.camera_compute(cam, scene)

    disp = tut.display_create()
    disp.wave = cam.sensor.wave

    ip = tut.ip_compute(cam.sensor, disp)
    tut.ip_set(ip, "illuminant correction method", "gray world")
    ip_final = tut.ip_compute(cam.sensor, disp)

    assert ip_final.rgb.shape == (scene.photons.shape[0], scene.photons.shape[1], 3)
