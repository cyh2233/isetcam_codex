from isetcam import ie_init, ie_session_get, ie_session_set


def test_set_and_get_basic_values():
    ie_init()
    ie_session_set('version', '1.2.3')
    assert ie_session_get('version') == '1.2.3'

    ie_session_set('name', 'my session')
    assert ie_session_get('name') == 'my session'

    ie_session_set('dir', '/tmp')
    assert ie_session_get('dir') == '/tmp'

    ie_session_set('waitbar', 1)
    assert ie_session_get('waitbar') == 1

    ie_session_set('font size', 14)
    assert ie_session_get('font size') == 14

    ie_session_set('init clear', True)
    assert ie_session_get('init clear') in {True, 1}


def test_selected_object_handling():
    ie_init()
    ie_session_set('scene', 2)
    assert ie_session_get('scene') == 2

    ie_session_set('selected', 3, 'sensor')
    assert ie_session_get('selected', 'sensor') == 3
