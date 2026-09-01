import subcommand

import filecmp
import pytest
import shutil


def test_sort(project_path, fixture_path, tmp_path):
    if not (fixture_path / "athletes-sorted.yaml").is_file():
        pytest.skip("No athletes-sorted.yaml for this fixture")
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
        shutil.copy(fixture_path / f, tmp_path)

    subcommand.run(["athletes.py"], project_path, tmp_path)

    assert filecmp.cmp(
        fixture_path / "athletes-sorted.yaml",
        tmp_path / "athletes-sorted.yaml",
        shallow=False,
    )
