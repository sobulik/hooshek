import hooshek.cli

import filecmp
import pytest
import shutil
import typer.testing


@pytest.mark.parametrize("ext", ("yaml", "txt"))
def test_finish(fixture_path, tmp_path, monkeypatch, ext):
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml", "start.yaml", "finish.yaml"):
        shutil.copy(fixture_path / f, tmp_path)
    monkeypatch.chdir(tmp_path)

    runner = typer.testing.CliRunner()
    result = runner.invoke(hooshek.cli.app, ["results"])

    assert result.exit_code == 0
    filename = "results." + ext
    assert filecmp.cmp(fixture_path / filename, tmp_path / filename, shallow=False)
