from isetcam.cli import main
from isetcam.camera import camera_from_file, Camera


def test_cli_pipeline(tmp_path):
    out = tmp_path / "cam.mat"
    rc = main(["pipeline", "--scene", "grid lines", "--output", str(out)])
    assert rc == 0
    cam = camera_from_file(out)
    assert isinstance(cam, Camera)
    assert cam.sensor.volts.size > 0
    assert cam.optical_image.photons.size > 0
