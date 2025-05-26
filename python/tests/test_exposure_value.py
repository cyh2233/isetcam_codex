import numpy as np
import pytest

from isetcam import exposure_value


def test_exposure_value_basic():
    assert exposure_value(1, 1) == 0
    assert exposure_value(2, 1) == pytest.approx(np.log2(4))
    assert exposure_value(1, 0.5) == pytest.approx(np.log2(2))


def test_exposure_value_invalid():
    with pytest.raises(ValueError):
        exposure_value(0, 1)
    with pytest.raises(ValueError):
        exposure_value(1, -1)
