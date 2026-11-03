import filecmp
import shutil
import typing

import pydantic
import pytest
import typer.testing

import hooshek.cli
from hooshek.athletes.athlete import Athlete
from hooshek.athletes.repo import AthleteModel, AthletesModel, dump, load
from hooshek.clubs.club import Club


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


def test_valid_athlete_model():
    a1: dict[str, typing.Any] = {
        "name": "Jan",
        "surname": "Novak",
        "born": 2005,
        "sex": "m",
        "club": "ABCD",
    }
    model = AthleteModel(**a1)
    assert model.name == "Jan"
    assert model.surname == "Novak"
    assert model.born == 2005
    assert model.sex == "m"
    assert model.club == "ABCD"
    assert model.id is None


def test_invalid_born_year():
    data: dict[str, typing.Any] = {
        "name": "Jan",
        "surname": "Novak",
        "born": 1899,
        "sex": "m",
    }
    with pytest.raises(pydantic.ValidationError):
        AthleteModel(**data)


def test_invalid_sex():
    data: dict[str, typing.Any] = {
        "name": "Jan",
        "surname": "Novak",
        "born": 2005,
        "sex": "x",
    }
    with pytest.raises(pydantic.ValidationError):
        AthleteModel(**data)


def test_duplicate_athlete_ids():
    a1 = AthleteModel(id="1", name="Jan", surname="Novak", born=2005, sex="m")
    a2 = AthleteModel(id="1", name="Petr", surname="Svoboda", born=2006, sex="m")
    data = {"version": "1.0", "athletes": [a1, a2]}
    with pytest.raises(ValueError, match="defined 2 times"):
        AthletesModel(**data)


def test_duplicate_athlete_key():
    a1 = AthleteModel(name="Jan", surname="Novak", born=2005, sex="m")
    a2 = AthleteModel(name="Jan", surname="Novak", born=2005, sex="m")
    data = {"version": "1.0", "athletes": [a1, a2]}
    with pytest.raises(ValueError, match="defined 2 times"):
        AthletesModel(**data)


def test_no_surname():
    data: dict[str, typing.Any] = {"name": "Jan", "born": 2005, "sex": "m"}
    with pytest.raises(pydantic.ValidationError):
        AthleteModel(**data)


def test_invalid_field():
    data: dict[str, typing.Any] = {
        "name": "Jan",
        "surname": "Novak",
        "born": 2005,
        "sex": "m",
        "invalid_field": True,
    }
    with pytest.raises(pydantic.ValidationError):
        AthleteModel(**data)


def test_load_repo(monkeypatch, tmp_path):
    athletes_yaml = tmp_path / "athletes.yaml"
    athletes_yaml.write_text(
        'version: "1.0"\n'
        "athletes:\n"
        '  - name: "Jan"\n'
        '    surname: "Novak"\n'
        "    born: 2005\n"
        '    sex: "m"\n'
        '    club: "ABCD"\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    clubs = {"ABCD": Club(id="ABCD", name="Club 1", abb15="C1", is_sokol=False)}
    athletes = load(clubs)
    assert isinstance(athletes, list)
    assert len(athletes) == 1
    assert athletes[0].name == "Jan"
    assert athletes[0].surname == "Novak"
    assert athletes[0].born == 2005
    assert athletes[0].sex == "m"
    assert athletes[0].club is not None
    assert athletes[0].club.id == "ABCD"


def test_load_repo_validation_error(monkeypatch, tmp_path):
    athletes_yaml = tmp_path / "athletes.yaml"
    athletes_yaml.write_text(
        'version: "1.0"\n'
        "athletes:\n"
        '  - name: "Jan"\n'
        '    surname: "Novak"\n'
        "    born: 1800\n"
        '    sex: "m"\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    with pytest.raises(pydantic.ValidationError):
        load({})


def test_dump_repo(tmp_path):
    club = Club(id="ABCD", name="Club 1", abb15="C1", is_sokol=False)
    athlete = Athlete(
        id="1", name="Jan", surname="Novak", born=2005, sex="m", club=club
    )
    out_file = tmp_path / "output-athletes.yaml"
    dump([athlete], out_file)
    assert out_file.is_file()
    content = out_file.read_text(encoding="utf-8")
    assert "Jan" in content
    assert "Novak" in content
    assert "ABCD" in content


def test_dump_repo_validation_error(tmp_path):
    # Invalid born year < 1900 should fail Pydantic validation during dump
    club = Club(id="ABCD", name="Club 1", abb15="C1", is_sokol=False)
    athlete = Athlete(
        id="1", name="Jan", surname="Novak", born=1800, sex="m", club=club
    )
    out_file = tmp_path / "output-athletes.yaml"
    with pytest.raises(pydantic.ValidationError):
        dump([athlete], out_file)
