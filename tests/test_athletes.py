import filecmp
import pytest
import subprocess
import shutil
import sys

@pytest.fixture
def sorted_exists(dir_fixture):
    return (dir_fixture / "athletes-sorted.yaml").is_file()

def test_sort(sorted_exists, dir_fixture, dir_script, tmp_path):
    if sorted_exists:
        for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
            shutil.copy(dir_fixture / f, tmp_path)
        subprocess.run([sys.executable, dir_script / "athletes.py"], cwd=tmp_path)
        assert filecmp.cmp(dir_fixture / "athletes-sorted.yaml", tmp_path / "athletes-sorted.yaml", shallow=False)
