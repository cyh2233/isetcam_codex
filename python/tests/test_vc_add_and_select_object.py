import numpy as np

from isetcam import (
    ie_init,
    vc_add_and_select_object,
)
from isetcam.scene import Scene
from isetcam.opticalimage import OpticalImage
from isetcam.sensor import Sensor
from isetcam.display import Display
from isetcam.camera import camera_create, Camera
from isetcam.ie_init_session import vcSESSION


def test_vc_add_and_select_scene():
    ie_init()
    sc = Scene(photons=np.zeros((1, 1, 1)))
    idx = vc_add_and_select_object('scene', sc)
    assert idx == 1
    assert vcSESSION['SCENE'][idx] is sc
    assert vcSESSION['SELECTED']['SCENE'] == idx


def test_vc_add_and_select_oi_sensor_display_camera():
    ie_init()
    oi = OpticalImage(photons=np.zeros((1, 1, 1)))
    si = Sensor(volts=np.zeros((1, 1, 1)), exposure_time=0.01)
    dp = Display(spd=np.zeros((1, 3)), wave=np.array([500, 600, 700]))
    cam = camera_create(sensor=si)

    oi_idx = vc_add_and_select_object('opticalimage', oi)
    assert vcSESSION['OPTICALIMAGE'][oi_idx] is oi
    assert vcSESSION['SELECTED']['OPTICALIMAGE'] == oi_idx

    sensor_idx = vc_add_and_select_object('sensor', si)
    assert vcSESSION['ISA'][sensor_idx] is si
    assert vcSESSION['SELECTED']['ISA'] == sensor_idx

    display_idx = vc_add_and_select_object('display', dp)
    assert vcSESSION['DISPLAY'][display_idx] is dp
    assert vcSESSION['SELECTED']['DISPLAY'] == display_idx

    cam_idx = vc_add_and_select_object('camera', cam)
    assert vcSESSION['CAMERA'][cam_idx] is cam
    assert vcSESSION['SELECTED']['CAMERA'] == cam_idx


