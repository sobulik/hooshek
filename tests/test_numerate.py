import subcommand

import filecmp
import pytest
import shutil


def test_numerate(project_path, fixture_path, tmp_path):
    if not (fixture_path / "athletes-without-numbers.yaml").is_file():
        pytest.skip("No athletes-without-numbers.yaml for this fixture")
    for f in ("event.yaml", "clubs.yaml"):
        shutil.copy(fixture_path / f, tmp_path)
    shutil.copy(
        fixture_path / "athletes-without-numbers.yaml", tmp_path / "athletes.yaml"
    )

    subcommand.run(["numerate.py"], project_path, tmp_path)

    assert filecmp.cmp(
        fixture_path / "athletes-with-numbers.yaml",
        tmp_path / "athletes-with-numbers.yaml",
        shallow=False,
    )
