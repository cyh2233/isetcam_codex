"""Optical image functions."""

from .oi_class import OpticalImage
from .oi_utils import get_photons, set_photons, get_n_wave

__all__ = [
    "OpticalImage",
    "get_photons",
    "set_photons",
    "get_n_wave",
]
