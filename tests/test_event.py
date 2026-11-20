import datetime
import typing

import pydantic
import pytest

from hooshek.event.repo import (
    EventModel10,
    EventModel11,
    RaceModel,
    load,
)
from hooshek.exceptions import ValidationError


def test_valid_race_model():
    race_data: dict[str, typing.Any] = {
        "age_min": 10,
        "age_max": 12,
        "name": "Benjamini",
        "sex": "m",
        "distance": "1000m",
        "slcr_name": "Benjamini M",
    }
    race = RaceModel(**race_data)
    assert race.age_min == 10
    assert race.age_max == 12
    assert race.name == "Benjamini"
    assert race.sex == "m"
    assert race.distance == "1000m"
    assert race.slcr_name == "Benjamini M"


def test_race_invalid_ages():
    race_data: dict[str, typing.Any] = {
        "age_min": 15,
        "age_max": 10,
        "name": "Invalid",
        "sex": "m",
        "distance": "1000m",
    }
    with pytest.raises(ValidationError, match="age_min higher than age_max"):
        RaceModel(**race_data)


def test_valid_event_v10_model():
    data: dict[str, typing.Any] = {
        "version": "1.0",
        "name": "Test Event",
        "date": datetime.date(2025, 1, 1),
        "races": [
            {
                "age_min": 10,
                "age_max": 12,
                "name": "Race 1",
                "sex": "m",
                "distance": "1000m",
            }
        ],
    }
    model = EventModel10(**data)
    assert model.version == "1.0"
    assert model.name == "Test Event"
    assert model.date == datetime.date(2025, 1, 1)
    assert len(model.races) == 1


def test_valid_event_v11_model():
    data: dict[str, typing.Any] = {
        "version": "1.1",
        "name": "Test Event 1.1",
        "date": datetime.date(2025, 1, 1),
        "location": "Skuhrov",
        "organizer": "Tělocvičná jednota Sokol Skuhrov",
        "slcr_event_id": 12345,
        "style": "Přespolní běh",
        "races": [
            {
                "age_min": 10,
                "age_max": 12,
                "name": "Race 1",
                "sex": "m",
                "distance": "1000m",
            }
        ],
    }
    model = EventModel11(**data)
    assert model.version == "1.1"
    assert model.slcr_event_id == 12345
    assert model.style == "Přespolní běh"
    assert model.location == "Skuhrov"
    assert model.organizer == "Tělocvičná jednota Sokol Skuhrov"


def test_duplicate_races_validation():
    race_data: dict[str, typing.Any] = {
        "age_min": 10,
        "age_max": 12,
        "name": "Race 1",
        "sex": "m",
        "distance": "1000m",
    }
    data: dict[str, typing.Any] = {
        "version": "1.0",
        "name": "Test Event",
        "date": datetime.date(2025, 1, 1),
        "races": [race_data, race_data],
    }
    with pytest.raises(ValidationError, match="defined 2 times"):
        EventModel10(**data)


def test_load_repo(monkeypatch, tmp_path):
    event_yaml = tmp_path / "event.yaml"
    event_yaml.write_text(
        'version: "1.0"\n'
        'name: "Skuhrovská steeplechase"\n'
        "date: 2025-05-10\n"
        "races:\n"
        "  - age_min: 10\n"
        "    age_max: 12\n"
        '    name: "Žáci"\n'
        '    sex: "m"\n'
        '    distance: "1500m"\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    event = load()
    assert event.version == "1.0"
    assert event.name == "Skuhrovská steeplechase"
    assert event.date == datetime.date(2025, 5, 10)
    assert len(event.races) == 1
    assert event.races[0].name == "Žáci"
    assert event.races[0].distance == "1500m"
    assert event.mass is True


def test_load_repo_v11(monkeypatch, tmp_path):
    event_yaml = tmp_path / "event.yaml"
    event_yaml.write_text(
        'version: "1.1"\n'
        'name: "Setkání mistrů"\n'
        "date: 2025-10-15\n"
        'location: "Skuhrov"\n'
        'organizer: "Tělocvičná jednota Sokol Skuhrov"\n'
        "slcr_event_id: 9876\n"
        'style: "Přespolní běh"\n'
        "races:\n"
        "  - age_min: 18\n"
        "    age_max: 99\n"
        '    name: "Dospělí"\n'
        '    sex: "m"\n'
        '    distance: "5000m"\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    event = load()
    assert event.version == "1.1"
    assert event.name == "Setkání mistrů"
    assert event.date == datetime.date(2025, 10, 15)
    assert event.location == "Skuhrov"
    assert event.organizer == "Tělocvičná jednota Sokol Skuhrov"
    assert event.slcr_event_id == 9876
    assert event.style == "Přespolní běh"
    assert len(event.races) == 1
    assert event.races[0].name == "Dospělí"


def test_load_repo_validation_error(monkeypatch, tmp_path):
    event_yaml = tmp_path / "event.yaml"
    event_yaml.write_text(
        'version: "1.0"\nname: "Invalid Event"\ndate: 2025-05-10\nraces: []\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    with pytest.raises(pydantic.ValidationError):
        load()
