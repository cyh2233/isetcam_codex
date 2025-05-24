import copy

from isetcam import (
    ie_init,
    ie_session_set,
    ie_session_get,
    ie_save_session,
    ie_load_session,
)
from isetcam.ie_init_session import vcSESSION


def test_session_save_and_load(tmp_path):
    ie_init()
    ie_session_set('version', '1.0')
    ie_session_set('name', 'my session')
    ie_session_set('scene', 3)

    expected = copy.deepcopy(vcSESSION)
    path = tmp_path / 'session.json'
    ie_save_session(vcSESSION, path)

    ie_init()
    assert ie_session_get('version') is None

    loaded = ie_load_session(path)
    assert loaded == expected
    assert ie_session_get('scene') == 3
    assert ie_session_get('name') == 'my session'

