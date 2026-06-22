import filecmp
import pytest
import subprocess
import shutil
import sys


@pytest.mark.parametrize("ext", ("yaml", "txt"))
def test_start(dir_fixture, dir_script, tmp_path, ext):
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
        shutil.copy(dir_fixture / f, tmp_path)
    subprocess.run([sys.executable, dir_script / "start.py"], cwd=tmp_path, check=True)
    filename = "start." + ext
    assert filecmp.cmp(dir_fixture / filename, tmp_path / filename, shallow=False)


def test_clubs(dir_fixture, dir_script, tmp_path):
    if not (dir_fixture / "start-clubs.txt").is_file():
        pytest.skip("No start-clubs.txt for this fixture")
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
        shutil.copy(dir_fixture / f, tmp_path)
    subprocess.run(
        [sys.executable, dir_script / "start.py", "--clubs"], cwd=tmp_path, check=True
    )
    assert filecmp.cmp(
        dir_fixture / "start-clubs.txt", tmp_path / "start-clubs.txt", shallow=False
    )
