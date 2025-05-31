from isetcam.pixel import Pixel, pixel_get, pixel_set


def test_pixel_get_set():
    p = Pixel(width=2.8e-6, height=2.8e-6, well_capacity=5000, fill_factor=0.5)

    assert pixel_get(p, " width ") == 2.8e-6
    assert pixel_get(p, "HEIGHT") == 2.8e-6
    assert pixel_get(p, "well capacity") == 5000
    assert pixel_get(p, "Fill_Factor") == 0.5

    pixel_set(p, "Width", 3e-6)
    assert pixel_get(p, "width") == 3e-6

    pixel_set(p, "height", 3e-6)
    assert pixel_get(p, "HEIGHT") == 3e-6

    pixel_set(p, "wellCapacity", 6000)
    assert pixel_get(p, "well_capacity") == 6000

    pixel_set(p, "fill factor", 0.6)
    assert pixel_get(p, "fillFactor") == 0.6
