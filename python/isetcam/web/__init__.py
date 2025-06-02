# mypy: ignore-errors
"""Utilities for retrieving images from web APIs."""

from __future__ import annotations

from pathlib import Path
from typing import List

import requests

__all__ = ["web_flickr", "web_pixabay"]


def _write_image(content: bytes, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(content)


def web_flickr(query: str, api_key: str, n_images: int, out_dir: str | Path) -> List[str]:
    """Download images from Flickr.

    Parameters
    ----------
    query:
        Search string.
    api_key:
        Flickr API key.
    n_images:
        Number of images to fetch.
    out_dir:
        Directory where images will be saved.

    Returns
    -------
    list of str
        Paths to the downloaded images.
    """

    params = {
        "method": "flickr.photos.search",
        "text": query,
        "per_page": n_images,
        "page": 1,
        "api_key": api_key,
        "format": "json",
        "nojsoncallback": 1,
        "media": "photos",
    }
    resp = requests.get("https://api.flickr.com/services/rest/", params=params)
    resp.raise_for_status()
    data = resp.json()
    photos = data.get("photos", {}).get("photo", [])[:n_images]
    out_paths = []
    out_dir = Path(out_dir)
    for idx, p in enumerate(photos):
        url = f"https://live.staticflickr.com/{p['server']}/{p['id']}_{p['secret']}.jpg"
        img_resp = requests.get(url)
        img_resp.raise_for_status()
        path = out_dir / f"flickr_{idx}.jpg"
        _write_image(img_resp.content, path)
        out_paths.append(str(path))
    return out_paths


def web_pixabay(query: str, api_key: str, n_images: int, out_dir: str | Path) -> List[str]:
    """Download images from Pixabay.

    Parameters
    ----------
    query:
        Search string.
    api_key:
        Pixabay API key.
    n_images:
        Number of images to fetch.
    out_dir:
        Directory where images will be saved.

    Returns
    -------
    list of str
        Paths to the downloaded images.
    """

    params = {
        "key": api_key,
        "q": query,
        "per_page": n_images,
        "image_type": "photo",
    }
    resp = requests.get("https://pixabay.com/api/", params=params)
    resp.raise_for_status()
    data = resp.json()
    hits = data.get("hits", [])[:n_images]
    out_paths = []
    out_dir = Path(out_dir)
    for idx, h in enumerate(hits):
        url = h.get("largeImageURL") or h.get("webformatURL")
        if not url:
            continue
        img_resp = requests.get(url)
        img_resp.raise_for_status()
        path = out_dir / f"pixabay_{idx}.jpg"
        _write_image(img_resp.content, path)
        out_paths.append(str(path))
    return out_paths
