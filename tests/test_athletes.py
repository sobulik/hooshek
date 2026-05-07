import filecmp
import pytest
import shutil
import subprocess
import sys

@pytest.fixture
def prepare(dir_fixture, tmp_path):
    if (dir_fixture / "athletes-sorted.yaml").is_file():
        for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
            shutil.copy(dir_fixture / f, tmp_path)
        return True
    return False

def test_sort(prepare, dir_fixture, dir_script, tmp_path):
    if prepare:
        subprocess.run([sys.executable, dir_script / "athletes.py"], cwd=tmp_path)
        assert filecmp.cmp(dir_fixture / "athletes-sorted.yaml", tmp_path / "athletes-sorted.yaml", shallow=False)
