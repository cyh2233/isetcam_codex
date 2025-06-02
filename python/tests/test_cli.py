import subprocess
import sys

from isetcam.cli import main


def test_cli_info(capsys):
    rc = main(["info"])
    out = capsys.readouterr().out
    assert "isetcam" in out
    assert rc == 0


def test_cli_list_scenes(capsys):
    rc = main(["list-scenes"])
    out = capsys.readouterr().out
    assert rc == 0
    assert isinstance(out, str)


def test_cli_run_tests(monkeypatch):
    called = {}

    def fake_run(cmd, cwd=None):
        called["cmd"] = cmd
        called["cwd"] = cwd

        class Result:
            returncode = 0

        return Result()

    monkeypatch.setattr(subprocess, "run", fake_run)
    rc = main(["run-tests"])
    assert called["cmd"][0] == sys.executable
    assert "pytest" in called["cmd"]
    assert rc == 0
