# MATLAB to Python Migration

This repository now contains experimental Python modules that replicate
portions of the MATLAB functionality. The long term goal is to allow
running ISETCam algorithms from Python directly or through MATLAB using
`pyenv`.

## Creating the Environment

Use a dedicated conda environment as described in
[`python/README.md`](../python/README.md):

```bash
conda create -n py39 python=3.9
conda activate py39
pip install -r python/requirements.txt
pip install -e python
```

Optional DNG and OpenEXR helpers rely on extra dependencies. Install
them when needed with:

```bash
pip install -e python[rawpy,OpenEXR]
```

Within MATLAB, point `pyenv` to the environment interpreter:

```matlab
pyenv('Version','/opt/miniconda3/envs/py39/bin/python');
```

The file `python/s_python.m` provides a step‑by‑step walkthrough of the
setup process.

## Running the Python Initialization Routines

Once the environment is activated (or after `pyenv` inside MATLAB), the
Python initialization mirrors the MATLAB `ieInit` command. In Python you
can run:

```python
from isetcam import ie_init
session = ie_init()
```


This returns a dictionary similar to the MATLAB `vcSESSION` structure.
You can also call `ie_init_session()` directly to construct the session
data structure without clearing the environment.

## Version Information

The package exposes ``isetcam.__version__`` so you can verify the
installed release:

```python
from isetcam import __version__
print(__version__)
```

When working from a source checkout the value is ``"0.0.0"`` if the
package metadata is unavailable.  After modifying any modules remember
to run ``pytest -q`` to confirm all tests still pass.

## Unit Tests

Unit tests are located in [`python/tests`](../python/tests). They can be
executed with `pytest` once the `PYTHONPATH` includes the `python`
directory:

```bash
export PYTHONPATH=$PWD/python
pytest -q
```


Running these tests verifies that the initialization routines and helper
functions behave as expected.

## Basic Pipeline Notebook

A short Jupyter notebook demonstrates constructing a scene, computing an optical image, simulating a sensor and rendering the result.
See [notebooks/basic_pipeline.ipynb](../notebooks/basic_pipeline.ipynb) for the full workflow. Validate it using the ``nbval`` plugin:

```bash
pytest --nbval notebooks/basic_pipeline.ipynb
```

Run ``pytest -q`` afterwards to execute the unit tests.


## Flake8 Workflow

The GitHub workflow `.github/workflows/python-tests.yml` installs
`flake8` and checks the code style of the Python package for every push
and pull request. You can run the same check locally:

```bash
flake8 python/isetcam
```

Run `flake8` together with `pytest -q` before submitting changes.

## Multi-version CI Tests

The GitHub action also runs the unit tests on Python 3.9, 3.10 and 3.11.
Check `.github/workflows/python-tests.yml` for details.

```bash
pytest -q
```

## Command Line Interface

Installing the package in editable mode exposes an ``isetcam`` command
with a few helper subcommands:

```bash
isetcam info          # show version and repository path
isetcam list-scenes   # list bundled sample scenes
isetcam run-tests     # execute the Python test suite
isetcam pipeline      # run a demo pipeline
```

The ``run-tests`` command simply invokes ``pytest`` in the repository
root. The ``pipeline`` subcommand runs a small camera pipeline and
stores the resulting camera structure in a MAT-file:

```bash
isetcam pipeline --scene "grid lines" --output cam.mat
```

## Building the Documentation

HTML documentation is generated with Sphinx. After installing the
package in editable mode you can build the docs locally:

```bash
cd docs
make html
```

The generated pages will be placed under `docs/build/html`.


## Finding the Repository Root

Use `iset_root_path` to locate the top level of the repository when
constructing paths to test data or calibration files.

```python
from isetcam import iset_root_path

root = iset_root_path()
print(root)
```

Run `pytest -q` after adding code that depends on the repository layout.

## Data Path Helper

Use `data_path` to locate calibration files bundled with the package. It
falls back to the repository `data` directory when running from the
source tree:

```python
from isetcam import data_path

path = data_path('lights/D65.mat')
```

Run `pytest -q` after editing functions that rely on `data_path`.
## Packaged Calibration Files

Calibration MAT-files in the `isetcam.data` package are stored as base64 text.
`data_path` extracts them to a temporary directory so they work both from a wheel
and a source checkout.

```python
from isetcam import data_path
xyz_mat = data_path("human/XYZ.mat")
```

Run `pytest -q` when modifying the packaged data.


## Conversion Functions

Several common ISETCam unit conversions have been reimplemented in
Python.  They are imported directly from the top level `isetcam`
module:

```python
from isetcam import energy_to_quanta, quanta_to_energy

photons = energy_to_quanta(wave, energy)
energy = quanta_to_energy(wave, photons)

from isetcam import luminance_from_energy, luminance_from_photons
l_from_e = luminance_from_energy(energy, wave)
l_from_p = luminance_from_photons(photons, wave)
```

These routines match the behavior of their MATLAB counterparts and are
used throughout the Python tests.

Additional helpers convert between the MATLAB "XW" format and standard
RGB arrays. This is useful when reshaping image data for matrix
operations:

```python
import numpy as np
from isetcam import rgb_to_xw_format, xw_to_rgb_format

rgb = np.arange(24).reshape(2, 3, 4)
xw, rows, cols = rgb_to_xw_format(rgb)
rgb2 = xw_to_rgb_format(xw, rows, cols)
```

The function `ie_luminance_to_radiance` generates a spectral radiance
distribution from a target luminance and peak wavelength:

```python
from isetcam import ie_luminance_to_radiance

lum = 10.0
energy, wave = ie_luminance_to_radiance(lum, 360)
```

## Scene Utilities

The Python package also includes a minimal `Scene` dataclass and a
`scene_add` function mirroring MATLAB `sceneAdd`.  A simple usage
pattern is:

```python
from isetcam.scene import Scene, scene_add

s1 = Scene(photons=data1, wave=wave)
s2 = Scene(photons=data2, wave=wave)
combined = scene_add(s1, s2, "add")
```

When multiple scenes are supplied you can optionally provide weights to
accumulate them or remove the spatial mean of individual scenes.

Accessors `scene_get` and `scene_set` retrieve or update values on a
scene instance.  You can also read images directly using
`scene_from_file`.  Integer images are automatically scaled to the
``[0, 1]`` range:

```python
from isetcam.scene import scene_get, scene_set, scene_from_file

sc = scene_from_file('demo.png', mean_luminance=20)
print(scene_get(sc, 'n wave'))
scene_set(sc, 'name', 'demo scene')
```

## Scene Creation

The helper `scene_create` generates simple scenes by name. Available
options include Macbeth charts, uniform monochromatic fields, white
noise patterns and newer types such as frequency sweeps or grid lines:

```python
from isetcam.scene import scene_create

macbeth = scene_create('macbeth d65', patch_size=4)
noise = scene_create('whitenoise', size=8, contrast=0.1)
sweep = scene_create('frequency sweep', size=256)
grid = scene_create('grid lines', spacing=32, thickness=2)
```

Run `pytest -q` to confirm the factory works.
## Slanted Bar Pattern

The functions `img_slanted_bar` and `scene_slanted_bar` generate a slanted bar test target. `img_slanted_bar` creates the binary image while `scene_slanted_bar` wraps it in a `Scene`:

```python
from isetcam.scene.imgtargets import img_slanted_bar
from isetcam.scene import scene_slanted_bar

pattern = img_slanted_bar(im_size=256, bar_slope=3.0)
sc = scene_slanted_bar(im_size=256, bar_slope=3.0, field_of_view=3)
```

Run `pytest -q` after modifying these helpers.


## scene_list

Retrieve the names of example scenes bundled with the package.

```python
from isetcam.scene import scene_list

names = scene_list()
print(len(names))
```

Run `pytest -q` after modifying the listing helper.

Scenes can be manipulated after creation. Use `scene_adjust_luminance` to
scale the luminance statistic and `scene_crop` to extract a region.

## Scene Insert

Insert one scene into another with `scene_insert`:

```python
from isetcam.scene import scene_adjust_luminance, scene_crop, scene_insert

sc2 = scene_adjust_luminance(sc, 'mean', 50)
roi = scene_crop(sc2, (10, 10, 64, 64))
sc3 = scene_insert(sc2, roi, (0, 0))
```

Run `pytest -q` after updating the scene helpers.

## Adjusting Scene Illuminant

The function `scene_adjust_illuminant` multiplies scene photons by a new
illuminant while optionally preserving mean luminance. The illuminant can
be a vector or a MAT-file with `data` and `wavelength` variables:

```python
from isetcam.scene import scene_adjust_illuminant

spd = np.linspace(0.5, 1.0, len(sc.wave))
sc3 = scene_adjust_illuminant(sc, spd)
```

Run `pytest -q` after modifying the scene routines.

## scene_adjust_reflectance

The helper `scene_adjust_reflectance` replaces the scene reflectance
data while leaving the illuminant untouched. The reflectance can be a
uniform vector or a spatial-spectral cube matching the scene photon
array:

```python
from isetcam.scene import scene_adjust_reflectance

new_refl = np.linspace(0.2, 0.8, len(sc.wave))
sc4 = scene_adjust_reflectance(sc, new_refl)
```

Run `pytest -q` after updating the reflectance routines.

## Optical Image Utilities

Optical images are represented by the `OpticalImage` dataclass found in
`isetcam.opticalimage`.  Helper functions mirror the scene accessors and
an `oi_add` routine implements the MATLAB `oiAdd` logic:

```python
from isetcam.opticalimage import OpticalImage, oi_add, get_photons

o1 = OpticalImage(photons=data1, wave=wave)
o2 = OpticalImage(photons=data2, wave=wave)
combined = oi_add(o1, o2, "average")
print(get_photons(combined).shape)
```

Use `oi_get` and `oi_set` to access or modify optical image fields:

```python
from isetcam.opticalimage import oi_get, oi_set

oi_set(o1, 'name', 'primary')
avg_lum = oi_get(o1, 'luminance').mean()
```

Multiple optical images can also be combined with weights or with the
spatial mean removed from each component.

## Optics Dataclass

Basic lens parameters are stored in the `Optics` dataclass located in
`isetcam.optics`. A convenience factory `optics_create` returns a
default instance or loads data by name.

```python
from isetcam.optics import optics_create, Optics

optics = optics_create()
print(optics.f_number)
```

Run `pytest -q` after editing the optics routines.

## Sensor Dataclass

The `Sensor` dataclass located in `isetcam.sensor` stores voltage data,
wavelength sampling and exposure time. Accessor helpers simplify reading
and updating these values:

```python
from isetcam.sensor import (
    Sensor,
    get_volts,
    set_volts,
    get_exposure_time,
    set_exposure_time,
    sensor_get,
    sensor_set,
)

sensor = Sensor(volts=raw_volts, wave=wave, exposure_time=0.01)
sensor_set(sensor, "name", "demo sensor")
nwave = sensor_get(sensor, "n wave")
set_exposure_time(sensor, 0.02)
```

## Pixel Dataclass

A simple `Pixel` dataclass stores pixel geometry and capacity. Use `pixel_get` and `pixel_set` to access the fields.

```python
from isetcam.pixel import Pixel, pixel_get, pixel_set

p = Pixel(width=2e-6, height=2e-6, well_capacity=5000, fill_factor=0.5)
pixel_set(p, "width", 3e-6)
cap = pixel_get(p, "well capacity")
```

Run `pytest -q` after editing the pixel helpers.

## Default Spectrum Initialization

The helper `init_default_spectrum` assigns a standard wavelength
sampling to dataclass objects.  Use it when creating new scenes,
optical images or sensors:

```python
from isetcam import init_default_spectrum
from isetcam.scene import Scene

sc = Scene(photons=data, wave=None)
init_default_spectrum(sc)
print(sc.wave[:3])
```

Remember to run `pytest -q` after adding or modifying code to verify
the tests still pass.

## Loading from MAT-files

You can reconstruct dataclass instances from saved MATLAB structures
using `sensor_from_file` and `oi_from_file`:

```python
from isetcam.sensor import sensor_from_file
from isetcam.opticalimage import oi_from_file

sensor = sensor_from_file("mysensor.mat")
oi = oi_from_file("myoi.mat")
```

After loading, the usual accessor helpers work as expected.  Run
`pytest -q` to confirm the file utilities operate correctly.

## Scene to File and Display from File

Scenes and displays can also be saved or loaded using convenience
functions.

```python
from isetcam.scene import scene_from_file, scene_to_file
from isetcam.display import display_from_file

scene = scene_from_file('demo.png', mean_luminance=20)
scene_to_file(scene, 'scene.mat')
disp = display_from_file('display.mat')
```

## scene_wb_create

Split a scene into single-wavelength MAT-files. When ``scene`` is not
provided, a Macbeth chart is generated using the chosen illuminant and
patch size.

```python
from isetcam.scene import scene_create, scene_wb_create

sc = scene_create('macbeth d65', patch_size=4)
paths = scene_wb_create(sc, 'wb_out')
print(len(paths))
```

Run `pytest -q` after editing the scene white-balance helper.

## Saving Objects to MAT-files

Dataclasses can be written back out to MATLAB compatible files using the
matching ``*_to_file`` helpers.

```python
from isetcam.sensor import sensor_to_file, sensor_from_file
from isetcam.opticalimage import oi_to_file, oi_from_file
from isetcam.display import display_to_file, display_from_file, Display
from isetcam.camera import camera_to_file, Camera

sensor_to_file(sensor, 'mysensor.mat')
oi_to_file(oi, 'myoi.mat')
display_to_file(disp, 'display.mat')
camera_to_file(Camera(sensor=sensor, optical_image=oi), 'cam.mat')
```

Remember to run `pytest -q` after using these I/O helpers.

## DNG Image I/O

Raw sensor data can be stored or loaded using `dng_write` and
`dng_read`. These helpers rely on the optional ``rawpy`` package.
Install it via the corresponding extra:

```bash
pip install -e python[rawpy]
```

```python
from isetcam.io import dng_read, dng_write
import numpy as np

data = (np.arange(12, dtype=np.uint16).reshape(3, 4) * 17) % 65535
dng_write('demo.dng', data)
loaded = dng_read('demo.dng')
```

Run `pytest -q` to confirm the DNG utilities work.

## sensor_dng_read

Read a DNG file directly into a `Sensor` instance.

```python
from isetcam.sensor import sensor_dng_read

sensor = sensor_dng_read('demo.dng')
print(sensor.exposure_time)
```

Run `pytest -q` after updating the DNG sensor loader.

## OpenEXR Image I/O

Floating point images can be saved or loaded using `openexr_write` and
`openexr_read`. These helpers rely on the OpenEXR bindings when
available and fall back to the ``imageio`` backend.
Install the bindings via the extra group:

```bash
pip install -e python[OpenEXR]
```

```python
from isetcam.io import openexr_read, openexr_write

openexr_write('img.exr', {'R': rgb[:, :, 0], 'G': rgb[:, :, 1], 'B': rgb[:, :, 2]})
channels = openexr_read('img.exr')
```

Run `pytest -q` to confirm the EXR utilities work.

## sensor_to_exr

Write sensor volt data to an OpenEXR file.

```python
from isetcam.sensor import Sensor, sensor_to_exr

path = "sensor.exr"
sensor_to_exr(sensor, path)
```

Run `pytest -q` after editing the EXR export helper.

## Multispectral Image I/O

Use `ie_save_multispectral_image` and `ie_load_multispectral_image` to write or read multispectral data cubes.

```python
from isetcam.io import ie_save_multispectral_image, ie_load_multispectral_image

ie_save_multispectral_image("cube.mat", coeffs, basis)
cube = ie_load_multispectral_image("cube.mat")
```

Run `pytest -q` after editing the multispectral I/O helpers.


## Updated Tests

Unit tests in `python/tests` exercise the conversion helpers, format
utilities and the dataclasses for scenes, optical images and sensors.
Run `pytest -q` to verify that all tests pass:

```bash
export PYTHONPATH=$PWD/python
pytest -q
```

## Session Helpers

The global session dictionary mirrors the MATLAB `vcSESSION` structure. Use
`ie_session_get` and `ie_session_set` to query or modify values:

```python
from isetcam import ie_init, ie_session_get, ie_session_set

session = ie_init()
ie_session_set('name', 'demo')
print(ie_session_get('name'))
```

You can also store or retrieve the currently selected object type using the
`selected` parameter.

## XYZ and Chromaticity Conversions

Color calculations are provided through the following helpers:

* `ie_xyz_from_energy` – compute CIE XYZ from spectral energy
* `ie_xyz_from_photons` – compute CIE XYZ from photon data
* `chromaticity` – convert XYZ values to (x, y) chromaticities

```python
import numpy as np
from isetcam import (
    energy_to_quanta,
    ie_xyz_from_energy,
    ie_xyz_from_photons,
    chromaticity,
)

wave = np.arange(400, 701, 10)
energy = np.ones((1, len(wave)))
xyz = ie_xyz_from_energy(energy, wave)
photons = energy_to_quanta(wave, energy.T).T
xyz2 = ie_xyz_from_photons(photons, wave)
xy = chromaticity(xyz)
```

Remember to run the Python unit tests via `pytest` after installing the
environment to ensure these functions behave as expected.

## Basic Pipeline Notebook

A short Jupyter notebook demonstrates constructing a scene, computing an optical image, simulating a sensor and rendering the result.
See [notebooks/basic_pipeline.ipynb](../notebooks/basic_pipeline.ipynb) for the full workflow. Validate it using the ``nbval`` plugin:

```bash
pytest --nbval notebooks/basic_pipeline.ipynb
```

After running the notebook, execute the unit tests with ``pytest -q``.

## Display Dataclass

Displays are represented by a small `Display` dataclass found in
`isetcam.display`.  Use `display_get` and `display_set` to retrieve or
update values. The accessors now support gamma tables in addition to SPD,
wave and name fields:

```python
import numpy as np
from isetcam.display import Display, display_get, display_set

wave = np.arange(400, 701, 10)
spd = np.ones((len(wave), 3))
gamma = np.linspace(0, 1, len(wave)).reshape(-1, 1).repeat(3, axis=1)
disp = Display(spd=spd, wave=wave, gamma=gamma, name="lcd")
display_set(disp, "name", "main display")
n_wave = display_get(disp, "n wave")
print(display_get(disp, "gamma").shape)
```

A convenience factory `display_create` loads calibration data by name:

```python
from isetcam.display import display_create

default_disp = display_create()
lcd = display_create("lcdExample")
```

## Updated Display Accessors

`display_get` and `display_set` now handle a `gamma` table in addition to
`spd`, `wave` and `name`.  Set the gamma to `None` to remove it:

```python
from isetcam.display import display_get, display_set

display_set(disp, "gamma", None)
print(display_get(disp, "gamma"))
```

Run `pytest -q` to ensure the display utilities behave correctly.

## Illuminant Helpers

Illuminant spectral data are provided through the `Illuminant` dataclass
and factory helpers in `isetcam.illuminant`:

```python
from isetcam.illuminant import illuminant_create, illuminant_blackbody

illum = illuminant_create("D65")
bb_spd = illuminant_blackbody(6500, illum.wave)
```

## Illuminant File Utilities

Use `illuminant_to_file` and `illuminant_from_file` to write or read an
`Illuminant` from a simple MAT-file:

```python
from isetcam.illuminant import (
    Illuminant,
    illuminant_to_file,
    illuminant_from_file,
)

illum = Illuminant(spd=np.ones(4), wave=np.arange(4))
illuminant_to_file(illum, "illum.mat")
reloaded = illuminant_from_file("illum.mat")
```

Run `pytest -q` after editing the illuminant I/O helpers.

## Session Persistence

The global session dictionary can be serialized to disk and reloaded via
`ie_save_session` and `ie_load_session`:

```python
from isetcam import ie_init, ie_save_session, ie_load_session

session = ie_init()
session["name"] = "temp"
ie_save_session(session, "session.json")
loaded = ie_load_session("session.json")
```

## Color Transformation Matrix

Use `ie_color_transform` to compute a linear transform from sensor
quantum efficiency to a color space such as XYZ or linear sRGB:

```python
import numpy as np
from isetcam import ie_color_transform
from isetcam.illuminant import illuminant_create

wave = np.arange(400, 701, 10)
qe = np.stack([
    np.exp(-0.5 * ((wave - 450) / 20) ** 2),
    np.exp(-0.5 * ((wave - 550) / 20) ** 2),
    np.exp(-0.5 * ((wave - 650) / 20) ** 2),
], axis=1)
illum = illuminant_create("D65", wave).spd
T = ie_color_transform(qe, wave, "srgb", illum)
```

The helper `color_transform_matrix` can also return predefined matrices or
fit one from sample data:

```python
from isetcam import color_transform_matrix

M = color_transform_matrix('xyz2srgb')
M2 = color_transform_matrix(src=src, dst=dst, offset=True)
```

After adding these modules remember to run the unit tests again with
`pytest -q` to confirm everything works.

## Color Transform Matrix Create

`color_transform_matrix_create` derives a least-squares transform from
sample spectral data.

```python
import numpy as np
from isetcam import color_transform_matrix_create

src = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
dst = src @ np.array([[1.0, 2.0], [-1.0, 0.5]])
T = color_transform_matrix_create(src, dst)
```

Run `pytest -q` after editing the matrix routines.

## Color Block Matrix

Use `color_block_matrix` to visualize a spectral distribution as RGB values.
The default matrix spans 400--700 nm in 10 nm steps.  Other wavelength
sampling is handled through interpolation with optional extrapolation for
out‑of‑range values.

```python
from isetcam import color_block_matrix

wave = np.arange(400, 701, 10)
B = color_block_matrix(wave)

wave2 = np.array([350, 400, 500, 650, 750])
B2 = color_block_matrix(wave2, extrap_val=0.1)
```

Run `pytest -q` after modifying the block matrix routine.

## Internal Color to Display Transform

`ie_internal_to_display` computes a matrix that maps values in an internal
color space to RGB intensities for a particular display.

```python
import numpy as np
from isetcam.imgproc import ie_internal_to_display

T = ie_internal_to_display(cmf, spd)
```

Run `pytest -q` whenever you update the color transform routines.
## Scotopic Luminance

The function `scotopic_luminance_from_energy` computes scotopic luminance from a spectral energy distribution.

```python
import numpy as np
from isetcam import scotopic_luminance_from_energy

wave = np.arange(400, 701, 10)
energy = np.ones((1, len(wave))) * 1e-4
lum = scotopic_luminance_from_energy(energy, wave)
```

`scotopic_luminance_from_photons` performs the same calculation when the input
data are photon counts.

```python
from isetcam import energy_to_quanta, scotopic_luminance_from_photons

photons = energy_to_quanta(wave, energy.T).T
lum2 = scotopic_luminance_from_photons(photons, wave)
```

Run `pytest -q` after editing the scotopic luminance routines.

## XYZ and L\*a\*b\* Conversions

Use `xyz_to_lab` and `lab_to_xyz` to convert between XYZ tristimulus values and CIE L\*a\*b\*.

```python
import numpy as np
from isetcam import xyz_to_lab, lab_to_xyz

white = np.array([0.95047, 1.0, 1.08883])
xyz = np.random.rand(2, 3, 3)
lab = xyz_to_lab(xyz, white)
xyz2 = lab_to_xyz(lab, white)
```

Chromaticity and CIELUV coordinates can also be computed:

```python
from isetcam import xyz_to_uv, xyz_to_luv

uv = xyz_to_uv(xyz)
luv = xyz_to_luv(xyz, white)
```

## xyY Conversions

Convert between XYZ tristimulus values and xyY coordinates using
`xyz_to_xyy` and `xyy_to_xyz`:

```python
from isetcam import xyz_to_xyy, xyy_to_xyz

xyy = xyz_to_xyy(xyz)
xyz2 = xyy_to_xyz(xyy)
```

These helpers preserve the array shape and are tested via
`pytest -q`.

## sRGB and XYZ

The helpers `srgb_to_xyz` and `xyz_to_srgb` convert between sRGB and CIE XYZ.

```python
import numpy as np
from isetcam import srgb_to_xyz, xyz_to_srgb

srgb = np.random.rand(4, 3)
xyz = srgb_to_xyz(srgb)
srgb2, lrgb, maxY = xyz_to_srgb(xyz)
```

## sRGB and Linear RGB

Use `srgb_to_lrgb` and `lrgb_to_srgb` to convert between nonlinear sRGB
values and linear RGB.

```python
import numpy as np
from isetcam import srgb_to_lrgb, lrgb_to_srgb

srgb = np.random.rand(4, 3)
lrgb = srgb_to_lrgb(srgb)
srgb2 = lrgb_to_srgb(lrgb)
```

Run `pytest -q` to ensure these color transforms work properly.

## LMS Conversions

Functions `xyz_to_lms`, `lms_to_xyz`, `srgb_to_lms` and `lms_to_srgb`
convert among XYZ, LMS and sRGB representations:

```python
from isetcam import (
    xyz_to_lms,
    lms_to_xyz,
    srgb_to_lms,
    lms_to_srgb,
)

lms = xyz_to_lms(xyz)
xyz2 = lms_to_xyz(lms)
srgb2 = lms_to_srgb(lms)
lms2 = srgb_to_lms(srgb)
```

Run `pytest -q` to ensure these color transforms remain valid.

## sRGB and L*a*b*

Convert between nonlinear sRGB values and CIE L\*a\*b\* using
`srgb_to_lab` and `lab_to_srgb`:

```python
import numpy as np
from isetcam import srgb_to_lab, lab_to_srgb

white = np.array([0.95047, 1.0, 1.08883])
srgb = np.random.rand(2, 2, 3)
lab = srgb_to_lab(srgb, white)
srgb2 = lab_to_srgb(lab, white)
```

Run `pytest -q` after updating these color transforms.

## RGB and YCbCr

`rgb_to_ycbcr` and `ycbcr_to_rgb` convert between RGB arrays and the YCbCr
representation used in video processing.

```python
import numpy as np
from isetcam import rgb_to_ycbcr, ycbcr_to_rgb

rgb = np.random.rand(4, 3)
ycbcr = rgb_to_ycbcr(rgb)
rgb2 = ycbcr_to_rgb(ycbcr)
```

Remember to run `pytest -q` after modifying these conversion helpers.

## RGB and HSV

`rgb_to_hsv` and `hsv_to_rgb` convert between linear RGB values and the
HSV representation.

```python
import numpy as np
from isetcam import rgb_to_hsv, hsv_to_rgb

rgb = np.random.rand(2, 2, 3)
hsv = rgb_to_hsv(rgb)
rgb2 = hsv_to_rgb(hsv)
```

## RGB and HSL

`rgb_to_hsl` and `hsl_to_rgb` transform RGB arrays to or from the HSL
color model.

```python
from isetcam import rgb_to_hsl, hsl_to_rgb

hsl = rgb_to_hsl(rgb)
rgb3 = hsl_to_rgb(hsl)
```

Run `pytest -q` after updating these color conversions.

## lstar_to_y

Convert CIE L\* values back to luminance using ``lstar_to_y``. The
function accepts L\* in either ``(n,)`` or image format and requires the
luminance of the reference white point.

```python
import numpy as np
from isetcam import lstar_to_y

L = np.array([50, 80])
Y = lstar_to_y(L, 100.0)
```

Run `pytest -q` after updating the L\* conversion helper.

## Daylight Spectra

`cct_to_sun` generates a daylight spectral distribution for a desired correlated color temperature.

```python
import numpy as np
from isetcam import cct_to_sun

wave = np.arange(380, 781, 5)
spd = cct_to_sun(wave, 6500)
```

## Circle Sampling

Call `circle_points` to obtain evenly spaced coordinates on a unit circle.

```python
from isetcam import circle_points

x, y = circle_points()
```

After adding these modules or experimenting with them remember to run `pytest -q` to verify the Python tests pass.

## sRGB to CCT

Use `srgb_to_cct` to estimate the correlated color temperature from an sRGB image.

```python
import numpy as np
from isetcam import srgb_to_cct

srgb = np.random.rand(10, 10, 3)
temp, table = srgb_to_cct(srgb)
```

Run `pytest -q` to confirm the color temperature routine functions correctly.
## XYZ to CCT

`xyz_to_cct` estimates the correlated color temperature directly from XYZ values.

```python
import numpy as np
from isetcam import xyz_to_cct

xyz = np.random.rand(4, 3)
temps = xyz_to_cct(xyz)
```

Run `pytest -q` when modifying this conversion helper.


## Color Temperature to sRGB

`ctemp_to_srgb` converts a blackbody color temperature to an sRGB white point.

```python
from isetcam import ctemp_to_srgb

srgb = ctemp_to_srgb(6500)
```

Run `pytest -q` after modifying the temperature conversion helper.

## Camera Dataclass

A `Camera` bundles a sensor with an optical image. Accessor helpers retrieve or update fields just like the other dataclasses.

```python
from isetcam.camera import Camera, camera_get, camera_set
from isetcam.sensor import Sensor
from isetcam.opticalimage import OpticalImage

cam = Camera(
    sensor=Sensor(volts=raw_volts, exposure_time=0.01, wave=wave),
    optical_image=OpticalImage(photons=oi_photons, wave=wave),
    name="demo cam",
)
camera_set(cam, "name", "main camera")
print(camera_get(cam, "n wave"))
```

Remember to run `pytest -q` after experimenting with the camera helpers.

## Sensor and Camera Creation

Factory helpers build dataclass instances with default parameters.

```python
from isetcam.sensor import sensor_create
from isetcam.camera import camera_create

sensor = sensor_create()
cam = camera_create(sensor=sensor)
```

Run `pytest -q` to verify these factories.

## Scene and Optical Image Spatial Support

Helpers `scene_spatial_support` and `oi_spatial_support` return the spatial
coordinates of each sample. Use `scene_spatial_resample` and
`oi_spatial_resample` to change the pixel spacing while keeping the field of
view constant.

```python
from isetcam.scene import scene_spatial_support, scene_spatial_resample
from isetcam.opticalimage import oi_spatial_support, oi_spatial_resample

sup = scene_spatial_support(sc, "mm")
sc2 = scene_spatial_resample(sc, 0.5e-3, method="nearest")
oi_sup = oi_spatial_support(oi)
oi2 = oi_spatial_resample(oi, 1e-3)
```

Run `pytest -q` after editing the spatial routines.

## Scene Adjust Pixel Size

`scene_adjust_pixel_size` sets the scene distance so its sample spacing
matches a desired sensor pixel size and updates the field of view.

```python
from isetcam.scene import scene_adjust_pixel_size

sc, new_d = scene_adjust_pixel_size(sc, oi, 2e-6)
```

Run `pytest -q` when modifying the pixel size helper.

## Scene Frequency Support

`scene_frequency_support` returns the spatial frequency grid for a scene.
`scene_frequency_resample` changes the frequency resolution while
preserving the field of view.

```python
from isetcam.scene import scene_frequency_support, scene_frequency_resample

f_sup = scene_frequency_support(sc)
sc_f = scene_frequency_resample(sc, 32, 32)
```

Run `pytest -q` after modifying the scene frequency helpers.

## Optical Image Frequency Support

Use `oi_frequency_support` to obtain the frequency grid of an optical
image and `oi_frequency_resample` to adjust the number of frequency
samples.

```python
from isetcam.opticalimage import oi_frequency_support, oi_frequency_resample

oi_f_sup = oi_frequency_support(oi)
oi_f = oi_frequency_resample(oi, 64, 64)
```

Remember to run `pytest -q` once these routines are updated.

## Scene and Optical Image Padding

Scenes and optical images can be padded, shifted or cropped using small helper functions.

```python
from isetcam.scene import scene_pad, scene_translate
from isetcam.opticalimage import oi_crop, oi_pad

padded_scene = scene_pad(sc, 8)
shifted_scene = scene_translate(sc, 4, -4)
cropped_oi = oi_crop(oi, (10, 10, 64, 64))
padded_oi = oi_pad(oi, (20, 20))
```

These utilities mirror the MATLAB equivalents and are covered by the unit tests. Run `pytest -q` after modifying them.

## oi_translate

Shift an optical image by whole pixels using `oi_translate`:

```python
from isetcam.opticalimage import OpticalImage, oi_translate

shifted = oi_translate(oi, 4, -2, fill=0)
```

Run `pytest -q` after updating the translation helper.

## Demosaicing Helpers

The `ie_nearest_neighbor` and `ie_bilinear` functions in
`isetcam.imgproc` convert a Bayer mosaic into an RGB image using simple
interpolation strategies.

```python
from isetcam.imgproc import ie_nearest_neighbor, ie_bilinear

rgb_nn = ie_nearest_neighbor(bayer, "rggb")
rgb_bl = ie_bilinear(bayer, "rggb")
```

Run `pytest -q` after changing the demosaicing routines.

## adaptive_laplacian

`adaptive_laplacian` implements a higher quality demosaic algorithm.

```python
from isetcam.imgproc.demosaic import adaptive_laplacian

rgb_al = adaptive_laplacian(bayer, "rggb")
```

Run `pytest -q` after updating the demosaicing code.

## ip_demosaic

`ip_demosaic` dispatches to one of the demosaicing algorithms based on a
method string.

```python
from isetcam.ip import ip_demosaic

rgb = ip_demosaic(bayer, "rggb", method="adaptive")
```

Remember to run `pytest -q` when modifying the demosaic wrapper.
## Faulty Pixel Correction

Utilities `faulty_insert` and `faulty_pixel_correction` help test and repair malfunctioning pixels.

```python
import numpy as np
from isetcam.imgproc.demosaic.faulty_pixel import (
    faulty_insert,
    faulty_pixel_correction,
)

bad = np.array([[1, 1], [2, 2]])
noisy = faulty_insert(bad, bayer, val=1)
fixed = faulty_pixel_correction(bad, noisy, "rggb")
```

Run `pytest -q` to verify the faulty pixel routines.

## Image Distortion and PSNR

The module `isetcam.imgproc` includes a simple `image_distort` routine. Use `ie_psnr` from `isetcam.metrics` to evaluate image quality.

```python
from isetcam.imgproc import image_distort
from isetcam.metrics import ie_psnr

distorted = image_distort(img, "gaussian noise", 10)
score = ie_psnr(img, distorted)
print(f"PSNR: {score:.2f} dB")
```

As always, run `pytest -q` to confirm these functions behave as expected.

## Basic Pipeline Notebook

A short Jupyter notebook demonstrates constructing a scene, computing an optical image, simulating a sensor and rendering the result.
See [notebooks/basic_pipeline.ipynb](../notebooks/basic_pipeline.ipynb) for the full workflow. Validate it using the ``nbval`` plugin:

```bash
pytest --nbval notebooks/basic_pipeline.ipynb
```

Run ``pytest -q`` afterwards to execute the unit tests.


## Structural Similarity (SSIM)

Use `ssim_metric` to compute the structural similarity index and map
between two images.

```python
from isetcam.metrics import ssim_metric

score, ssim_map = ssim_metric(img1, img2)
```

Run `pytest -q` after modifying the SSIM implementation.
## Scene and Optical Image Rotation

The helpers `scene_rotate` and `oi_rotate` rotate photon data while optionally filling empty regions. Pass an angle in degrees.

```python
from isetcam.scene import scene_rotate
from isetcam.opticalimage import oi_rotate

rotated_sc = scene_rotate(sc, 45, fill=0.5)
rotated_oi = oi_rotate(oi, -30)
```

Run `pytest -q` to verify the rotation routines.

## Display Gamma Correction

Use `display_apply_gamma` to convert between digital counts and linear values based on a display's gamma table.

```python
import numpy as np
from isetcam.display import Display, display_apply_gamma

gamma = np.linspace(0, 1, 256).reshape(-1, 1)
disp = Display(gamma=gamma)
lin = display_apply_gamma(dac_img, disp, inverse=True)
dac = display_apply_gamma(lin, disp)
```

Remember to run `pytest -q` after editing the display helpers.

## Inverse Gamma Table

`mk_inv_gamma_table` generates a lookup table mapping linear values back to
digital counts. This is helpful when converting images to the display domain.

```python
import numpy as np
from isetcam import mk_inv_gamma_table

gamma = np.linspace(0, 1, 4)
inv = mk_inv_gamma_table(gamma)
```

Run `pytest -q` after changing the gamma utilities.

## ie_scale and ie_scale_columns

Use `ie_scale` to normalize an array into a desired range. The
`ie_scale_columns` helper applies the same logic to each column of a
matrix.

```python
import numpy as np
from isetcam import ie_scale, ie_scale_columns

data = np.array([0.0, 1.0, 2.0])
scaled, mn, mx = ie_scale(data, -1.0, 1.0)

M = np.arange(6).reshape(3, 2)
M_scaled = ie_scale_columns(M, 0.0, 1.0)
```

Run `pytest -q` after editing the scaling helpers.

## Scene, Optical Image and Sensor Photon Noise

`scene_photon_noise`, `oi_photon_noise` and `sensor_photon_noise` add
Poisson noise to the photon or voltage data stored in a scene, optical
image or sensor.

```python
from isetcam.scene import scene_photon_noise
from isetcam.opticalimage import oi_photon_noise
from isetcam.sensor import sensor_photon_noise

noisy_sc, sc_noise = scene_photon_noise(sc)
noisy_oi, oi_noise = oi_photon_noise(oi)
noisy_s, s_noise = sensor_photon_noise(sensor)
```

Run `pytest -q` after modifying the noise utilities.

## Sensor Photon Noise

The helper `sensor_photon_noise` adds Poisson noise directly to the
volt data stored in a sensor instance.

```python
from isetcam.sensor import sensor_photon_noise

noisy_s, noise = sensor_photon_noise(sensor)
```

Remember to run `pytest -q` after adjusting the sensor noise routines.

## sensor_add_noise

Add DSNU and PRNU noise to a sensor voltage array.

```python
from isetcam.sensor import Sensor, sensor_set, sensor_add_noise
import numpy as np

s = Sensor(volts=np.ones((4, 4)), wave=np.array([550]), exposure_time=0.01)
sensor_set(s, 'gain_sd', 5.0)
sensor_set(s, 'offset_sd', 0.1)
noisy, noise = sensor_add_noise(s)
```

Run `pytest -q` after modifying the noise model.

## sensor_pixel_coord and sensor_jiggle

`sensor_pixel_coord` returns the pixel centre coordinates relative to the
sensor origin. Use `sensor_jiggle` to shift sensor voltage data by whole
pixels while recording the accumulated offset.

```python
import numpy as np
from isetcam.sensor import Sensor, sensor_jiggle, sensor_pixel_coord

s = Sensor(volts=np.zeros((3, 3)), wave=np.array([550]), exposure_time=0.01)
x0, y0 = sensor_pixel_coord(s)
shifted = sensor_jiggle(s, 1, -1)
x1, y1 = sensor_pixel_coord(shifted)
```

Remember to run `pytest -q` after editing these sensor helpers.

## ie_poisson, ie_exprnd, ie_normpdf and ie_prctile

Basic statistical helpers replicate MATLAB behavior. ``ie_poisson``
generates Poisson samples, ``ie_exprnd`` draws exponential random
values, ``ie_normpdf`` evaluates the normal distribution and
``ie_prctile`` computes percentiles along the first dimension.

```python
import numpy as np
from isetcam import (
    ie_poisson,
    ie_exprnd,
    ie_normpdf,
    ie_prctile,
)

vals, seed = ie_poisson(5, n_samp=2)
exp = ie_exprnd(1.5, (3, 1))
pdf = ie_normpdf(np.linspace(-1, 1, 5))
p50 = ie_prctile(exp, 50)
```

Run `pytest -q` after editing the statistical helpers.

## SCIELAB Color Difference

The `scielab` metric provides a perceptual color difference measure in the spatial domain.

```python
from isetcam.metrics import scielab, sc_params

params = sc_params()
de = scielab(img1, img2, [0.95047, 1.0, 1.08883], params)
```

Run `pytest -q` to ensure the metric operates correctly.

## Delta E Metrics

Color difference calculations are also available through several helpers:

```python
from isetcam.metrics import (
    delta_e_ab,
    delta_e_94,
    delta_e_2000,
    delta_e_uv,
)

de2000 = delta_e_2000(lab1, lab2)
de94 = delta_e_94(lab1, lab2)
de76 = delta_e_ab(lab1, lab2, "1976")
deuv = delta_e_uv(luv1, luv2)
```

Remember to run `pytest -q` after working with the color difference metrics.
## color_rendering_index

`color_rendering_index` computes the CIE color rendering index for test and reference spectra.

```python
cri = color_rendering_index(test_spd, ref_spd, wave)
```

Run `pytest -q` after editing the CRI calculations.

## cie_whiteness

The function `cie_whiteness` evaluates material whiteness from XYZ data or spectral reflectance.

```python
import numpy as np
from isetcam.metrics import cie_whiteness

xyz = np.array([[0.9, 1.0, 1.1]])
W = cie_whiteness(xyz)
```

Run `pytest -q` after updating the whiteness calculation.


## Visual Signal-to-Noise Ratio

`xyz_to_vsnr` computes the visual SNR of an XYZ region of interest.

```python
import numpy as np
from isetcam.metrics import xyz_to_vsnr, SCIELABParams

roi = np.random.rand(32, 32, 3)
white = np.array([1.0, 1.0, 1.0])
score = xyz_to_vsnr(roi, white)
```

Run `pytest -q` after modifying the VSNR implementation.

## Responsivity Unit Conversion

`ie_responsivity_convert` converts spectral responsivity curves between energy
and photon units.

```python
import numpy as np
from isetcam import ie_responsivity_convert

resp_q, scale = ie_responsivity_convert(resp, wave, "e2q")
```

Remember to run `pytest -q` when editing responsivity helpers.

## Sensor Compute

`sensor_compute` integrates the photons from an optical image to produce sensor volts.

```python
from isetcam.sensor import Sensor, sensor_compute
from isetcam.opticalimage import OpticalImage

sensor = Sensor(volts=np.zeros((2, 2)), wave=oi.wave, exposure_time=0.01)
sensor_compute(sensor, oi)
print(sensor.volts)
```

As always, run `pytest -q` after adding or modifying sensor routines.

## Camera Compute Sequence

`camera_compute_sequence` renders a camera for multiple scenes and exposure times, returning the captured images.

```python
from isetcam.camera import camera_create, camera_compute_sequence
from isetcam.scene import scene_create

cam = camera_create()
sc = scene_create('uniform', size=8)
cam, frames = camera_compute_sequence(cam, scenes=sc, exposure_times=[0.5, 1.0], n_frames=2)
```

Run `pytest -q` after changing the sequence routine.

## Sensor Plot

Use `sensor_plot` to visualize a sensor voltage image and optionally overlay the
color filter array.

```python
import numpy as np
from isetcam.sensor import Sensor, sensor_plot

s = Sensor(volts=np.random.rand(4, 4), wave=np.array([550]), exposure_time=0.01)
ax = sensor_plot(s, show_filters=True)
```

Run `pytest -q` to exercise the plotting helper.

## AdobeRGB Parameters

Use `adobergb_parameters` to obtain chromaticity, luminance and white
point values defined by the Adobe RGB standard.

```python
from isetcam import adobergb_parameters

params = adobergb_parameters()
xyy_white = adobergb_parameters("xyywhite")
```

Run `pytest -q` after updating the color space helpers.

## Adjust Optical Image Illuminance

The routine `oi_adjust_illuminance` scales an optical image so its mean
illuminance matches a desired level.

```python
from isetcam.opticalimage import OpticalImage, oi_adjust_illuminance

oi = OpticalImage(photons=data, wave=wave)
scaled = oi_adjust_illuminance(oi, 100.0)
```

Remember to run `pytest -q` after editing the illuminance utilities.

## oi_calculate_irradiance and oi_calculate_illuminance

Use `oi_calculate_irradiance` to integrate the spectral photon data of an
optical image and return an irradiance map.

```python
from isetcam.opticalimage import OpticalImage, oi_calculate_irradiance,
oi_calculate_illuminance

oi = OpticalImage(photons=data, wave=wave)
irr = oi_calculate_irradiance(oi)
lux = oi_calculate_illuminance(oi)
```

Run `pytest -q` after updating the irradiance helpers.

## Bayer Indices

`bayer_indices` returns the column and row positions of each color in a
Bayer mosaic for a given CFA pattern and image size.

```python
from isetcam.imgproc.demosaic import bayer_indices

rx, ry, bx, by, g1x, g1y, g2x, g2y = bayer_indices("rggb", (4, 4))
```

Run `pytest -q` after modifying the demosaicing helpers.

## Exposure Value

Call `exposure_value` to compute the photographic exposure value from an
F-number and shutter time.

```python
from isetcam import exposure_value

ev = exposure_value(2.8, 1 / 60)
```

Remember to run `pytest -q` when changing the metric routines.

## Chromaticity Plot

`chromaticity_plot` displays the CIE xy chromaticity diagram and optional
points.

```python
import numpy as np
from isetcam import chromaticity_plot

x = np.array([0.3, 0.4])
y = np.array([0.3, 0.4])
ax = chromaticity_plot(x, y)
```

Run `pytest -q` after updating the plotting utilities.

## ie_hist_image and ie_format_figure

`ie_hist_image` plots histograms for grayscale or RGB images while
`ie_format_figure` applies ISETCam styling to an existing Matplotlib
axis.

```python
import numpy as np
from isetcam import ie_hist_image, ie_format_figure

img = np.random.rand(32, 32, 3)
ax = ie_hist_image(img, bins=50)
ie_format_figure(ax, xlabel="Value", ylabel="Count", grid=True)
```

Run `pytest -q` after implementing these plotting utilities.

## Reading Spectral Data

`ie_read_spectra` loads spectral measurements from a MAT-file. Provide an optional wavelength vector to interpolate the data.

```python
from isetcam import ie_read_spectra

spd, wave, comment, path = ie_read_spectra("filters.mat", range(400, 701, 10))
```

Run `pytest -q` after editing the I/O helpers.

## Extracting Wavebands

Use `scene_extract_waveband` and `oi_extract_waveband` to subset scenes or optical images by wavelength.

```python
from isetcam.scene import scene_extract_waveband
from isetcam.opticalimage import oi_extract_waveband

sc_band = scene_extract_waveband(scene, [450, 550])
oi_band = oi_extract_waveband(oi, [450, 550], illuminance=True)
```

Run `pytest -q` to confirm the waveband helpers work.

## Adding and Selecting Objects

`vc_add_and_select_object` stores an object in the global session and marks it as selected.

```python
from isetcam import ie_init, vc_add_and_select_object

session = ie_init()
index = vc_add_and_select_object("scene", my_scene)
```

Run `pytest -q` after changing session utilities.

## Sensor Signal-to-Noise Ratio

`sensor_snr` returns SNR versus voltage while `sensor_snr_luxsec` converts the values to photometric exposure.

```python
from isetcam.sensor import sensor_snr, sensor_snr_luxsec

snr, volts, *_ = sensor_snr(sensor)
snr_lux, luxsec = sensor_snr_luxsec(sensor)
```

Remember to run `pytest -q` after updating the sensor analysis routines.

## Camera MTF

Use `camera_mtf` to compute the modulation transfer function of a camera model based on its sensor and optics.

```python
from isetcam.camera import camera_mtf

freqs, mtf = camera_mtf(camera)
```

Run `pytest -q` after editing camera utilities.

## Scene Add Grid

`scene_add_grid` overlays black grid lines on a scene's photon data.

```python
from isetcam.scene import scene_add_grid

gridded = scene_add_grid(scene, (16, 16), g_width=2)
```

Run `pytest -q` after updating the grid helper.

## Scene Combine

`scene_combine` joins two scenes horizontally, vertically or in a grid.

```python
from isetcam.scene import scene_combine

combined = scene_combine(scene1, scene2, "horizontal")
```

Run `pytest -q` after modifying the combination utilities.

## scene_show_image and oi_show_image

`scene_show_image` converts scene photons to an sRGB image and displays
it with Matplotlib. `oi_show_image` renders an optical image in the same
way using an optional display model.

```python
from isetcam.scene import Scene, scene_show_image
from isetcam.opticalimage import OpticalImage, oi_show_image

sc = Scene(photons=np.ones((1, 1, 3)), wave=np.array([500, 600, 700]))
ax = scene_show_image(sc)

oi = OpticalImage(photons=sc.photons, wave=sc.wave)
ax2 = oi_show_image(oi)
```

Run `pytest -q` after updating the image display helpers.

## scene_save_image and oi_save_image

`scene_save_image` writes an sRGB rendering of a scene to disk while
`oi_save_image` performs the same operation for an optical image.

```python
from isetcam.scene import scene_save_image
from isetcam.opticalimage import oi_save_image

scene_save_image(sc, "scene.png")
oi_save_image(oi, "oi.png")
```

Remember to run `pytest -q` after modifying the image saving routines.

## scene_illuminant_pattern and oi_illuminant_pattern

These helpers multiply the photons and illuminant by a spatial pattern
for scenes or optical images.

```python
import numpy as np
from isetcam.scene import scene_illuminant_pattern
from isetcam.opticalimage import oi_illuminant_pattern

pattern = np.array([[1.0, 0.5], [0.5, 1.0]])
sc2 = scene_illuminant_pattern(sc, pattern)
oi2 = oi_illuminant_pattern(oi, pattern)
```

Run `pytest -q` to verify the illuminant helpers.

## scene_thumbnail and oi_thumbnail

`scene_thumbnail` and `oi_thumbnail` create small sRGB previews of a
scene or optical image.

```python
from isetcam.scene import scene_thumbnail
from isetcam.opticalimage import oi_thumbnail

thumb_scene = scene_thumbnail(sc, size=(16, 16))
thumb_oi = oi_thumbnail(oi, size=(8, 8))
```

Run `pytest -q` after modifying the thumbnail helpers.

## scene_plot, oi_plot and ip_plot

These helpers visualize scenes, optical images and IP results.
`scene_plot` displays luminance or radiance profiles and rendered
images. `oi_plot` shows irradiance or illuminance information for an
optical image. `ip_plot` renders data stored in a `VCImage`.

```python
import numpy as np
from isetcam.scene import Scene, scene_plot
from isetcam.opticalimage import OpticalImage, oi_plot
from isetcam.ip import VCImage, ip_plot

sc = Scene(photons=np.ones((8, 8, 3)), wave=np.array([500, 600, 700]))
ax1 = scene_plot(sc, kind="radiance image with grid", grid_spacing=4)

oi = OpticalImage(photons=sc.photons, wave=sc.wave)
ax2 = oi_plot(oi, kind="irradiance hline", loc=2)

ip = VCImage(rgb=np.random.rand(8, 8, 3), wave=sc.wave)
ax3 = ip_plot(ip, kind="image")
```

Run `pytest -q` after implementing these plotting utilities.

## Sensor Crop

Use `sensor_crop` to extract a voltage region while keeping the 2x2 CFA
alignment.

```python
from isetcam.sensor import sensor_crop

cropped = sensor_crop(sensor, (0, 0, 128, 128))
```

Remember to run `pytest -q` after editing the sensor routines.

## sensor_roi

Return a rectangular ROI and its row and column indices.

```python
import numpy as np
from isetcam.sensor import Sensor, sensor_roi

s = Sensor(volts=np.arange(16).reshape(4, 4), wave=np.array([550]), exposure_time=0.01)
roi_volts, rows, cols = sensor_roi(s, (1, 1, 2, 2))
```

Run `pytest -q` after updating the ROI helper.

## Optical Image Compute

`oi_compute` forms an optical image from a scene using an optics model.

```python
from isetcam.opticalimage import oi_compute
from isetcam.optics import Optics

oi = oi_compute(scene, Optics(f_number=2.8, f_length=5.0, wave=scene.wave))
```

Run `pytest -q` to confirm the optical image calculations.

## Camera VSNR

`camera_vsnr` estimates the visible SNR for a camera imaging a scene.

```python
from isetcam.camera import camera_create, camera_vsnr

cam = camera_create()
score = camera_vsnr(cam, scene)
```

Run `pytest -q` after modifying the VSNR routines.

## Camera Acutance and Color Accuracy

`camera_acutance` evaluates the ISO acutance from a camera's MTF while `camera_color_accuracy` measures luminance differences for a Macbeth chart scene.

```python
from isetcam.camera import (
    camera_create,
    camera_acutance,
    camera_color_accuracy,
)

cam = camera_create()
val = camera_acutance(cam)
metrics, cam = camera_color_accuracy(cam, lum=50, patch_size=4)
```

Run `pytest -q` after updating these camera metrics.
## camera_plot and camera_moire

The `camera_plot` routine displays the sensor response together with the camera MTF. `camera_moire` synthesizes a radial sinusoid to test aliasing.

```python
from isetcam.camera import camera_plot, camera_moire, camera_create

cam = camera_create()
pattern, cam = camera_moire(cam, size=128)
ax_img, ax_mtf = camera_plot(cam)
```

Run `pytest -q` after editing these camera visualization helpers.

## iso12233_sfr

`iso12233_sfr` computes the spatial frequency response (SFR) from a
slanted-edge test chart.

```python
import numpy as np
from isetcam.metrics import iso12233_sfr

x, y = np.meshgrid(np.arange(32), np.arange(32))
edge = (x > 0.25 * y + 8).astype(float)
freq, mtf = iso12233_sfr(edge, delta_x=0.002)
```

Run `pytest -q` after implementing the slanted-edge metric.

## Human Pupil Size and Macular Transmittance

`human_pupil_size` estimates the diameter and area of the human pupil while
`human_macular_transmittance` applies macular pigment absorption to an
`OpticalImage` instance.

```python
from isetcam.human import human_pupil_size, human_macular_transmittance
from isetcam.opticalimage import OpticalImage

diam, area = human_pupil_size(100, 'wy', age=30)
oi2 = human_macular_transmittance(oi, density=0.35)
```

Run `pytest -q` after updating these human vision helpers.

## Human Optical Density, OTF and LSF

Additional human eye utilities provide typical optical density parameters and
frequency-domain models.

```python
import numpy as np
from isetcam.human import human_optical_density, human_otf, human_lsf

od = human_optical_density()
otf, fs, wave = human_otf(wave=np.array([550]))
lsf, x_axis, _ = human_lsf(wave=np.array([550]))
```


Remember to run `pytest -q` whenever modifying these functions.

## human_wave_defocus and human_core

`human_wave_defocus` returns ocular defocus in diopters versus wavelength.
`human_core` computes the optical transfer function across wavelengths for a
set of spatial frequencies.

```python
import numpy as np
from isetcam.human import human_wave_defocus, human_core

wave = np.arange(450, 651, 50)
D = human_wave_defocus(wave)
otf = human_core(np.array([10, 20]), wave=wave)
```

Run `pytest -q` after editing these human vision routines.

## human_achromatic_otf

`human_achromatic_otf` returns the achromatic modulation transfer function
for spatial frequencies in cycles per degree. The ``'dl'`` and
``'watson'`` models require a pupil diameter in millimeters.

```python
import numpy as np
from isetcam.human import human_achromatic_otf

sf = np.arange(0, 51, 10)
mtf = human_achromatic_otf(sf, 'watson', pupil_d=3.0)
```

Run `pytest -q` after updating the achromatic OTF helper.

## human_otf_ibio and ijspeert

`human_otf_ibio` wraps the ISETBio human optical transfer function while
`ijspeert` evaluates an analytic model for the ocular MTF and, when
requested, its PSF and LSF.

```python
import numpy as np
from isetcam.human import human_otf_ibio, ijspeert

otf2d, support, wave = human_otf_ibio()
freq = np.linspace(0, 60, 6)
mtf, _, _ = ijspeert(30, 3.0, 0.4, freq)
```

Remember to run `pytest -q` after editing these vision functions.
## human_space_time, kelly_space_time and westheimer_lsf

These helpers return spatio-temporal sensitivity surfaces and a line spread function for human vision.
The `'poirsoncolor'` option (also `'wandellpoirsoncolorspace'`) gives
luminance and chromatic sensitivity surfaces.

```python
from isetcam.human import human_space_time, kelly_space_time, westheimer_lsf
spatial, fs, ft = human_space_time()
poirson, pos, _ = human_space_time("poirsoncolor")
ks_sens, _, _ = kelly_space_time()
lsf, x = westheimer_lsf()
```

Run `pytest -q` after editing these human vision models.


## Human Cone Contrast and Cone Isolating

`human_cone_isolating` returns RGB directions for a display that
approximately isolate each cone class. `human_cone_contrast` computes the
L, M and S cone contrast of a signal relative to a background.

```python
from isetcam.display import display_create
from isetcam.human import human_cone_isolating, human_cone_contrast

dsp = display_create('LCD-Apple')
iso, sig_spd = human_cone_isolating(dsp)
bg_spd = dsp.spd @ (0.5 * np.ones(3))
contrast = human_cone_contrast(sig_spd, bg_spd, dsp.wave)
```

Run `pytest -q` after editing these human cone utilities.

## IP Package

The `ip` package implements a minimal sensor to display pipeline. Use
`ip_create` to allocate a `VCImage` and `ip_compute` to render sensor volts
into RGB values.  `ip_get` and `ip_set` retrieve or update fields.

```python
from isetcam.sensor import sensor_create
from isetcam.display import display_create
from isetcam.ip import ip_create, ip_compute, ip_get, ip_set

sensor = sensor_create()
disp = display_create()
vc = ip_compute(sensor, disp)
print(ip_get(vc, 'n wave'))
ip_set(vc, 'name', 'view')
```

Run `pytest -q` when modifying the IP pipeline.

## Display Render and Show

`display_render` converts digital RGB values to spectral radiance using a
`Display` definition.  `display_show_image` renders and displays the result
with matplotlib.

```python
from isetcam.display import Display, display_render, display_show_image

spectral = display_render(img, disp)
ax = display_show_image(img, disp)
```

The unit test for `display_show_image` sets the Matplotlib backend to `"Agg"`
so the function can run without opening a window.  Remember to run
`pytest -q` after editing the display routines.

## Display List, Plot and Max Contrast

`display_list` returns the names of available display calibration files.
`display_plot` visualizes a display's SPD, gamma curves or gamut when
matplotlib is installed. `display_max_contrast` computes the Michelson
contrast between two RGB directions.

```python
from isetcam.display import (
    display_create,
    display_list,
    display_plot,
    display_max_contrast,
)

names = display_list()
dsp = display_create(names[0])
ax = display_plot(dsp, kind="spd")
contrast = display_max_contrast(dsp.spd[:, 0], dsp.spd[:, 1])
```

Remember to run `pytest -q` and `flake8` after updating the display utilities.

## Additional Display Helpers

The display module now exposes routines for describing and adjusting a display.

```python
from isetcam.display import (
    display_description,
    display_set_max_luminance,
    display_set_white_point,
    display_reflectance,
    display_create,
)

disp = display_create()
print(display_description(disp))
display_set_max_luminance(disp, 150)
display_set_white_point(disp, (0.31, 0.33))
ref_disp, primaries, illum = display_reflectance(6500)
```

Run `pytest -q` and `flake8` after modifying these display helpers.

## Portable FloatMap I/O

`pfm_read` and `pfm_write` load and save images in the high dynamic range PFM
format.

```python
from isetcam.io import pfm_read, pfm_write

pfm_write('img.pfm', data.astype(np.float32))
loaded = pfm_read('img.pfm')
```

Run `pytest -q` after modifying these I/O helpers.

## vc_get_object and Replacement Helpers

Objects stored in the global session can be retrieved with `vc_get_object`.
Use `vc_replace_object` or `vc_replace_and_select_object` to update an entry
while maintaining the selected index.

```python
from isetcam import (
    ie_init,
    vc_add_and_select_object,
    vc_get_object,
    vc_replace_object,
    vc_replace_and_select_object,
)

ie_init()
idx = vc_add_and_select_object('scene', sc)
sc2 = vc_get_object('scene', idx)
vc_replace_object('scene', new_sc, idx)
vc_replace_and_select_object('scene', other_sc)
```

Run `pytest -q` after changing the session management helpers.

## illuminant_get and illuminant_set

`illuminant_get` retrieves values from an `Illuminant` dataclass while
`illuminant_set` updates its fields.

```python
import numpy as np
from isetcam.illuminant import Illuminant, illuminant_get, illuminant_set

illum = Illuminant(spd=np.ones((31, 1)), wave=np.arange(400, 701, 10))
illuminant_set(illum, "name", "demo")
nwave = illuminant_get(illum, "n wave")
```

Run `pytest -q` after editing the illuminant helpers.

## display_compute and display_convert

`display_compute` converts digital RGB values to spectral radiance using a
`Display` definition.  `display_convert` builds a `Display` instance from a
Color Toolbox dictionary.

```python
import numpy as np
from isetcam.display import Display, display_compute, display_convert

img = np.random.rand(4, 4, 3)
disp = Display(spd=np.eye(3), wave=np.array([450, 550, 650]))
spectral = display_compute(img, disp)

ct = {"m_strDisplayName": "demo", "sPhysicalDisplay": {"m_objCDixelStructure": {
    "m_aWaveLengthSamples": disp.wave,
    "m_aSpectrumOfPrimaries": disp.spd,
}}}
disp2 = display_convert(ct)
```

Run `pytest -q` after modifying the display routines.

## scene_depth_overlay and scene_depth_range

`scene_depth_overlay` draws depth map contours on a scene RGB rendering.
`scene_depth_range` masks photons outside a specified depth interval.

```python
import numpy as np
from isetcam.scene import Scene, scene_depth_overlay, scene_depth_range

sc = Scene(photons=np.ones((2, 2, 3)), wave=np.array([500, 600, 700]))
sc.depth_map = np.array([[0.3, 0.5], [0.6, 0.8]])
ax = scene_depth_overlay(sc, n=5)
sc2, mask = scene_depth_range(sc, (0.4, 0.7))
```

Run `pytest -q` after updating the depth utilities.

## sensor_ccm

Use `sensor_ccm` to fit a 3x3 color correction matrix from a Macbeth chart
captured by a sensor.

```python
import numpy as np
from isetcam.sensor import Sensor, sensor_ccm

sensor = Sensor(volts=chart_volts, wave=np.array([550]), exposure_time=0.01)
corners = np.array([[0, sensor.volts.shape[0]],
                    [sensor.volts.shape[1], sensor.volts.shape[0]],
                    [sensor.volts.shape[1], 0],
                    [0, 0]], dtype=float)
L = sensor_ccm(sensor, corners)
```

Run `pytest -q` after editing the sensor CCM routine.

## metrics_compute

`metrics_compute` evaluates image quality metrics such as CIELAB ΔE,
mean squared error, PSNR or SCIELAB.

```python
import numpy as np
from isetcam.metrics import metrics_compute, sc_params

img1 = np.random.rand(4, 4, 3)
img2 = np.random.rand(4, 4, 3)
white = np.array([0.95047, 1.0, 1.08883])
de = metrics_compute(img1, img2, "cielab", white_point=white)
psnr = metrics_compute(img1, img2, "psnr")
```

Run `pytest -q` to ensure the metric calculations remain valid.

## illuminant_list

List the available illuminant spectral files bundled with the package.

```python
from isetcam.illuminant import illuminant_list

names = illuminant_list()
print(names[:3])
```

Run `pytest -q` after updating the illuminant listing helper.

## sensor_show_image

`sensor_show_image` renders sensor volt data to sRGB and shows it with
Matplotlib.

```python
from isetcam.sensor import Sensor, sensor_show_image

sensor = Sensor(volts=raw_volts, wave=wave, exposure_time=0.01)
ax = sensor_show_image(sensor)
```

Run `pytest -q` after editing the sensor display helper.

## ip_to_file and ip_from_file

Use `ip_to_file` to save a ``VCImage`` to disk and `ip_from_file` to
reload it.

```python
from isetcam.ip import VCImage, ip_to_file, ip_from_file

ip = VCImage(rgb=rgb, wave=wave, name="demo")
ip_to_file(ip, "vcimage.mat")
loaded = ip_from_file("vcimage.mat")
```

Remember to run `pytest -q` after modifying these IP file utilities.

## optics_psf and optics_otf

`optics_psf` converts a PSF to an OTF while `optics_otf` performs the
inverse operation.

```python
import numpy as np
from isetcam.optics import optics_psf, optics_otf

psf = np.ones((5, 5))
otf = optics_psf(psf)
psf2 = optics_otf(otf)
```

Run `pytest -q` after updating the optics transforms.

## pocs Demosaicing

The `pocs` routine demosaics a Bayer pattern using Projection Onto
Convex Sets.

```python
from isetcam.imgproc import pocs

rgb = pocs(bayer, "rggb", iter_n=10)
```

Run `pytest -q` when modifying the POCS routine.

## scene_spd_scale

`scene_spd_scale` multiplies the photons of a scene by a constant factor.

```python
from isetcam.scene import scene_spd_scale

sc2 = scene_spd_scale(sc, 0.5)
```

Run `pytest -q` to confirm the scaling helper.

## scene_illuminant_scale

`scene_illuminant_scale` adjusts the scene illuminant so that the
average reflectance equals one without modifying the photon data.

```python
from isetcam.scene import Scene, scene_illuminant_scale

sc = Scene(photons=data, wave=wave)
sc.illuminant = illum
sc2 = scene_illuminant_scale(sc)
```

Run `pytest -q` after editing the illuminant scaling routine.

## sensor_rotate

Rotate a sensor voltage image by a chosen angle.

```python
from isetcam.sensor import sensor_rotate

rotated = sensor_rotate(sensor, 90)
```

Run `pytest -q` after modifying the rotation utility.

## vc_delete_object

Remove an entry from the global session by type and index.

```python
from isetcam import ie_init, vc_add_and_select_object, vc_delete_object

ie_init()
idx = vc_add_and_select_object("scene", sc)
remaining = vc_delete_object("scene", idx)
```

Remember to run `pytest -q` when updating the session manager.

## vc_clear_objects

`vc_clear_objects` removes all stored objects from the global session and
resets the selection indices.

```python
from isetcam import (
    ie_init,
    vc_add_and_select_object,
    vc_clear_objects,
)
from isetcam.scene import Scene

ie_init()
vc_add_and_select_object("scene", Scene(photons=np.zeros((1, 1, 1))))
vc_clear_objects()
```

Run `pytest -q` after implementing the session cleanup helper.

## Additional vc_* Session Utilities

Several helpers manage the global session beyond object insertion and
deletion:

- `vc_get_objects` and `vc_set_objects` access the full list for a type
- `vc_count_objects` returns how many objects of a type are stored
- `vc_get_object_names` lists the stored object names
- `vc_get_selected_object` and `vc_set_selected_object` handle the
  current selection
- `vc_new_object_name` and `vc_new_object_value` generate unique
  identifiers

```python
from isetcam import (
    ie_init,
    vc_add_and_select_object,
    vc_get_objects,
    vc_count_objects,
    vc_get_object_names,
    vc_set_selected_object,
    vc_get_selected_object,
    vc_new_object_name,
)

session = ie_init()
vc_add_and_select_object("scene", my_scene)
count = vc_count_objects("scene")
names = vc_get_object_names("scene")
vc_set_selected_object("scene", 1)
idx, obj = vc_get_selected_object("scene")
new_name = vc_new_object_name("scene")
```

Run `pytest -q` after updating the session utilities.

## vc_copy_object, vc_rename_object and ROI Helpers

Duplicate or rename objects in the global session and convert regions between rectangle and location formats.

```python
idx2 = vc_copy_object("scene")
vc_rename_object("scene", "copy", index=idx2)
rows, cols = vc_rect_to_locs((0, 0, 4, 4))
rect = vc_locs_to_rect((rows, cols))
```

Run `pytest -q` after updating these session helpers.

## oi_create

`oi_create` builds a uniform `OpticalImage` of a specified size.

```python
from isetcam.opticalimage import oi_create

oi = oi_create(name="demo", size=64)
print(oi.photons.shape)
```

Run `pytest -q` after editing this factory.

## scene_description

Generate a textual summary of a scene.

```python
from isetcam.scene import Scene, scene_description

sc = Scene(photons=data, wave=wave, name="demo")
print(scene_description(sc))
```

Run `pytest -q` after updating the description helper.

## scene_clear_data

Remove optional cached fields from a scene structure.

```python
from isetcam.scene import Scene, scene_clear_data

sc = Scene(photons=data, wave=wave)
sc.ui = {"win": None}
scene_clear_data(sc)
```

Run `pytest -q` after modifying the cleanup routine.

## oi_clear_data, sensor_clear_data, ip_clear_data and camera_clear_data

Remove cached attributes from optical images, sensors, VCImage objects and
complete cameras.  These helpers strip fields that may have been added by
user interfaces or previous computations.

```python
from isetcam.opticalimage import OpticalImage, oi_clear_data
from isetcam.sensor import Sensor, sensor_clear_data
from isetcam.ip import VCImage, ip_clear_data
from isetcam.camera import Camera, camera_clear_data

oi = oi_clear_data(OpticalImage(photons=data, wave=wave))
sensor = sensor_clear_data(Sensor(volts=raw, wave=wave, exposure_time=0.01))
ip = ip_clear_data(VCImage(rgb=rgb, wave=wave))
cam = camera_clear_data(Camera(sensor=sensor, optical_image=oi, ip=ip))
```

Run `pytest -q` after editing any of these cleanup routines.

## scene_interpolate_w and oi_interpolate_w

Resample the spectral data of a scene or optical image to a new wavelength grid.

```python
from isetcam.scene import scene_interpolate_w
from isetcam.opticalimage import oi_interpolate_w

new_wave = np.arange(450, 651, 5)
sc2 = scene_interpolate_w(sc, new_wave)
oi2 = oi_interpolate_w(oi, new_wave)
```

Remember to run `pytest -q` after editing these interpolation functions.

## sensor_show_cfa

Display the sensor color filter array arrangement.

```python
from isetcam.sensor import Sensor, sensor_show_cfa

s = Sensor(filter_color_letters="rggb")
ax = sensor_show_cfa(s)
```

Run `pytest -q` after updating the CFA viewer.

## sensor_add_filter, sensor_delete_filter and sensor_replace_filter

Modify the color filter array for a `Sensor` instance.

```python
import numpy as np
from isetcam import data_path
from isetcam.sensor import (
    Sensor,
    sensor_add_filter,
    sensor_delete_filter,
    sensor_replace_filter,
)

s = Sensor(volts=np.zeros((1, 1)), wave=np.arange(370, 731, 10), exposure_time=0.01)
sensor_add_filter(s, data_path("sensor/colorfilters/B.mat"))
sensor_delete_filter(s, 0)
sensor_add_filter(s, data_path("sensor/colorfilters/G.mat"))
sensor_replace_filter(s, 0, data_path("sensor/colorfilters/R.mat"))
```

Run `pytest -q` after editing the CFA helpers.

## Color Filter File Utilities

Read or write color filter spectra using `ie_save_color_filter` and `ie_read_color_filter`.

```python
from isetcam.io import ie_save_color_filter, ie_read_color_filter

ie_save_color_filter("filters.mat", spectra, names, wave)
filters, names, wv = ie_read_color_filter("filters.mat", wave)
```

Run `pytest -q` after updating the color filter helpers.


## sensor_stats

Compute mean signal, noise standard deviation and SNR for a sensor ROI.

```python
from isetcam.sensor import sensor_stats

roi = (0, 0, 2, 2)
mean_signal, noise_sd, snr = sensor_stats(sensor, roi)
```

Run `pytest -q` after modifying the sensor statistics helper.

## sensor_iso_speed

`sensor_iso_speed` estimates the ISO speed from sensor noise parameters using
the SNR=10 criterion.

```python
import numpy as np
from isetcam.sensor import Sensor, sensor_set, sensor_iso_speed

s = Sensor(volts=np.zeros((1,)), wave=np.array([550]), exposure_time=0.01)
sensor_set(s, "conversion_gain", 1.0)
sensor_set(s, "read_noise_electrons", 5.0)
sensor_set(s, "gain_sd", 0.0)
sensor_set(s, "offset_sd", 0.0)
s.volts_per_lux_sec = 1000.0
iso = sensor_iso_speed(s)
```

Run `pytest -q` after editing the ISO speed calculation.

## iso_speed_saturation

`iso_speed_saturation` evaluates the saturation-based ISO speed using a
uniform D65 source.

```python
import numpy as np
from isetcam.sensor import Sensor
from isetcam.metrics import iso_speed_saturation

s = Sensor(volts=np.zeros((1,)), wave=np.array([550]), exposure_time=0.01)
s.well_capacity = 5000.0
s.qe = np.array([1.0])
iso = iso_speed_saturation(s)
```

Run `pytest -q` after adding the saturation speed routine.

## human_cones, human_cone_mosaic, watson_impulse_response and watson_rgc_spacing

These helpers return cone spectral sensitivities, simulate a simple cone mosaic and model ganglion cell temporal and spatial characteristics.

```python
import numpy as np
from isetcam.human import (
    human_cones,
    human_cone_mosaic,
    watson_impulse_response,
    watson_rgc_spacing,
)

spd = human_cones()
cones = human_cone_mosaic((64, 64))
imp = watson_impulse_response(np.linspace(0, 0.1, 100))
spacing = watson_rgc_spacing(0.5)
```

Run `pytest -q` after implementing these routines.

## scene_hdr_image

`scene_hdr_image` creates a simple HDR pattern of bright patches over an
optional background image.

```python
from isetcam.scene import scene_hdr_image

sc = scene_hdr_image(5, image_size=256, dynamic_range=4.0)
```

Run `pytest -q` after editing the HDR image helper.

## scene_hdr_chart

`scene_hdr_chart` returns horizontal strips spanning a very wide dynamic
range.

```python
from isetcam.scene import scene_hdr_chart

chart = scene_hdr_chart(dynamic_range=1e5, n_levels=10)
```

Run `pytest -q` after updating the HDR chart helper.

## scene_hdr_lights

`scene_hdr_lights` generates a synthetic scene of geometric lights across
several intensity levels.

```python
from isetcam.scene import scene_hdr_lights

lights = scene_hdr_lights(image_size=384, dynamic_range=1e6)
```

Run `pytest -q` once the lights helper is implemented.

## scene_create_hdr

Use `scene_create_hdr` to access the HDR scene factories by name.

```python
from isetcam.scene import scene_create_hdr

hdr = scene_create_hdr('hdrimage', n_patches=6)
```

Run `pytest -q` after modifying the HDR factory.

## CPCamera, CPScene, CPCModule, cp_burst_camera and cp_burst_ip

The `cp` package provides simple computational photography helpers. In HDR
mode `cp_burst_camera` now returns exposure times symmetric around the
``base_exposure`` with steps of ``ev_step`` in exposure value (EV).

```python
from isetcam.cp import CPScene, CPCModule, CPCamera, cp_burst_camera, cp_burst_ip
from isetcam.sensor import sensor_create
from isetcam.optics import optics_create
from isetcam.scene import scene_create

scene = CPScene([scene_create('uniform', size=8)])
module = CPCModule(sensor_create(), optics_create())
camera = CPCamera([module])

exp_times = cp_burst_camera(3, 0.01, mode='hdr', ev_step=1.0)  # [0.005, 0.01, 0.02]
captures = camera.take_picture(scene, exposure_times=exp_times)
combined = cp_burst_ip(captures, mode='sum')
```

Run `pytest -q` after implementing these burst capture routines.

## ip_hdr_white

`ip_hdr_white` shifts bright regions of a `VCImage` toward white for HDR
display.

```python
import numpy as np
from isetcam.ip import VCImage, ip_hdr_white

ip = VCImage(rgb=np.random.rand(64, 64, 3))
ip, weights = ip_hdr_white(ip, saturation=1.0, hdr_level=0.9)
```

Run `pytest -q` after editing the HDR whitening function.

## optics_cos4th and optics_defocused_mtf

`optics_cos4th` models cos^4 falloff vignetting while `optics_defocused_mtf` returns an MTF for a defocused optic.

```python
import numpy as np
from isetcam.optics import optics_cos4th, optics_defocused_mtf

v = optics_cos4th(np.linspace(0, 1, 5))
mtf = optics_defocused_mtf(np.arange(0, 60, 10), defocus_d=1.0)
```

Run `pytest -q` after editing these optics helpers.

## camera_full_reference

`camera_full_reference` compares a rendered image against ground truth and returns quality metrics.

```python
from isetcam.camera import camera_full_reference

score = camera_full_reference(target, reference)
```

Run `pytest -q` after adding this metric.

## image_illuminant_correction and image_esser_transform

`image_illuminant_correction` balances an image for a chosen illuminant while `image_esser_transform` computes the Esser chart transform.

```python
from isetcam.imgproc import image_illuminant_correction, image_esser_transform

balanced = image_illuminant_correction(img, illum)
T = image_esser_transform(patch_size=4)
```

Run `pytest -q` after implementing these routines.
## ie_clip

Clamp array values to a range. With one bound the other is mirrored.

```python
import numpy as np
from isetcam import ie_clip

vals = np.linspace(-1, 1, 5)
clipped = ie_clip(vals, 0, 1)
```

Run `pytest -q` after implementing the clipping helper.

## ie_scp

Copy a local file to a remote host using ``scp``.

```python
from isetcam import ie_scp

cmd, rc = ie_scp('user', 'host', 'local.txt', 'remote.txt')
print(cmd, rc)
```

Run `pytest -q` to verify the secure copy wrapper.

## ie_gamma and ie_tone

Gamma correction and tone mapping helpers.

```python
import numpy as np
from isetcam import ie_gamma, ie_tone_curve, ie_apply_tone

img = ie_gamma(np.random.rand(4, 4, 3), 2.2)
curve = ie_tone_curve(num_points=64)
img = ie_apply_tone(img, curve)
```

Run `pytest -q` after implementing the gamma and tone modules.

## ie_tikhonov

`ie_tikhonov` solves a regularized least-squares problem with optional
minimum-norm and smoothness terms.

```python
import numpy as np
from isetcam import ie_tikhonov

A = np.array([[1, 2], [3, 4], [5, 6]], dtype=float)
b = np.array([1.0, 2.0, 3.0])
x, x_ols = ie_tikhonov(A, b, minnorm=0.1, smoothness=0.05)
```

Run `pytest -q` after editing the regularization helper.
## sensor_resample_wave

Interpolate sensor spectral data to a new wavelength grid.

```python
import numpy as np
from isetcam.sensor import Sensor, sensor_resample_wave

s = Sensor(volts=np.ones((2, 2)), wave=np.arange(400, 701, 10))
new = sensor_resample_wave(s, np.arange(420, 681, 20))
print(new.wave)
```

Run `pytest -q` after adding this resampling routine.

## sensor_rescale

Resize the sensor voltage image and update the pixel size.

```python
from isetcam.sensor import Sensor, sensor_rescale

s = Sensor(volts=np.ones((2, 2)), wave=np.array([550]), exposure_time=0.01)
s2 = sensor_rescale(s, (4, 4), (4e-6, 4e-6))
print(s2.volts.shape)
```

Run `pytest -q` after implementing the rescaling helper.

## sensor_gain_offset

Apply analog gain and offset to sensor voltages.

```python
from isetcam.sensor import Sensor, sensor_gain_offset

s = Sensor(volts=np.array([1.0]), wave=np.array([550]), exposure_time=0.01)
sensor_gain_offset(s, gain=2.0, offset=-0.5)
```

Run `pytest -q` after updating the gain/offset routine.

## sensor_dr

Compute the sensor dynamic range in decibels.

```python
from isetcam.sensor import Sensor, sensor_set, sensor_dr

s = Sensor(volts=np.zeros((1,)), wave=np.array([550]), exposure_time=0.01)
sensor_set(s, 'read_noise_electrons', 5.0)
dr_db, vmax, vmin = sensor_dr(s)
```

Run `pytest -q` after adding the dynamic range calculation.
## scene_calculate_luminance

Compute the luminance map of a scene in cd/m^2 and return the mean value.

```python
import numpy as np
from isetcam.scene import Scene, scene_calculate_luminance

sc = Scene(photons=np.ones((1, 1, 1)), wave=np.array([550]))
lum, mean_lum = scene_calculate_luminance(sc)
print(mean_lum)
```

Run `pytest -q` after editing the luminance routine.

## scene_from_ddf_file

Load a compressed ``.ddf`` file that stores photons and wavelength data.

```python
from isetcam.scene import scene_from_ddf_file

sc = scene_from_ddf_file('sample.ddf')
print(sc.photons.shape)
```

Run `pytest -q` after modifying the DDF reader.

## scene_make_video

Encode a list of scenes into a movie using ``ffmpeg``.

```python
from isetcam.scene import Scene, scene_make_video
import numpy as np

wave = np.array([500, 600, 700])
sc1 = Scene(photons=np.ones((2, 2, 3)), wave=wave)
sc2 = Scene(photons=np.zeros((2, 2, 3)), wave=wave)
scene_make_video([sc1, sc2], 'movie.mp4', fps=10)
```

Run `pytest -q` after updating the video writer.

## scene_init_geometry and scene_init_spatial

Assign default distance and field of view when they are undefined.

```python
from isetcam.scene import Scene, scene_init_geometry, scene_init_spatial
import numpy as np

sc = Scene(photons=np.ones((1, 1, 1)), wave=np.array([550]))
scene_init_geometry(sc)
scene_init_spatial(sc)
print(sc.distance, sc.fov)
```

Run `pytest -q` after editing the initialization helpers.

## scene_photons_from_vector and scene_energy_from_vector

Retrieve the spectral data at a pixel as a vector of photons or energy.

```python
from isetcam.scene import (
    Scene,
    scene_photons_from_vector,
    scene_energy_from_vector,
)
import numpy as np

sc = Scene(photons=np.arange(6).reshape(1, 2, 3), wave=np.array([500, 600, 700]))
phot_vec = scene_photons_from_vector(sc, 0, 1)
energy_vec = scene_energy_from_vector(sc, 0, 1)
```

Run `pytest -q` after modifying the vector utilities.
## scene_radiance_from_vector

Return the radiance vector at a pixel in watts/sr/nm/m^2.

```python
from isetcam.scene import scene_radiance_from_vector
vec = scene_radiance_from_vector(sc, 0, 1)
```

Run `pytest -q` after editing this routine.


## scene_checkerboard, scene_dead_leaves and scene_grid_lines

Generate synthetic patterns for resolution and texture testing.

```python
from isetcam.scene import (
    scene_checkerboard,
    scene_dead_leaves,
    scene_grid_lines,
)

cb = scene_checkerboard(8, 4)
dl = scene_dead_leaves(patch_size=128, noise_level=0.05)
gl = scene_grid_lines(size=64, spacing=8, spectral_type="ep")
```

Run `pytest -q` after implementing these scene generators.
## oi_calculate_otf

Compute the optical transfer function for an optical image and optics model.

```python
import numpy as np
from isetcam.opticalimage import OpticalImage, oi_calculate_otf
from isetcam.optics import Optics

oi = OpticalImage(photons=np.ones((4, 4, 1)), wave=np.array([550]))
optics = Optics(f_number=4.0, f_length=0.005, wave=oi.wave)
otf, fs = oi_calculate_otf(oi, optics)
print(otf.shape)
```

Run `pytest -q` after editing the OTF calculation.

## human_oi

Create a human optical image from scene photons using typical eye optics.

```python
import numpy as np
from isetcam.scene import Scene
from isetcam.human import human_oi

sc = Scene(photons=np.ones((8, 8, 1)), wave=np.array([550]))
oi = human_oi(sc)
print(oi.illuminance.shape)
```

Run `pytest -q` after updating the human OI helper.

## human_uv_safety

Evaluate ultraviolet and blue light exposure safety.

```python
import numpy as np
from isetcam.human import human_uv_safety

wave = np.arange(300, 401, 10)
energy = np.ones_like(wave) * 0.01
val, level, safe = human_uv_safety(energy, wave, method='eye', duration=100)
```

Run `pytest -q` after modifying the UV safety routine.

## camera_vsnr_sl

`camera_vsnr_sl` computes visible SNR values for a camera over a sweep of mean luminances.

```python
from isetcam.camera import camera_create, camera_vsnr_sl

cam = camera_create()
result = camera_vsnr_sl(cam, [1, 10, 100])
print(result.vsnr)
```

Run `pytest -q` after implementing the VSNR sweep.

## oi_wb_compute and oi_camera_motion

`oi_wb_compute` loads single-waveband scenes from a directory and saves the corresponding optical images. `oi_camera_motion` shifts and averages an optical image according to a motion path.

```python
from isetcam.opticalimage import (
    OpticalImage,
    oi_wb_compute,
    oi_camera_motion,
)
from isetcam.optics import optics_create
import numpy as np

paths = oi_wb_compute("wb_dir", optics_create())
oi = OpticalImage(photons=np.ones((2, 2, 1)), wave=np.array([550]))
moved = oi_camera_motion(oi, {"path": [(0, 0), (1, 0)], "fill": 0})
```

Run `pytest -q` after adding or modifying these optical image helpers.

## camera_computesrgb

`camera_computesrgb` renders a scene with a camera and returns the approximate and ideal sRGB images along with the raw sensor volts.

```python
from isetcam.camera import camera_create, camera_computesrgb

cam = camera_create()
srgb_res, srgb_ideal, volts = camera_computesrgb(
    cam,
    scene="macbeth d65",
    patch_size=4,
    mean_luminance=20,
)
```

Run `pytest -q` once the sRGB computation routine is in place.

## sensor_wb_compute and sensor_vignetting

`sensor_wb_compute` accumulates the response of a sensor to multiple optical images. `sensor_vignetting` attaches a pixel vignetting map.

```python
import numpy as np
from isetcam.sensor import Sensor, sensor_wb_compute, sensor_vignetting
from isetcam.opticalimage import OpticalImage

sensor = Sensor(volts=np.zeros((2, 2)), wave=np.array([500, 510]), exposure_time=0.5)
oi1 = OpticalImage(photons=np.ones((2, 2)), wave=np.array([500]))
oi2 = OpticalImage(photons=2 * np.ones((2, 2)), wave=np.array([510]))
sensor_wb_compute(sensor, [oi1, oi2])
sensor_vignetting(sensor)
```

Run `pytest -q` after updating these sensor utilities.

## scene_from_basis

Construct a scene from basis coefficients and an illuminant.

```python
from isetcam.scene import scene_from_basis

sceneS = {"mcCOEF": coef, "basis": basis, "illuminant": illum}
sc = scene_from_basis(sceneS)
```

Run `pytest -q` after adding or modifying this helper.

## illuminant_modernize

Convert legacy illuminant structures into the modern dataclass.

```python
from isetcam.illuminant import illuminant_modernize

legacy = {"data": np.ones(3), "wave": np.array([500, 510, 520])}
illum = illuminant_modernize(legacy)
```

Run `pytest -q` after updating the illuminant utilities.

## optics_coc and oi_make_even_row_col

`optics_coc` computes the circle of confusion at various evaluation
distances. `oi_make_even_row_col` pads an optical image so its dimensions
are even while preserving field of view.

```python
import numpy as np
from isetcam.optics import Optics, optics_coc
from isetcam.opticalimage import OpticalImage, oi_make_even_row_col

opt = Optics(f_number=4.0, f_length=0.05)
diam = optics_coc(opt, 1.0, np.linspace(0.5, 2.0, 3))

oi = OpticalImage(photons=np.ones((5, 3, 1)), wave=np.array([550]))
oi_even = oi_make_even_row_col(oi)
```

Run `pytest -q` after modifying these optics helpers.

## sensor_show_cfa_weights and sensor_set_size_to_fov

`sensor_show_cfa_weights` visualizes a weight matrix using the sensor CFA
colors. `sensor_set_size_to_fov` resizes the sensor so its field of view
matches an optical image or optics definition.

```python
import numpy as np
from isetcam.sensor import (
    Sensor,
    sensor_show_cfa_weights,
    sensor_set_size_to_fov,
)
from isetcam.opticalimage import OpticalImage
from isetcam.optics import Optics

weights = np.arange(9).reshape(3, 3)
s = Sensor(volts=np.zeros((4, 4)), wave=np.array([550]), exposure_time=0.01)
s.filter_color_letters = "rggb"
img = sensor_show_cfa_weights(weights, s)

oi = OpticalImage(photons=np.zeros((1, 1, 1)), wave=np.array([550]))
oi.optics = Optics(f_number=4.0, f_length=1e-3, wave=oi.wave)
sensor_set_size_to_fov(s, 0.5, oi)
```

Run `pytest -q` after updating these sensor routines.

## Hypercube utilities

The `hypercube` package contains helpers for processing hyperspectral image cubes.

```python
import numpy as np
from isetcam.hypercube import (
    hc_basis,
    hc_blur,
    hc_illuminant_scale,
    hc_image,
    hc_image_crop,
    hc_image_rotate_clip,
)

cube = np.random.rand(4, 4, 31)
basis = np.random.rand(31, 5)
cube_basis = hc_basis(cube, basis)
cube_blur = hc_blur(cube, 1.5)
scaled_illum = hc_illuminant_scale(cube, np.ones(31))
img = hc_image(cube, np.arange(400, 710, 10))
crop = hc_image_crop(cube, (1, 1, 2, 2))
rot = hc_image_rotate_clip(cube, 15.0)
```

Run `pytest -q` after implementing these hypercube utilities.

## Font management and `scene_from_font`

Font creation, parameter access and modification mirror the MATLAB routines. The
`scene_from_font` function builds a simple scene from rendered text.

```python
from isetcam.fonts import font_create, font_get, font_set
from isetcam.scene import scene_from_font

f = font_create(letter="A", size=20)
bitmap = font_get(f, "bitmap")
f = font_set(f, "size", 24)
scene = scene_from_font("ISET", f)
```

Run `pytest -q` after updating these font helpers.

## `web_flickr` and `web_pixabay`

These utilities download photos from their respective web APIs.

```python
from isetcam.web import web_flickr, web_pixabay

flickr_paths = web_flickr("cats", "FLICKR_API_KEY", 5, "flickr_dir")
pixabay_paths = web_pixabay("dogs", "PIXABAY_API_KEY", 5, "pixabay_dir")
```

Run `pytest -q` after adding these web utilities.

## `animated_gif`

Write a series of frames into an animated GIF.

```python
import numpy as np
from isetcam import animated_gif

frames = np.random.rand(10, 16, 16, 3)
animated_gif(frames, "movie.gif", fps=5, loop=1)
```

Run `pytest -q` after modifying this animation helper.
