import numpy as np

from isetcam.scene import Scene
from isetcam.sensor import sensor_create
from isetcam.optics import optics_create
from isetcam.cp import CPScene, CPCModule, CPCamera, cp_burst_camera, cp_burst_ip


def _simple_scene() -> Scene:
    photons = np.ones((1, 1, 1), dtype=float)
    return Scene(photons=photons, wave=np.array([550.0]))


def test_cpscene_render_repeat():
    sc = CPScene([_simple_scene()])
    exp = [0.1, 0.1, 0.1]
    out = sc.render(exp)
    assert len(out) == 3
    for s in out:
        assert np.allclose(s.photons, 1.0)


def test_burst_capture_sum():
    scene = CPScene([_simple_scene()])
    sensor = sensor_create()
    optics = optics_create()
    module = CPCModule(sensor=sensor, optics=optics)
    camera = CPCamera([module])

    exp_times = cp_burst_camera(3, 0.03, mode="burst")
    sensors = camera.take_picture(scene, exposure_times=exp_times)
    assert len(sensors) == 3

    combined = cp_burst_ip(sensors, mode="sum")
    expected = sensors[0].volts * 3
    assert np.allclose(combined, expected)


def test_burst_camera_hdr_odd():
    exp = cp_burst_camera(3, 0.01, mode="hdr")
    expected = [0.01 * 2 ** -1, 0.01, 0.01 * 2 ** 1]
    assert np.allclose(exp, expected)


def test_burst_camera_hdr_even():
    exp = cp_burst_camera(4, 0.01, mode="hdr")
    offset = (4 - 1) / 2
    expected = [0.01 * 2 ** ((i - offset)) for i in range(4)]
    assert np.allclose(exp, expected)


def test_burst_camera_hdr_ev_step():
    exp = cp_burst_camera(3, 0.01, mode="hdr", ev_step=0.5)
    expected = [0.01 * 2 ** (-0.5), 0.01, 0.01 * 2 ** (0.5)]
    assert np.allclose(exp, expected)
