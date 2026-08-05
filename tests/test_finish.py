import subcommand

import filecmp
import pytest
import shutil


@pytest.mark.parametrize("ext", ("yaml", "txt"))
def test_finish(project_path, fixture_path, tmp_path, ext):
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml", "start.yaml", "finish.yaml"):
        shutil.copy(fixture_path / f, tmp_path)

    subcommand.run(["finish.py"], project_path, tmp_path)

    filename = "results." + ext
    assert filecmp.cmp(fixture_path / filename, tmp_path / filename, shallow=False)
