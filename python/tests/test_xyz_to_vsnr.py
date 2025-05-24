import numpy as np
from isetcam.metrics import xyz_to_vsnr, SCIELABParams

WHITE = np.array([1.0, 1.0, 1.0])


def test_xyz_to_vsnr_identity_filters():
    roi = np.array(
        [
            [[0.1, 0.2, 0.3], [0.2, 0.3, 0.4], [0.3, 0.4, 0.5]],
            [[0.2, 0.3, 0.4], [0.3, 0.4, 0.5], [0.4, 0.5, 0.6]],
            [[0.3, 0.4, 0.5], [0.4, 0.5, 0.6], [0.5, 0.6, 0.7]],
        ],
        dtype=float,
    )

    params = SCIELABParams(
        filters=[np.array([[1.0]]), np.array([[1.0]]), np.array([[1.0]])],
        filterSize=1,
        sampPerDeg=1,
    )

    val = xyz_to_vsnr(roi, WHITE, params)
    expected = 0.07412217171654639
    assert np.isclose(val, expected)
