import hooshek.cli

import filecmp
import pytest
import shutil
import typer.testing


@pytest.mark.parametrize("ext", ("yaml", "txt"))
def test_start(fixture_path, tmp_path, monkeypatch, ext):
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
        shutil.copy(fixture_path / f, tmp_path)
    monkeypatch.chdir(tmp_path)

    runner = typer.testing.CliRunner()
    result = runner.invoke(hooshek.cli.app, ["startlist"])

    assert result.exit_code == 0
    filename = "start." + ext
    assert filecmp.cmp(fixture_path / filename, tmp_path / filename, shallow=False)


def test_clubs(fixture_path, tmp_path, monkeypatch):
    if not (fixture_path / "start-clubs.txt").is_file():
        pytest.skip("No start-clubs.txt for this fixture")
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
        shutil.copy(fixture_path / f, tmp_path)
    monkeypatch.chdir(tmp_path)

    runner = typer.testing.CliRunner()
    result = runner.invoke(hooshek.cli.app, ["startlist"])

    assert result.exit_code == 0
    assert filecmp.cmp(
        fixture_path / "start-clubs.txt", tmp_path / "start-clubs.txt", shallow=False
    )
