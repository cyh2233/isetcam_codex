# Python Support for ISETCam

This directory contains experimental Python code that mirrors portions of the
MATLAB ISETCam toolbox.  To use these modules, activate the Python environment
that accompanies the MATLAB examples.

```bash
# Create the environment
conda create -n py39 python=3.9

# Activate it
conda activate py39
```

Inside MATLAB, point `pyenv` to the environment's Python interpreter:

```matlab
pyenv('Version','/opt/miniconda3/envs/py39/bin/python');
```

For a detailed walkthrough see `s_python.m` in this folder.
