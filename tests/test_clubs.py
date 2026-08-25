from hooshek.clubs.repo import ClubsModel, load

import pytest
import pydantic


def test_valid_clubs_model():
    data = {
        "version": "1.0",
        "clubs": [
            {"id": "ABCD", "name": "Test Club 1", "abb15": "Test1", "isSokol": True},
            {"id": "EFGH", "name": "Test Club 2", "abb15": "Test2", "isSokol": False},
        ],
    }
    model = ClubsModel(**data)
    assert model.version == "1.0"
    assert len(model.clubs) == 2
    assert model.clubs[0].id == "ABCD"
    assert model.clubs[0].is_sokol is True
    assert model.clubs[1].id == "EFGH"
    assert model.clubs[1].is_sokol is False


def test_invalid_club_id_length():
    data = {
        "version": "1.0",
        "clubs": [
            {"id": "ABC", "name": "Short ID", "abb15": "Short"},
        ],
    }
    with pytest.raises(pydantic.ValidationError):
        ClubsModel(**data)


def test_invalid_club_id_pattern():
    data = {
        "version": "1.0",
        "clubs": [
            {"id": "abcd", "name": "Lowercase ID", "abb15": "Lower"},
        ],
    }
    with pytest.raises(pydantic.ValidationError):
        ClubsModel(**data)


def test_duplicate_club_ids():
    data = {
        "version": "1.0",
        "clubs": [
            {"id": "ABCD", "name": "Club 1", "abb15": "C1"},
            {"id": "ABCD", "name": "Club 2", "abb15": "C2"},
        ],
    }
    with pytest.raises(ValueError, match="defined 2 times"):
        ClubsModel(**data)


def test_abb15_max_length():
    data = {
        "version": "1.0",
        "clubs": [
            {"id": "ABCD", "name": "Club", "abb15": "A" * 16},
        ],
    }
    with pytest.raises(pydantic.ValidationError):
        ClubsModel(**data)


def test_load_repo(monkeypatch, tmp_path):
    clubs_yaml = tmp_path / "clubs.yaml"
    clubs_yaml.write_text(
        'version: "1.0"\n'
        "clubs:\n"
        "  - id: ABCD\n"
        '    name: "Sokol Abc"\n'
        '    abb15: "Sokol"\n'
        "    isSokol: true\n"
        "  - id: EFGH\n"
        '    name: "Ski club"\n'
        '    abb15: "Ski"\n'
        "    isSokol: false\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    clubs = load()
    assert isinstance(clubs, dict)
    assert len(clubs) == 2
    assert "ABCD" in clubs
    assert clubs["ABCD"].name == "Sokol Abc"
    assert clubs["ABCD"].abb15 == "Sokol"
    assert clubs["ABCD"].is_sokol is True
    assert "EFGH" in clubs
    assert clubs["EFGH"].name == "Ski club"
    assert clubs["EFGH"].abb15 == "Ski"
    assert clubs["EFGH"].is_sokol is False


def test_load_repo_validation_error(monkeypatch, tmp_path):
    clubs_yaml = tmp_path / "clubs.yaml"
    clubs_yaml.write_text(
        'version: "1.0"\n'
        "clubs:\n"
        "  - id: ABCD\n"
        '    name: "Invalid"\n'
        '    abb15: "Too long abbreviation"\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    with pytest.raises(pydantic.ValidationError):
        load()
