import filecmp
import pytest
import subprocess
import shutil
import sys

def test_numerate(dir_fixture, dir_script, tmp_path):
    if not (dir_fixture / "athletes-without-numbers.yaml").is_file():
        pytest.skip("No athletes-without-numbers.yaml for this fixture")
    for f in ("event.yaml", "clubs.yaml"):
        shutil.copy(dir_fixture / f, tmp_path)
    shutil.copy(dir_fixture / "athletes-without-numbers.yaml", tmp_path / "athletes.yaml")
    subprocess.run([sys.executable, dir_script / "numerate.py"], cwd=tmp_path, check=True)
    assert filecmp.cmp(dir_fixture / "athletes-with-numbers.yaml", tmp_path / "athletes-with-numbers.yaml", shallow=False)
