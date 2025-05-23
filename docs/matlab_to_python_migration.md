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

## Updated Tests

Unit tests in `python/tests` exercise the new conversion and scene
utilities in addition to the initialization routines.  Execute them with
`pytest`:

```bash
export PYTHONPATH=$PWD/python
pytest -q
```
