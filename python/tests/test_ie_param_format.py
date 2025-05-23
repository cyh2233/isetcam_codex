import numpy as np

from isetcam import ie_param_format


def test_format_string():
    assert ie_param_format("Exposure Time") == "exposuretime"
    assert ie_param_format("Hello World") == "helloworld"


def test_format_numeric():
    assert ie_param_format(42) == 42
    arr = np.array([1, 2])
    assert ie_param_format(arr) is arr


def test_format_list():
    inp = ["Exposure Time", 1, "CamelCase", True]
    out = ie_param_format(inp)
    assert out == ["exposuretime", 1, "camelcase", True]


def test_format_tuple():
    inp = ("Exposure Time", 1, "CamelCase", 2)
    out = ie_param_format(inp)
    assert out == ("exposuretime", 1, "camelcase", 2)
