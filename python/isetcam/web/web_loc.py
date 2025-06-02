# mypy: ignore-errors
"""Utilities for retrieving images from the Library of Congress API."""

from __future__ import annotations

from typing import List, Dict, Any

import requests


class WebLOC:
    """Simple wrapper around the LOC pictures search API."""

    def __init__(self) -> None:
        self.search_url = "https://loc.gov/pictures/search/"
        self.default_per_page = 20
        self.tag_mode = "all"
        self.sort = "date_desc"

    def search(self, tags: str) -> List[Dict[str, Any]]:
        """Search LOC for images matching *tags*.

        Parameters
        ----------
        tags:
            Comma separated keywords.
        Returns
        -------
        list of dict
            Filtered results returned by the API.
        """
        search_padding = 3
        per_page = self.default_per_page
        query = tags.replace(",", "+")
        params = {
            "fo": "json",
            "q": query,
            "c": per_page * search_padding,
        }
        resp = requests.get(self.search_url, params=params)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        return self.filter_results(results)

    def filter_results(self, list_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove results that do not provide digitized images."""
        not_digitized = "item not digitized thumbnail"
        filtered: List[Dict[str, Any]] = []
        for r in list_results:
            image = r.get("image", {})
            if image.get("alt") == not_digitized:
                continue
            filtered.append(r)
        return filtered

    def get_image_url(self, photo: Dict[str, Any], size: str) -> str:
        """Return the image URL for *photo* of the given *size*."""
        if size == "thumbnail":
            url = photo["image"]["thumb"]
        else:
            url = photo["image"]["full"]
        if url.startswith("//"):
            url = "https:" + url
        return url

    def get_image(self, photo: Dict[str, Any], size: str) -> bytes:
        """Download image bytes for *photo* of the given *size*."""
        url = self.get_image_url(photo, size)
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.content
