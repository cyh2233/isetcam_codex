# mypy: ignore-errors
"""Python utilities migrated from ISETCam."""

from importlib.metadata import PackageNotFoundError, version as _version

try:  # pragma: no cover - fallback for editable installs
    __version__ = _version("isetcam")
except PackageNotFoundError:  # pragma: no cover - package metadata not found
    __version__ = "0.0.0"

from .vc_constants import vc_constants
from .iset_root_path import iset_root_path
from .data_path import data_path
from .vc_get_image_format import vc_get_image_format
from .quanta2energy import quanta_to_energy
from .energy_to_quanta import energy_to_quanta
from .ie_responsivity_convert import ie_responsivity_convert
from .ie_init import ie_init
from .ie_init_session import ie_init_session
from .luminance_from_energy import luminance_from_energy
from .luminance_from_photons import luminance_from_photons
from .scotopic_luminance_from_energy import scotopic_luminance_from_energy
from .scotopic_luminance_from_photons import scotopic_luminance_from_photons
from .ie_luminance_to_radiance import ie_luminance_to_radiance
from .ie_xyz_from_energy import ie_xyz_from_energy
from .ie_xyz_from_photons import ie_xyz_from_photons
from .ie_color_transform import ie_color_transform
from .color_transform_matrix import color_transform_matrix
from .color_transform_matrix_create import color_transform_matrix_create
from .color_block_matrix import color_block_matrix
from .chromaticity import chromaticity
from .chromaticity_plot import chromaticity_plot
from .cct import cct
from .cct_to_sun import cct_to_sun
from .daylight import daylight
from .circle_points import circle_points
from .ie_clip import ie_clip
from .ie_param_format import ie_param_format
from .ie_session_get import ie_session_get
from .ie_session_set import ie_session_set
from .ie_save_session import ie_save_session
from .ie_load_session import ie_load_session
from .vc_add_and_select_object import vc_add_and_select_object
from .vc_get_object import vc_get_object
from .vc_replace_object import vc_replace_object
from .vc_replace_and_select_object import vc_replace_and_select_object
from .vc_delete_object import vc_delete_object
from .vc_clear_objects import vc_clear_objects
from .vc_get_objects import vc_get_objects
from .vc_count_objects import vc_count_objects
from .vc_get_object_names import vc_get_object_names
from .vc_get_selected_object import vc_get_selected_object
from .vc_set_objects import vc_set_objects
from .vc_set_selected_object import vc_set_selected_object
from .vc_new_object_name import vc_new_object_name
from .vc_new_object_value import vc_new_object_value
from .vc_rect_to_locs import vc_rect_to_locs
from .vc_locs_to_rect import vc_locs_to_rect
from .vc_copy_object import vc_copy_object
from .vc_rename_object import vc_rename_object
from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format
from .xyz_to_lab import xyz_to_lab
from .lab_to_xyz import lab_to_xyz
from .xyz_to_xyy import xyz_to_xyy
from .xyy_to_xyz import xyy_to_xyz
from .y_to_lstar import y_to_lstar
from .lstar_to_y import lstar_to_y
from .xyz_to_uv import xyz_to_uv
from .xyz_to_luv import xyz_to_luv
from .lms_to_xyz import lms_to_xyz
from .xyz_to_lms import xyz_to_lms
from .lms_to_srgb import lms_to_srgb
from .srgb_to_lms import srgb_to_lms
from .srgb_to_lab import srgb_to_lab
from .lab_to_srgb import lab_to_srgb
from .srgb_to_lrgb import srgb_to_lrgb
from .lrgb_to_srgb import lrgb_to_srgb
from .srgb_xyz import (
    srgb_to_linear,
    linear_to_srgb,
    srgb_to_xyz,
    xyz_to_srgb,
)
from .rgb_ycbcr import rgb_to_ycbcr, ycbcr_to_rgb
from .srgb_to_cct import srgb_to_cct
from .spd_to_cct import spd_to_cct
from .xyz_to_cct import xyz_to_cct
from .srgb_parameters import srgb_parameters
from .adobergb_parameters import adobergb_parameters
from .ctemp_to_srgb import ctemp_to_srgb
from .init_default_spectrum import init_default_spectrum
from .mk_inv_gamma_table import mk_inv_gamma_table
from .ie_gamma import ie_gamma
from .ie_tone import ie_tone_curve, ie_apply_tone
from .ie_cov_ellipsoid import ie_cov_ellipsoid
from .ie_read_spectra import ie_read_spectra
from .ie_hist_image import ie_hist_image
from .ie_scale import ie_scale
from .ie_scale_columns import ie_scale_columns
from .ie_prctile import ie_prctile
from .ie_mvnrnd import ie_mvnrnd
from .ie_poisson import ie_poisson
from .ie_normpdf import ie_normpdf
from .ie_tikhonov import ie_tikhonov
from .ie_format_figure import (
    ie_format_figure,
    set_ie_figure_defaults,
    _IE_FIGURE_DEFAULTS,
)
from .imgproc import (
    image_distort,
    ie_internal_to_display,
    ie_nearest_neighbor,
    ie_bilinear,
    adaptive_laplacian,
    bayer_indices,
    pocs,
    faulty_insert,
    faulty_list,
    faulty_pixel_correction,
)
from .ie_spectra_sphere import ie_spectra_sphere
from .metrics.ie_psnr import ie_psnr
from .metrics.scielab import scielab, sc_params, SCIELABParams
from .metrics.xyz_to_vsnr import xyz_to_vsnr
from .metrics.ssim_metric import ssim_metric
from .metrics.exposure_value import exposure_value
from .metrics.iso_speed_saturation import iso_speed_saturation
from .human import (
    human_pupil_size,
    human_macular_transmittance,
    human_optical_density,
    human_wave_defocus,
    human_core,
    human_otf,
    human_achromatic_otf,
    human_lsf,
    human_cone_contrast,
    human_cone_isolating,
    human_cones,
    human_cone_mosaic,
    human_cone_plot,
    watson_impulse_response,
    watson_rgc_spacing,
)
from .hypercube import (
    hc_basis,
    hc_blur,
    hc_illuminant_scale,
    hc_image,
    hc_image_crop,
    hc_image_rotate_clip,
)

# Expose subpackages that mirror the MATLAB modules. These are currently
# placeholders for future development.
from . import scene, opticalimage, sensor, pixel, display, illuminant, camera, imgproc, metrics, optics, human, ip, cp, hypercube, fonts  # noqa: E501
from .opticalimage import oi_to_file, oi_plot
from .sensor import sensor_to_file
from .display import (
    display_to_file,
    display_list,
    display_max_contrast,
    display_plot,
    display_description,
    display_reflectance,
    display_set_max_luminance,
    display_set_white_point,
)
from .camera import (
    camera_to_file,
    camera_from_file,
    camera_plot,
    camera_moire,
)
from .optics import optics_to_file, optics_from_file
from .scene import scene_plot
from .scene import scene_from_font
from .illuminant import (
    illuminant_to_file,
    illuminant_from_file,
    illuminant_get,
    illuminant_set,
    illuminant_list,
)
from .fonts import font_create, font_get, font_set, font_bitmap_get
from .ip import ip_to_file, ip_from_file, ip_plot
from .io import (
    openexr_read,
    openexr_write,
    pfm_read,
    pfm_write,
    dng_read,
    dng_write,
    ie_read_color_filter,
    ie_save_color_filter,
    ie_save_multispectral_image,
    ie_load_multispectral_image,
)
from .animated_gif import animated_gif
from .ie_scp import ie_scp
from .web import web_flickr, web_pixabay, WebLOC

__all__ = [
    '__version__',
    'vc_constants',
    'vc_get_image_format',
    'quanta_to_energy',
    'energy_to_quanta',
    'ie_responsivity_convert',
    'luminance_from_energy',
    'luminance_from_photons',
    'scotopic_luminance_from_energy',
    'scotopic_luminance_from_photons',
    'ie_luminance_to_radiance',
    'ie_xyz_from_energy',
    'ie_xyz_from_photons',
    'ie_color_transform',
    'color_transform_matrix',
    'color_transform_matrix_create',
    'color_block_matrix',
    'chromaticity',
    'chromaticity_plot',
    'cct',
    'cct_to_sun',
    'daylight',
    'circle_points',
    'ie_clip',
    'ie_param_format',
    'ie_session_get',
    'ie_session_set',
    'ie_save_session',
    'ie_load_session',
    'rgb_to_xw_format',
    'xw_to_rgb_format',
    'xyz_to_lab',
    'lab_to_xyz',
    'xyz_to_xyy',
    'xyy_to_xyz',
    'y_to_lstar',
    'lstar_to_y',
    'xyz_to_uv',
    'xyz_to_luv',
    'lms_to_xyz',
    'xyz_to_lms',
    'lms_to_srgb',
    'srgb_to_lms',
    'srgb_to_lab',
    'lab_to_srgb',
    'srgb_to_lrgb',
    'lrgb_to_srgb',
    'srgb_to_linear',
    'linear_to_srgb',
    'srgb_to_xyz',
    'xyz_to_srgb',
    'rgb_to_ycbcr',
    'ycbcr_to_rgb',
    'srgb_to_cct',
    'spd_to_cct',
    'xyz_to_cct',
    'srgb_parameters',
    'adobergb_parameters',
    'ctemp_to_srgb',
    'init_default_spectrum',
    'mk_inv_gamma_table',
    'ie_gamma',
    'ie_tone_curve',
    'ie_apply_tone',
    'ie_cov_ellipsoid',
    'ie_read_spectra',
    'ie_hist_image',
    'ie_scale',
    'ie_scale_columns',
    'ie_prctile',
    'ie_mvnrnd',
    'ie_poisson',
    'ie_normpdf',
    'ie_tikhonov',
    'ie_format_figure',
    'set_ie_figure_defaults',
    '_IE_FIGURE_DEFAULTS',
    'ie_spectra_sphere',
    'image_distort',
    'ie_internal_to_display',
    'ie_nearest_neighbor',
    'ie_bilinear',
    'adaptive_laplacian',
    'bayer_indices',
    'pocs',
    'faulty_insert',
    'faulty_list',
    'faulty_pixel_correction',
    'ie_psnr',
    'scielab',
    'sc_params',
    'SCIELABParams',
    'xyz_to_vsnr',
    'ssim_metric',
    'exposure_value',
    'iso_speed_saturation',
    'human_pupil_size',
    'human_macular_transmittance',
    'human_optical_density',
    'human_wave_defocus',
    'human_core',
    'human_otf',
    'human_achromatic_otf',
    'human_lsf',
    'human_cone_contrast',
    'human_cone_isolating',
    'human_cones',
    'human_cone_mosaic',
    'human_cone_plot',
    'watson_impulse_response',
    'watson_rgc_spacing',
    'iset_root_path',
    'data_path',
    'ie_init',
    'ie_init_session',
    'camera',
    'optics',
    'scene',
    'opticalimage',
    'sensor',
    'pixel',
    'display',
    'illuminant',
    'imgproc',
    'metrics',
    'human',
    'ip',
    'cp',
    'fonts',
    'hypercube',
    'oi_to_file',
    'sensor_to_file',
    'display_to_file',
    'display_list',
    'display_max_contrast',
    'display_plot',
    'display_description',
    'display_reflectance',
    'display_set_max_luminance',
    'display_set_white_point',
    'illuminant_to_file',
    'illuminant_from_file',
    'illuminant_get',
    'illuminant_set',
    'illuminant_list',
    'camera_to_file',
    'camera_from_file',
    'camera_plot',
    'camera_moire',
    'scene_plot',
    'oi_plot',
    'optics_to_file',
    'optics_from_file',
    'ip_to_file',
    'ip_from_file',
    'ip_plot',
    'openexr_read',
    'openexr_write',
    'pfm_read',
    'pfm_write',
    'dng_read',
    'dng_write',
    'ie_read_color_filter',
    'ie_save_color_filter',
    'ie_save_multispectral_image',
    'ie_load_multispectral_image',
    'animated_gif',
    'ie_scp',
    'web_flickr',
    'web_pixabay',
    'WebLOC',
    'vc_add_and_select_object',
    'vc_get_object',
    'vc_replace_object',
    'vc_replace_and_select_object',
    'vc_delete_object',
    'vc_clear_objects',
    'vc_get_objects',
    'vc_count_objects',
    'vc_get_object_names',
    'vc_get_selected_object',
    'vc_set_objects',
    'vc_set_selected_object',
    'vc_new_object_name',
    'vc_new_object_value',
    'vc_rect_to_locs',
    'vc_locs_to_rect',
    'vc_copy_object',
    'vc_rename_object',
    'font_create',
    'font_get',
    'font_set',
    'font_bitmap_get',
    'scene_from_font',
    'hc_basis',
    'hc_blur',
    'hc_illuminant_scale',
    'hc_image',
    'hc_image_crop',
    'hc_image_rotate_clip',
]
