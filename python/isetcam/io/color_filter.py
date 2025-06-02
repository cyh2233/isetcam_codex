# mypy: ignore-errors
"""Read and write color filter spectra."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Sequence

import numpy as np
from scipy.io import loadmat, savemat
import h5py


def _read_mat(path: Path) -> tuple[np.ndarray, np.ndarray, List[str]]:
    """Read a MAT-file returning ``(data, wave, names)``."""
    try:
        mat = loadmat(str(path), squeeze_me=True, struct_as_record=False)
    except NotImplementedError:
        # MATLAB v7.3 file - use h5py
        with h5py.File(str(path), "r") as f:
            wave = np.asarray(f["wavelength"]).reshape(-1)
            data = np.asarray(f["data"])
            if data.shape[0] != wave.size and data.shape[1] == wave.size:
                data = data.T
            if "filterNames" in f:
                ds = f["filterNames"]
                names: List[str] = []
                if ds.dtype.kind == "O":
                    for ref in ds:
                        ref = ref[0] if ds.ndim > 1 else ref
                        names.append("".join(chr(c) for c in f[ref][()].flatten()))
                else:
                    names = [str(s.decode("utf-8")) for s in ds[()].flatten()]
            else:
                names = []
        return data.astype(float), wave.astype(float), names
    else:
        data = np.asarray(mat["data"], dtype=float)
        wave = np.asarray(mat["wavelength"], dtype=float).reshape(-1)
        names = mat.get("filterNames")
        if names is None:
            names_list: List[str] = []
        else:
            arr = np.atleast_1d(names)
            names_list = [str(a.squeeze()) if isinstance(a, np.ndarray) else str(a) for a in arr]
        return data, wave, names_list


def _read_txt(path: Path) -> tuple[np.ndarray, np.ndarray, List[str]]:
    """Read a simple text file."""
    with path.open("r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    names: List[str] = []
    if lines and lines[0].startswith("#"):
        names = lines[0][1:].strip().split()
        lines = lines[1:]
    wave_list: list[float] = []
    rows: list[list[float]] = []
    for ln in lines:
        parts = ln.split()
        if not parts:
            continue
        wave_list.append(float(parts[0]))
        rows.append([float(x) for x in parts[1:]])
    data = np.asarray(rows, dtype=float)
    wave = np.asarray(wave_list, dtype=float)
    if data.ndim == 1:
        data = data.reshape(-1, 1)
    return data, wave, names


def ie_read_color_filter(path: str | Path, wave: Iterable[float] | None = None) -> tuple[np.ndarray, List[str], np.ndarray]:
    """Load filter spectra from ``path`` and interpolate to ``wave``."""
    p = Path(path)
    if p.suffix.lower() == ".mat":
        data, src_wave, names = _read_mat(p)
    else:
        data, src_wave, names = _read_txt(p)
    if wave is None:
        out_wave = src_wave
        res = data
    else:
        out_wave = np.asarray(list(wave), dtype=float).reshape(-1)
        res = np.column_stack(
            [np.interp(out_wave, src_wave, data[:, i], left=0.0, right=0.0) for i in range(data.shape[1])]
        )
    if res.max() > 1.0 or res.min() < 0.0:
        if res.min() >= 0.0:
            res = res / res.max()
        else:
            raise ValueError("Filter values must be non-negative")
    return res.astype(float), names, out_wave


def _write_mat(path: Path, spectra: np.ndarray, names: Sequence[str], wave: np.ndarray) -> None:
    data = {
        "wavelength": wave.reshape(-1, 1),
        "data": spectra,
        "filterNames": np.array(list(names), dtype=object).reshape(-1, 1),
    }
    savemat(str(path), data)


def _write_txt(path: Path, spectra: np.ndarray, names: Sequence[str], wave: np.ndarray) -> None:
    with path.open("w", encoding="utf-8") as f:
        if names:
            f.write("# " + " ".join(names) + "\n")
        for i, wv in enumerate(wave):
            row = [f"{wv:g}"] + [f"{spectra[i, j]:.8f}" for j in range(spectra.shape[1])]
            f.write(" ".join(row) + "\n")


def ie_save_color_filter(
    path: str | Path,
    spectra: np.ndarray,
    names: Sequence[str],
    wave: Iterable[float],
) -> None:
    """Save ``spectra`` and ``names`` at ``wave`` to ``path``."""
    arr = np.asarray(spectra, dtype=float)
    wv = np.asarray(list(wave), dtype=float).reshape(-1)
    if arr.shape[0] != wv.size:
        raise ValueError("spectra rows must match wave length")
    p = Path(path)
    if p.suffix.lower() == ".mat":
        _write_mat(p, arr, names, wv)
    else:
        _write_txt(p, arr, names, wv)


__all__ = ["ie_read_color_filter", "ie_save_color_filter"]
