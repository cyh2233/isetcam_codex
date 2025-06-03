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
    path = base / "tutorials" / "camera" / "t_camera_compute.py"

    import isetcam
    from isetcam.scene import scene_create, scene_show_image
    from isetcam.camera import camera_create, camera_compute, camera_show
    from isetcam.display import display_create
    from isetcam.ip import ip_compute

    isetcam.scene_create = scene_create
    isetcam.scene_show_image = scene_show_image
    isetcam.camera_create = camera_create
    isetcam.camera_compute = camera_compute
    isetcam.camera_show = camera_show
    isetcam.display_create = display_create
    isetcam.ip_compute = ip_compute

    import importlib.util

    spec = importlib.util.spec_from_file_location("t_camera_compute", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.skipif(not _mpl_available(), reason="matplotlib not installed")
def test_t_camera_compute_pipeline():
    tut = _load_tutorial()

    tut.ie_init()
    scene = tut.scene_create("macbeth d65")
    cam = tut.camera_create()
    tut.camera_compute(cam, scene)

    disp = tut.display_create()
    disp.wave = cam.sensor.wave
    ip = tut.ip_compute(cam.sensor, disp)
    cam.ip = ip

    assert ip.rgb.shape == (scene.photons.shape[0], scene.photons.shape[1], 3)
