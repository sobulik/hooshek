import filecmp
import pytest
import subprocess
import shutil
import sys

def test_export_slcr(dir_fixture, dir_script, tmp_path):
    if not (dir_fixture / "slcr-export.json").is_file():
        pytest.skip("No slcr-export.yaml for this fixture")
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml", "start.yaml", "finish.yaml"):
        shutil.copy(dir_fixture / f, tmp_path)
    subprocess.run([sys.executable, dir_script / "export_slcr.py"], cwd=tmp_path, check=True)
    assert filecmp.cmp(dir_fixture / "slcr-export.json", tmp_path / "slcr-export.json", shallow=False)
