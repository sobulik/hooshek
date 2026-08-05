import subcommand

import filecmp
import pytest
import shutil


@pytest.mark.parametrize("ext", ("yaml", "txt"))
def test_start(project_path, fixture_path, tmp_path, ext):
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
        shutil.copy(fixture_path / f, tmp_path)

    subcommand.run(["start.py"], project_path, tmp_path)

    filename = "start." + ext
    assert filecmp.cmp(fixture_path / filename, tmp_path / filename, shallow=False)


def test_clubs(project_path, fixture_path, tmp_path):
    if not (fixture_path / "start-clubs.txt").is_file():
        pytest.skip("No start-clubs.txt for this fixture")
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
        shutil.copy(fixture_path / f, tmp_path)

    subcommand.run(["start.py", "--clubs"], project_path, tmp_path)

    assert filecmp.cmp(
        fixture_path / "start-clubs.txt", tmp_path / "start-clubs.txt", shallow=False
    )
