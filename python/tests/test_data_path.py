import importlib.resources as resources
from isetcam import data_path, iset_root_path


def test_data_path_packaged_human_xyz(tmp_path):
    path = data_path('human/XYZ.mat')
    assert path.is_file()
    fallback = iset_root_path() / 'data' / 'human' / 'XYZ.mat'
    assert path != fallback
    expected_b64 = resources.files('isetcam.data') / 'human' / 'XYZ.mat.b64'
    assert expected_b64.is_file()
