import filecmp
import pytest
import subprocess
import shutil
import sys

def test_sort(dir_fixture, dir_script, tmp_path):
    if not (dir_fixture / "athletes-sorted.yaml").is_file():
        pytest.skip("No athletes-sorted.yaml for this fixture")
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
        shutil.copy(dir_fixture / f, tmp_path)
    subprocess.run([sys.executable, dir_script / "athletes.py"], cwd=tmp_path, check=True)
    assert filecmp.cmp(dir_fixture / "athletes-sorted.yaml", tmp_path / "athletes-sorted.yaml", shallow=False)
