import numpy as np

from isetcam import (
    ie_init,
    vc_add_and_select_object,
    vc_get_object,
    vc_replace_object,
    vc_replace_and_select_object,
    vc_delete_object,
    vc_clear_objects,
)
from isetcam.scene import Scene
from isetcam.opticalimage import OpticalImage
from isetcam.sensor import Sensor
from isetcam.display import Display
from isetcam.camera import camera_create
from isetcam.ie_init_session import vcSESSION


def test_vc_get_object():
    ie_init()
    sc = Scene(photons=np.zeros((1, 1, 1)))
    idx = vc_add_and_select_object("scene", sc)
    assert vc_get_object("scene", idx) is sc
    assert vc_get_object("scene") is sc


def test_vc_replace_object():
    ie_init()
    sc1 = Scene(photons=np.zeros((1, 1, 1)))
    idx = vc_add_and_select_object("scene", sc1)

    sc2 = Scene(photons=np.ones((1, 1, 1)))
    out = vc_replace_object("scene", sc2, idx)
    assert out == idx
    assert vc_get_object("scene", idx) is sc2
    assert vcSESSION["SELECTED"]["SCENE"] == idx


def test_vc_replace_and_select_object():
    ie_init()
    sc1 = Scene(photons=np.zeros((1, 1, 1)))
    idx = vc_add_and_select_object("scene", sc1)

    sc2 = Scene(photons=np.ones((1, 1, 1)))
    out = vc_replace_and_select_object("scene", sc2)
    assert out == idx
    assert vc_get_object("scene", idx) is sc2
    assert vcSESSION["SELECTED"]["SCENE"] == idx


def test_vc_delete_object():
    ie_init()
    sc1 = Scene(photons=np.zeros((1, 1, 1)))
    sc2 = Scene(photons=np.ones((1, 1, 1)))
    idx1 = vc_add_and_select_object("scene", sc1)
    idx2 = vc_add_and_select_object("scene", sc2)

    remaining = vc_delete_object("scene", idx1)
    assert remaining == 1
    assert vc_get_object("scene", 1) is sc2
    assert vcSESSION["SELECTED"]["SCENE"] == 1


def test_vc_delete_selected_object():
    ie_init()
    sc1 = Scene(photons=np.zeros((1, 1, 1)))
    sc2 = Scene(photons=np.ones((1, 1, 1)))
    vc_add_and_select_object("scene", sc1)
    vc_add_and_select_object("scene", sc2)

    remaining = vc_delete_object("scene")
    assert remaining == 1
    assert vc_get_object("scene", 1) is sc1
    assert vcSESSION["SELECTED"]["SCENE"] == 1


def test_vc_clear_objects():
    ie_init()
    sc = Scene(photons=np.zeros((1, 1, 1)))
    oi = OpticalImage(photons=np.zeros((1, 1, 1)))
    si = Sensor(volts=np.zeros((1, 1, 1)), exposure_time=0.01)
    dp = Display(spd=np.zeros((1, 3)), wave=np.array([500, 600, 700]))
    cam = camera_create(sensor=si)

    vc_add_and_select_object("scene", sc)
    vc_add_and_select_object("opticalimage", oi)
    vc_add_and_select_object("sensor", si)
    vc_add_and_select_object("display", dp)
    vc_add_and_select_object("camera", cam)

    vc_clear_objects()

    assert vcSESSION["SCENE"] == [None]
    assert vcSESSION["OPTICALIMAGE"] == [None]
    assert vcSESSION["ISA"] == [None]
    assert vcSESSION["VCIMAGE"] == [None]
    assert vcSESSION["DISPLAY"] == [None]
    assert vcSESSION["GRAPHWIN"] == []
    assert vcSESSION["CAMERA"] == [None]

    for fld in [
        "SCENE",
        "OPTICALIMAGE",
        "ISA",
        "VCIMAGE",
        "DISPLAY",
        "GRAPHWIN",
        "CAMERA",
    ]:
        assert vcSESSION["SELECTED"][fld] == []

