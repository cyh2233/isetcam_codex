from pathlib import Path
import importlib.util
import sys
import pytest
import matplotlib

matplotlib.use("Agg")


def _load_tutorial(name: str):
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "sensor" / name
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _rawpy_available() -> bool:
    try:
        import rawpy  # noqa: F401
        return True
    except Exception:
        return False


def test_t_sensor_exposure_color():
    mod = _load_tutorial("t_sensor_exposure_color.py")
    exp_time, rgb1, rgb2 = mod.main()
    assert exp_time > 0
    assert rgb1.shape == (3,)
    assert rgb2.shape == (3,)


def test_t_sensor_color_filters():
    mod = _load_tutorial("t_sensor_color_filters.py")
    shape, names, mean_v = mod.main()
    assert len(names) == shape[1]
    assert mean_v >= 0


def test_t_sensor_fpn():
    mod = _load_tutorial("t_sensor_fpn.py")
    base_mean, var_p, var_fpn = mod.main()
    assert base_mean >= 0
    assert var_fpn > var_p >= 0


def test_t_sensor_input_refer():
    mod = _load_tutorial("t_sensor_input_refer.py")
    e1, lum, e2, ill, q = mod.main()
    assert e1 > 0
    assert e2 > 0
    assert lum > 0
    assert ill > 0
    assert q > 0


def test_t_sensor_spatial_resolution():
    mod = _load_tutorial("t_sensor_spatial_resolution.py")
    coarse_shape, fine_shape = mod.main()
    assert coarse_shape[0] > 0 and fine_shape[0] > 0
    assert fine_shape[0] >= coarse_shape[0]


@pytest.mark.skipif(not _rawpy_available(), reason="rawpy not available")
def test_t_sensor_read_raw():
    mod = _load_tutorial("t_sensor_read_raw.py")
    cropped_shape, rgb_shape = mod.main()
    assert len(cropped_shape) == 2
    assert rgb_shape[-1] == 3
