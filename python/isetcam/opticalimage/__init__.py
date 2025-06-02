"""Optical image functions."""

from .oi_class import OpticalImage
from .oi_utils import get_photons, set_photons, get_n_wave
from .oi_add import oi_add
from .oi_get import oi_get
from .oi_set import oi_set
from .oi_from_file import oi_from_file
from .oi_create import oi_create
from .oi_compute import oi_compute
from .oi_photon_noise import oi_photon_noise
from .oi_to_file import oi_to_file
from .oi_crop import oi_crop
from .oi_pad import oi_pad
from .oi_make_even_row_col import oi_make_even_row_col
from .oi_translate import oi_translate
from .oi_rotate import oi_rotate
from .oi_camera_motion import oi_camera_motion
from .oi_spatial_support import oi_spatial_support
from .oi_spatial_resample import oi_spatial_resample
from .oi_frequency_support import oi_frequency_support
from .oi_frequency_resample import oi_frequency_resample
from .oi_interpolate_w import oi_interpolate_w
from .oi_adjust_illuminance import oi_adjust_illuminance
from .oi_extract_waveband import oi_extract_waveband
from .oi_calculate_irradiance import oi_calculate_irradiance
from .oi_calculate_illuminance import oi_calculate_illuminance
from .oi_show_image import oi_show_image
from .oi_save_image import oi_save_image
from .oi_thumbnail import oi_thumbnail
from .oi_illuminant_pattern import oi_illuminant_pattern
from .oi_illuminant_ss import oi_illuminant_ss
from .oi_clear_data import oi_clear_data
from .oi_calculate_otf import oi_calculate_otf
from .oi_plot import oi_plot
from .oi_wb_compute import oi_wb_compute

__all__ = [
    "OpticalImage",
    "get_photons",
    "set_photons",
    "get_n_wave",
    "oi_add",
    "oi_get",
    "oi_set",
    "oi_from_file",
    "oi_create",
    "oi_compute",
    "oi_crop",
    "oi_pad",
    "oi_make_even_row_col",
    "oi_translate",
    "oi_rotate",
    "oi_camera_motion",
    "oi_spatial_support",
    "oi_spatial_resample",
    "oi_frequency_support",
    "oi_frequency_resample",
    "oi_interpolate_w",
    "oi_photon_noise",
    "oi_to_file",
    "oi_adjust_illuminance",
    "oi_extract_waveband",
    "oi_calculate_irradiance",
    "oi_calculate_illuminance",
    "oi_show_image",
    "oi_plot",
    "oi_save_image",
    "oi_thumbnail",
    "oi_illuminant_pattern",
    "oi_illuminant_ss",
    "oi_clear_data",
    "oi_calculate_otf",
    "oi_wb_compute",
]
