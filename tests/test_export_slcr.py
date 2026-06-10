import filecmp
import pytest
import subprocess
import shutil
import sys

@pytest.fixture
def export_slcr_exists(dir_fixture):
    return (dir_fixture / "slcr-export.json").is_file()

def test_export_slcr(export_slcr_exists, dir_fixture, dir_script, tmp_path):
    if export_slcr_exists:
        for f in ("event.yaml", "clubs.yaml", "athletes.yaml", "start.yaml", "finish.yaml"):
            shutil.copy(dir_fixture / f, tmp_path)
        subprocess.run([sys.executable, dir_script / "export_slcr.py"], cwd=tmp_path)
        assert filecmp.cmp(dir_fixture / "slcr-export.json", tmp_path / "slcr-export.json", shallow=False)
