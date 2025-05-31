"""Display-related functions.

Use :func:`display_create` to load one of the calibration files that ship
with ISETCam, or :func:`display_from_file` to load a display definition from a
MAT-file.
"""

from .display_class import Display
from .display_create import display_create
from .display_get import display_get
from .display_set import display_set
from .display_apply_gamma import display_apply_gamma
from .display_render import display_render
from .display_show_image import display_show_image
from .display_from_file import display_from_file
from .display_to_file import display_to_file
from .display_list import display_list
from .display_max_contrast import display_max_contrast
from .display_plot import display_plot

__all__ = [
    "Display",
    "display_create",
    "display_get",
    "display_set",
    "display_apply_gamma",
    "display_render",
    "display_show_image",
    "display_from_file",
    "display_to_file",
    "display_list",
    "display_max_contrast",
    "display_plot",
]
