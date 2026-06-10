import filecmp
import pytest
import subprocess
import shutil
import sys

@pytest.fixture
def wo_numbers_exists(dir_fixture):
    return (dir_fixture / "athletes-without-numbers.yaml").is_file()

def test_numerate(wo_numbers_exists, dir_fixture, dir_script, tmp_path):
    if wo_numbers_exists:
        for f in ("event.yaml", "clubs.yaml"):
            shutil.copy(dir_fixture / f, tmp_path)
        shutil.copy(dir_fixture / "athletes-without-numbers.yaml", tmp_path / "athletes.yaml")
        subprocess.run([sys.executable, dir_script / "numerate.py"], cwd=tmp_path)
        assert filecmp.cmp(dir_fixture / "athletes-with-numbers.yaml", tmp_path / "athletes-with-numbers.yaml", shallow=False)
