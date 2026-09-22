import hooshek.cli

import filecmp
import pytest
import shutil
import typer.testing


def test_export_slcr(fixture_path, tmp_path, monkeypatch):
    if not (fixture_path / "slcr-export.json").is_file():
        pytest.skip("No slcr-export.yaml for this fixture")
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml", "start.yaml", "finish.yaml"):
        shutil.copy(fixture_path / f, tmp_path)
    monkeypatch.chdir(tmp_path)

    runner = typer.testing.CliRunner()
    result = runner.invoke(hooshek.cli.app, ["export-slcr"])

    assert result.exit_code == 0
    assert filecmp.cmp(
        fixture_path / "slcr-export.json", tmp_path / "slcr-export.json", shallow=False
    )
