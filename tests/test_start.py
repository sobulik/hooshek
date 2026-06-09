import filecmp
import pytest
import subprocess
import sys

@pytest.fixture
def start_clubs_exists(dir_fixture):
    return (dir_fixture / "start-clubs.txt").is_file()

@pytest.mark.parametrize("ext", ("yaml", "txt"))
def test_start(prepare, dir_fixture, dir_script, tmp_path, ext):
    subprocess.run([sys.executable, dir_script / "start.py"], cwd=tmp_path)
    filename = "start." + ext
    assert filecmp.cmp(dir_fixture / filename, tmp_path / filename, shallow=False)

def test_clubs(start_clubs_exists, prepare, dir_fixture, dir_script, tmp_path):
    if start_clubs_exists:
        subprocess.run([sys.executable, dir_script / "start.py", "--clubs"], cwd=tmp_path)
        assert filecmp.cmp(dir_fixture / "start-clubs.txt", tmp_path / "start-clubs.txt", shallow=False)
