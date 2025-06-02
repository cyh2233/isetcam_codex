import numpy as np

from isetcam import vc_rect_to_locs, vc_locs_to_rect


def test_roundtrip_rect_locs():
    rect = (2, 1, 3, 2)
    rows, cols = vc_rect_to_locs(rect)
    out = vc_locs_to_rect((rows, cols))
    assert out == rect


def test_locs_array_input():
    rect = (0, 0, 2, 3)
    rows, cols = vc_rect_to_locs(rect)
    locs = np.array([(r, c) for r in rows for c in cols])
    out = vc_locs_to_rect(locs)
    assert out == rect


def test_invalid_inputs():
    with np.testing.assert_raises(ValueError):
        vc_rect_to_locs((1, 2, 0, 1))
    with np.testing.assert_raises(ValueError):
        vc_locs_to_rect(np.empty((0, 2)))
