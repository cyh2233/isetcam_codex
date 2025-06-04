from pathlib import Path
import importlib.util
import sys
import matplotlib

matplotlib.use("Agg")


def _load_tutorial():
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "sensor" / "t_sensor_estimation.py"
    spec = importlib.util.spec_from_file_location("t_sensor_estimation", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_sensor_estimation_shapes():
    mod = _load_tutorial()
    qe_shape, rgb_shape = mod.main()
    assert qe_shape[1] == 3
    assert rgb_shape[0] == 3
