import filecmp
import pytest
import subprocess
import shutil
import sys

@pytest.mark.parametrize("ext", ("yaml", "txt"))
def test_finish(dir_fixture, dir_script, tmp_path, ext):
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml", "start.yaml", "finish.yaml"):
        shutil.copy(dir_fixture / f, tmp_path)
    subprocess.run([sys.executable, dir_script / "finish.py"], cwd=tmp_path)
    filename = "results." + ext
    assert filecmp.cmp(dir_fixture / filename, tmp_path / filename, shallow=False)
