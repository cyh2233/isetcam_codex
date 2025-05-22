from isetcam import ie_init, ie_init_session, vc_constants


def test_ie_init_returns_session():
    session = ie_init()
    assert isinstance(session, dict)
    assert 'NAME' in session
    assert 'DIR' in session
    assert session['GUI']['waitbar'] == 0


def test_ie_init_session_can_be_called_directly():
    session = ie_init_session()
    assert 'SCENE' in session
    assert session['SCENE'][0] is None
