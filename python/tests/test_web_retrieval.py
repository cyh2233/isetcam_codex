from pathlib import Path

from isetcam.web import web_flickr, web_pixabay


class FakeResponse:
    def __init__(self, *, json_data=None, content=b"", status=200):
        self._json_data = json_data
        self.content = content
        self.status_code = status

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"status {self.status_code}")


def test_web_flickr(mocker, tmp_path):
    api_json = {
        "photos": {
            "photo": [
                {"id": "1", "secret": "s1", "server": "srv1"},
                {"id": "2", "secret": "s2", "server": "srv2"},
            ]
        }
    }

    mock_get = mocker.patch("requests.get")
    mock_get.side_effect = [
        FakeResponse(json_data=api_json),
        FakeResponse(content=b"img1"),
        FakeResponse(content=b"img2"),
    ]

    paths = web_flickr("cats", "KEY", 2, tmp_path)
    assert mock_get.call_count == 3

    # check API call parameters
    url, kwargs = mock_get.call_args_list[0]
    assert url[0] == "https://api.flickr.com/services/rest/"
    assert kwargs["params"]["text"] == "cats"
    assert len(paths) == 2
    for idx, p in enumerate(paths):
        assert Path(p).exists()
        assert Path(p).read_bytes() == f"img{idx+1}".encode()


def test_web_pixabay(mocker, tmp_path):
    api_json = {
        "hits": [
            {"largeImageURL": "http://img1"},
            {"largeImageURL": "http://img2"},
        ]
    }

    mock_get = mocker.patch("requests.get")
    mock_get.side_effect = [
        FakeResponse(json_data=api_json),
        FakeResponse(content=b"img1"),
        FakeResponse(content=b"img2"),
    ]

    paths = web_pixabay("dogs", "KEY", 2, tmp_path)
    assert mock_get.call_count == 3

    url, kwargs = mock_get.call_args_list[0]
    assert url[0] == "https://pixabay.com/api/"
    assert kwargs["params"]["q"] == "dogs"
    assert len(paths) == 2
    for idx, p in enumerate(paths):
        assert Path(p).exists()
        assert Path(p).read_bytes() == f"img{idx+1}".encode()
