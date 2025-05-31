from isetcam.illuminant import illuminant_list


def test_illuminant_list_contains_sample():
    names = illuminant_list()
    assert isinstance(names, list)
    assert "D65" in names
    assert all(isinstance(n, str) for n in names)
