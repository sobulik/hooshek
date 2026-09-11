import subcommand

import filecmp
import pytest
import shutil


def test_assign_bibs(project_path, fixture_path, tmp_path):
    if not (fixture_path / "athletes-without-bibs.yaml").is_file():
        pytest.skip("No athletes-without-bibs.yaml for this fixture")
    for f in ("event.yaml", "clubs.yaml"):
        shutil.copy(fixture_path / f, tmp_path)
    shutil.copy(fixture_path / "athletes-without-bibs.yaml", tmp_path / "athletes.yaml")

    subcommand.run(["assign-bibs.py"], project_path, tmp_path)

    assert filecmp.cmp(
        fixture_path / "athletes-with-bibs.yaml",
        tmp_path / "athletes-with-bibs.yaml",
        shallow=False,
    )
