from isetcam.scene import scene_list


def test_scene_list_contains_sample():
    names = scene_list()
    assert isinstance(names, list)
    assert "d_sceneICVL" in names
    assert all(isinstance(n, str) for n in names)
