import subprocess

from isetcam import ie_scp


def test_ie_scp_quiet(monkeypatch):
    called = {}

    def fake_run(cmd, stdout=None, stderr=None):
        called['cmd'] = cmd
        called['stdout'] = stdout
        called['stderr'] = stderr

        class Result:
            returncode = 0

        return Result()

    monkeypatch.setattr(subprocess, 'run', fake_run)
    cmd, rc = ie_scp('user', 'host', 'local.txt', 'remote.txt')
    assert called['cmd'] == ['scp', '-q', 'local.txt', 'user@host:remote.txt']
    assert cmd == 'scp -q local.txt user@host:remote.txt'
    assert rc == 0
    assert called['stdout'] is subprocess.PIPE
    assert called['stderr'] is subprocess.PIPE


def test_ie_scp_not_quiet(monkeypatch):
    called = {}

    def fake_run(cmd, stdout=None, stderr=None):
        called['cmd'] = cmd
        called['stdout'] = stdout
        called['stderr'] = stderr

        class Result:
            returncode = 1

        return Result()

    monkeypatch.setattr(subprocess, 'run', fake_run)
    cmd, rc = ie_scp('u', 'h', 'src', 'dest', quiet=False)
    assert called['cmd'] == ['scp', 'src', 'u@h:dest']
    assert cmd == 'scp src u@h:dest'
    assert rc == 1
    assert called['stdout'] is None
    assert called['stderr'] is None
