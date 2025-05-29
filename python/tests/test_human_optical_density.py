import numpy as np
from isetcam.human import human_optical_density


def test_human_optical_density_defaults():
    params = human_optical_density()
    assert params["visfield"] == "fovea"
    assert np.isclose(params["lens"], 1.0)
    assert np.isclose(params["macular"], 0.28)
    assert np.isclose(params["LPOD"], 0.5)
    assert np.isclose(params["MPOD"], 0.5)
    assert np.isclose(params["SPOD"], 0.4)
    assert np.isclose(params["melPOD"], 0.5)
    assert np.array_equal(params["wave"], np.arange(390, 731))
