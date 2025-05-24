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
from .display_from_file import display_from_file

__all__ = [
    "Display",
    "display_create",
    "display_get",
    "display_set",
    "display_apply_gamma",
    "display_from_file",
]
