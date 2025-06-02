from isetcam.web import WebLOC


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


def test_search_filters_results(mocker):
    api_json = {
        "results": [
            {"image": {"thumb": "//t1", "full": "//f1", "alt": "thumb"}},
            {"image": {"thumb": "//t2", "full": "//f2", "alt": "item not digitized thumbnail"}},
        ]
    }

    mock_get = mocker.patch("requests.get", return_value=FakeResponse(json_data=api_json))
    loc = WebLOC()
    results = loc.search("cat,dog")
    assert mock_get.call_count == 1
    url, kwargs = mock_get.call_args
    assert url[0] == loc.search_url
    assert kwargs["params"]["q"] == "cat+dog"
    assert len(results) == 1


def test_get_image_uses_https_and_returns_bytes(mocker):
    mock_get = mocker.patch("requests.get", return_value=FakeResponse(content=b"img"))
    loc = WebLOC()
    photo = {"image": {"thumb": "//thumb", "full": "//full"}}
    data = loc.get_image(photo, "thumbnail")
    assert mock_get.call_count == 1
    assert mock_get.call_args[0][0] == "https://thumb"
    assert data == b"img"
