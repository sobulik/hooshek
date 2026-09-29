import hooshek.cli

import filecmp
import pytest
import shutil
import typer.testing


def test_assign_bibs(fixture_path, tmp_path, monkeypatch):
    if not (fixture_path / "athletes-without-bibs.yaml").is_file():
        pytest.skip("No athletes-without-bibs.yaml for this fixture")
    for f in ("event.yaml", "clubs.yaml"):
        shutil.copy(fixture_path / f, tmp_path)
    shutil.copy(fixture_path / "athletes-without-bibs.yaml", tmp_path / "athletes.yaml")
    monkeypatch.chdir(tmp_path)

    runner = typer.testing.CliRunner()
    result = runner.invoke(hooshek.cli.app, ["assign-bibs"])

    assert result.exit_code == 0
    assert filecmp.cmp(
        fixture_path / "athletes-with-bibs.yaml",
        tmp_path / "athletes-with-bibs.yaml",
        shallow=False,
    )
