import numpy as np

from isetcam.illuminant import Illuminant, illuminant_modernize


def test_modernize_passthrough():
    illum = Illuminant(spd=np.array([1.0, 0.5]), wave=np.array([500, 510]), name="demo")
    out = illuminant_modernize(illum)
    assert out is illum


def test_modernize_from_simple_dict():
    legacy = {
        "spd": np.array([0.1, 0.2, 0.3]),
        "wave": np.array([400, 500, 600]),
        "name": "simple",
    }
    out = illuminant_modernize(legacy)
    assert isinstance(out, Illuminant)
    assert np.allclose(out.spd, legacy["spd"])
    assert np.array_equal(out.wave, legacy["wave"])
    assert out.name == legacy["name"]


def test_modernize_from_legacy_fields():
    legacy = {
        "data": {"photons": np.array([1.0, 2.0])},
        "wavelength": np.array([500, 510]),
        "name": "old",
    }
    out = illuminant_modernize(legacy)
    assert np.allclose(out.spd, legacy["data"]["photons"])
    assert np.array_equal(out.wave, legacy["wavelength"])
    assert out.name == "old"
