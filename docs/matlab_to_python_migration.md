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
)

sensor = Sensor(volts=raw_volts, wave=wave, exposure_time=0.01)
set_exposure_time(sensor, 0.02)
```

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
update values:

```python
import numpy as np
from isetcam.display import Display, display_get, display_set

wave = np.arange(400, 701, 10)
spd = np.ones((len(wave), 3))
disp = Display(spd=spd, wave=wave, name="lcd")
display_set(disp, "name", "main display")
n_wave = display_get(disp, "n wave")
```

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

After adding these modules remember to run the unit tests again with
`pytest -q` to confirm everything works.
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

## sRGB and XYZ

The helpers `srgb_to_xyz` and `xyz_to_srgb` convert between sRGB and CIE XYZ.

```python
import numpy as np
from isetcam import srgb_to_xyz, xyz_to_srgb

srgb = np.random.rand(4, 3)
xyz = srgb_to_xyz(srgb)
srgb2, lrgb, maxY = xyz_to_srgb(xyz)
```

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

After experimenting with these conversions and utilities remember to run `pytest -q` to verify the Python tests pass.
