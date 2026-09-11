import hooshek.cli

import filecmp
import pytest
import shutil
import typer.testing


def test_sort(fixture_path, tmp_path, monkeypatch):
    if not (fixture_path / "athletes-sorted.yaml").is_file():
        pytest.skip("No athletes-sorted.yaml for this fixture")
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
        shutil.copy(fixture_path / f, tmp_path)
    monkeypatch.chdir(tmp_path)

    runner = typer.testing.CliRunner()
    result = runner.invoke(hooshek.cli.app, ["athletes"])

    assert result.exit_code == 0
    assert filecmp.cmp(
        fixture_path / "athletes-sorted.yaml",
        tmp_path / "athletes-sorted.yaml",
        shallow=False,
    )
