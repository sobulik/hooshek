import filecmp
import pytest
import subprocess
import sys

@pytest.fixture
def sorted_exists(dir_fixture):
    return (dir_fixture / "athletes-sorted.yaml").is_file()

def test_sort(sorted_exists, prepare, dir_fixture, dir_script, tmp_path):
    if sorted_exists:
        subprocess.run([sys.executable, dir_script / "athletes.py"], cwd=tmp_path)
        assert filecmp.cmp(dir_fixture / "athletes-sorted.yaml", tmp_path / "athletes-sorted.yaml", shallow=False)
