import numpy as np
from isetcam.cp import CPScene, CPCModule, CPCamera
from isetcam.sensor import sensor_create
from isetcam.optics import optics_create
from isetcam.opticalimage import OpticalImage


def test_take_picture_pbrt_optical_image(monkeypatch):
    from isetcam import cp as cp_pkg

    sensor = sensor_create(wave=np.array([550.0]))
    optics = optics_create()
    module = cp_pkg.CPCModule(sensor=sensor, optics=optics)
    camera = cp_pkg.CPCamera([module])
    scene = cp_pkg.CPScene(scene_type="pbrt", scene_path="dummy")

    def fake_render(self, exp, *, focus_dists=None, render_flags=None):
        assert focus_dists == [2.0]
        assert render_flags == [True]
        oi = OpticalImage(photons=np.ones((1, 1, 1)), wave=np.array([550.0]))
        return [oi]

    monkeypatch.setattr(cp_pkg.cp_scene.CPScene, "render", fake_render, raising=False)

    def fail_oi_compute(*args, **kwargs):
        raise RuntimeError("oi_compute should not be called")

    monkeypatch.setattr(cp_pkg.cp_cmodule, "oi_compute", fail_oi_compute)

    sensors = camera.take_picture(scene, exposure_times=0.1, focus_dists=2.0, render_flags=True)
    assert len(sensors) == 1
    assert sensors[0].exposure_time == 0.1
