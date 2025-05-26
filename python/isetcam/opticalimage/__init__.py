"""Optical image functions."""

from .oi_class import OpticalImage
from .oi_utils import get_photons, set_photons, get_n_wave
from .oi_add import oi_add
from .oi_get import oi_get
from .oi_set import oi_set
from .oi_from_file import oi_from_file
from .oi_photon_noise import oi_photon_noise
from .oi_to_file import oi_to_file
from .oi_crop import oi_crop
from .oi_pad import oi_pad
from .oi_rotate import oi_rotate
from .oi_spatial_support import oi_spatial_support
from .oi_spatial_resample import oi_spatial_resample
from .oi_frequency_support import oi_frequency_support
from .oi_frequency_resample import oi_frequency_resample
from .oi_adjust_illuminance import oi_adjust_illuminance

__all__ = [
    "OpticalImage",
    "get_photons",
    "set_photons",
    "get_n_wave",
    "oi_add",
    "oi_get",
    "oi_set",
    "oi_from_file",
    "oi_crop",
    "oi_pad",
    "oi_rotate",
    "oi_spatial_support",
    "oi_spatial_resample",
    "oi_frequency_support",
    "oi_frequency_resample",
    "oi_photon_noise",
    "oi_to_file",
    "oi_adjust_illuminance",
]
