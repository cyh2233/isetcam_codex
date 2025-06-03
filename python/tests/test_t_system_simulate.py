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
    path = base / "tutorials" / "camera" / "t_system_simulate.py"

    import isetcam
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

    # Provide missing symbols expected by the tutorial
    isetcam.scene_create = scene_create
    isetcam.scene_adjust_illuminant = scene_adjust_illuminant
    isetcam.scene_adjust_luminance = scene_adjust_luminance
    isetcam.scene_show_image = scene_show_image
    isetcam.optics_create = optics_create
    isetcam.optics_set = optics_set
    isetcam.oi_compute = oi_compute
    isetcam.oi_show_image = oi_show_image
    isetcam.sensor_create = sensor_create
    isetcam.sensor_set = sensor_set
    isetcam.sensor_compute = sensor_compute
    isetcam.sensor_add_noise = sensor_add_noise
    isetcam.sensor_gain_offset = sensor_gain_offset
    isetcam.sensor_show_image = sensor_show_image
    isetcam.display_create = display_create
    isetcam.ip_compute = ip_compute
    isetcam.ip_set = ip_set
    isetcam.ip_plot = ip_plot
    isetcam.scene_slanted_bar = scene_slanted_bar
    isetcam.iso12233_sfr = iso12233_sfr
    spec = importlib.util.spec_from_file_location("t_system_simulate", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.skipif(not _mpl_available(), reason="matplotlib not installed")
def test_t_system_simulate_pipeline():
    tut = _load_tutorial()

    tut.ie_init()
    wave = np.arange(400, 711, 5)
    scene = tut.scene_create("macbeth d65", patch_size=64, wave=wave)
    scene = tut.scene_adjust_illuminant(scene, tut.data_path("lights/Tungsten.mat"))
    scene = tut.scene_adjust_luminance(scene, "mean", 200.0)
    scene.fov = 26.5

    optics = tut.optics_create()
    tut.optics_set(optics, "f_number", 4.0)
    tut.optics_set(optics, "off axis method", "cos4th")
    tut.optics_set(optics, "f_length", 3e-3)

    oi = tut.oi_compute(scene, optics)

    sensor = tut.build_sensor(466, 642)
    disp = tut.display_create()
    disp.wave = sensor.wave

    ip2 = tut.ip_compute(sensor, disp)
    assert ip2.rgb.shape == (466, 642, 3)

    bar_scene = tut.scene_slanted_bar()
    bar_img = bar_scene.photons.sum(axis=2)
    freq, mtf = tut.iso12233_sfr(bar_img)

    assert freq.shape == mtf.shape
    assert np.all(np.isfinite(freq))
    assert np.all(np.isfinite(mtf))
