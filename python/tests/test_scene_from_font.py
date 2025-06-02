from isetcam.scene import scene_from_font
from isetcam.fonts import font_create
from isetcam.scene import Scene
import numpy as np
import pytest


def test_scene_from_font_basic():
    f = font_create("A", size=20)
    sc = scene_from_font("AB", f, spacing=1)
    assert isinstance(sc, Scene)
    assert sc.photons.ndim == 3
    assert sc.photons.shape[2] == 3
    # width should be larger than single character
    sc_single = scene_from_font("A", f, spacing=1)
    assert sc.photons.shape[1] > sc_single.photons.shape[1]


def test_scene_from_font_invalid_spacing():
    f = font_create("A")
    with pytest.raises(ValueError):
        scene_from_font("A", f, spacing=-1)
