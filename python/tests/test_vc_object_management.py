import numpy as np

from isetcam import (
    ie_init,
    vc_add_and_select_object,
    vc_get_object,
    vc_replace_object,
    vc_replace_and_select_object,
    vc_delete_object,
)
from isetcam.scene import Scene
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

