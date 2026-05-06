import filecmp
import pathlib
import pytest
import shutil
import subprocess
import sys

class TestAthletes:

    events = ( \
        "2020-skuhrovska-lyze", \
        "2020-skuhrovska-steeplechase", \
        "2021-skuhrovska-steeplechase", \
        "2022-skuhrovska-lyze", \
        "2025-skuhrovska-lyze", \
        "2025-setkani-mistru" \
    )

    root = pathlib.Path(__file__).parents[1]
    resources = root / "test" / "resources"

    @pytest.mark.parametrize("event", events)
    def test_sort(self, event, tmp_path):
        source = self.resources / event
        if (source / "athletes-sorted.yaml").is_file():
            for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
                shutil.copy(source / f, tmp_path)

            subprocess.run([sys.executable, self.root / "athletes.py"], cwd=tmp_path)
            comp = filecmp.cmpfiles(source, tmp_path, ["athletes-sorted.yaml"], shallow=False)
            assert not comp[1] and not comp[2]
