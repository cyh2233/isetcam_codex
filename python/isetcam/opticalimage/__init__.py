"""Optical image functions."""

from .oi_class import OpticalImage
from .oi_utils import get_photons, set_photons, get_n_wave
from .oi_add import oi_add

__all__ = [
    "OpticalImage",
    "get_photons",
    "set_photons",
    "get_n_wave",
    "oi_add",
]
