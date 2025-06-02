import numpy as np

from isetcam.io import ie_save_multispectral_image, ie_load_multispectral_image


def test_multispectral_roundtrip(tmp_path):
    coefficients = np.random.rand(2, 3, 4).astype(np.float32)
    basis = np.random.rand(5, 4).astype(np.float32)
    comment = "demo"
    img_mean = np.random.rand(5).astype(np.float32)
    illuminant = np.random.rand(5).astype(np.float32)
    fov = 12.5
    distance = 1.0
    name = "cube"

    path = tmp_path / "cube.mat"
    ie_save_multispectral_image(
        path,
        coefficients,
        basis,
        comment=comment,
        img_mean=img_mean,
        illuminant=illuminant,
        fov=fov,
        distance=distance,
        name=name,
    )

    loaded = ie_load_multispectral_image(path)
    assert np.allclose(loaded["coefficients"], coefficients)
    assert np.allclose(loaded["basis"], basis)
    assert loaded["comment"] == comment
    assert np.allclose(loaded["img_mean"], img_mean)
    assert np.allclose(loaded["illuminant"], illuminant)
    assert loaded["fov"] == fov
    assert loaded["distance"] == distance
    assert loaded["name"] == name
