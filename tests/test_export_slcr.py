import subcommand

import filecmp
import pytest
import shutil


def test_export_slcr(project_path, fixture_path, tmp_path):
    if not (fixture_path / "slcr-export.json").is_file():
        pytest.skip("No slcr-export.yaml for this fixture")
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml", "start.yaml", "finish.yaml"):
        shutil.copy(fixture_path / f, tmp_path)

    subcommand.run(["export_slcr.py"], project_path, tmp_path)

    assert filecmp.cmp(
        fixture_path / "slcr-export.json", tmp_path / "slcr-export.json", shallow=False
    )
