import numpy as np
from isetcam import image_distort


def test_gaussian_noise():
    np.random.seed(0)
    img = np.ones((10, 10), dtype=np.uint8) * 100
    out = image_distort(img, 'gaussian noise', 5)
    assert out.shape == img.shape
    assert out.dtype == np.uint8
    assert not np.array_equal(out, img)


def test_jpeg_compress(tmp_path):
    img = np.random.randint(0, 255, (20, 20, 3), dtype=np.uint8)
    out = image_distort(img, 'jpeg compress', 50)
    assert out.shape == img.shape
    assert out.dtype == img.dtype


def test_scale_contrast():
    img = np.ones((5, 5), dtype=float)
    out = image_distort(img, 'scale contrast', 0.2)
    assert np.allclose(out, img * 1.2)
