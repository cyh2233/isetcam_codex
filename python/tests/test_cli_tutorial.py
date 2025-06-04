from isetcam.cli import main


def test_cli_tutorial_runs():
    rc = main(["tutorial", "introduction/t_introduction_to_iset"])
    assert rc == 0
