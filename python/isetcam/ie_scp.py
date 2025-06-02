# mypy: ignore-errors
"""Lightweight wrapper around the :command:`scp` utility."""

from __future__ import annotations

import subprocess


def ie_scp(user: str, host: str, src: str, dest: str, quiet: bool = True) -> tuple[str, int]:
    """Copy ``src`` to ``dest`` on ``host`` via ``scp``.

    Parameters
    ----------
    user, host : str
        Remote login information used as ``user@host``.
    src : str
        Path to the local file to copy.
    dest : str
        Destination path on the remote host.
    quiet : bool, optional
        Add the ``-q`` flag to suppress progress information.

    Returns
    -------
    tuple[str, int]
        Command string executed and the subprocess return code.
    """
    cmd = ["scp"]
    if quiet:
        cmd.append("-q")
    cmd.extend([src, f"{user}@{host}:{dest}"])
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE if quiet else None,
        stderr=subprocess.PIPE if quiet else None,
    )
    return " ".join(cmd), result.returncode
