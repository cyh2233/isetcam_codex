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

## Finding the Repository Root

Use `iset_root_path` to locate the top level of the repository when
constructing paths to test data or calibration files.

```python
from isetcam import iset_root_path

root = iset_root_path()
print(root)
```

Run `pytest -q` after adding code that depends on the repository layout.

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
`scene_from_file`:

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

Scenes can be manipulated after creation. Use `scene_adjust_luminance` to
scale the luminance statistic and `scene_crop` to extract a region:

```python
from isetcam.scene import scene_adjust_luminance, scene_crop

sc2 = scene_adjust_luminance(sc, 'mean', 50)
cropped = scene_crop(sc2, (10, 10, 64, 64))
```

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

## OpenEXR Image I/O

Floating point images can be saved or loaded using `openexr_write` and
`openexr_read`. These helpers rely on the OpenEXR bindings when
available and fall back to the ``imageio`` backend.

```python
from isetcam.io import openexr_read, openexr_write

openexr_write('img.exr', {'R': rgb[:, :, 0], 'G': rgb[:, :, 1], 'B': rgb[:, :, 2]})
channels = openexr_read('img.exr')
```

Run `pytest -q` to confirm the EXR utilities work.

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

After working with these modules you can rerun the unit tests using:

```bash
pytest -q
```

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

## Scene and Optical Image Photon Noise

`scene_photon_noise` and `oi_photon_noise` add Poisson noise to the
photon data stored in a scene or optical image.

```python
from isetcam.scene import scene_photon_noise
from isetcam.opticalimage import oi_photon_noise

noisy_sc, sc_noise = scene_photon_noise(sc)
noisy_oi, oi_noise = oi_photon_noise(oi)
```

Run `pytest -q` after modifying the noise utilities.

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
