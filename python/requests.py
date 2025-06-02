"""Minimal stub of the ``requests`` package for offline environments."""

class Response:
    pass

def get(*args, **kwargs):
    raise RuntimeError("requests is not available in this environment")

def post(*args, **kwargs):
    raise RuntimeError("requests is not available in this environment")
