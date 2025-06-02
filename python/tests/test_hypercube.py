import numpy as np

from isetcam.hypercube import (
    hc_basis,
    hc_blur,
    hc_illuminant_scale,
    hc_image,
    hc_image_crop,
    hc_image_rotate_clip,
)


def _simple_cube() -> tuple[np.ndarray, np.ndarray]:
    wave = np.array([500, 600], dtype=float)
    cube = np.stack(
        [np.full((4, 4), 0.5), np.full((4, 4), 1.0)], axis=2
    )
    return cube, wave


def test_hc_basis_identity():
    cube, _ = _simple_cube()
    basis = np.eye(2)
    recon = hc_basis(cube, basis)
    assert np.allclose(recon, cube)


def test_hc_blur_constant():
    cube, _ = _simple_cube()
    out = hc_blur(cube, sigma=1.0)
    assert np.allclose(out, cube)


def test_hc_illuminant_scale_vector():
    cube, _ = _simple_cube()
    illum = np.array([1.0, 2.0])
    new_illum = hc_illuminant_scale(cube, illum)
    scaled = illum * (cube / illum.reshape(1, 1, -1)).mean()
    assert np.allclose(new_illum, scaled)


def test_hc_image_crop():
    cube, _ = _simple_cube()
    cropped = hc_image_crop(cube, (1, 1, 2, 2))
    assert cropped.shape == (2, 2, 2)
    assert np.allclose(cropped, cube[1:3, 1:3, :])


def test_hc_image_rotate_clip():
    cube, _ = _simple_cube()
    rotated = hc_image_rotate_clip(cube, 90)
    assert rotated.shape == cube.shape


def test_hc_image():
    cube, wave = _simple_cube()
    rgb = hc_image(cube, wave)
    assert rgb.shape == (4, 4, 3)

