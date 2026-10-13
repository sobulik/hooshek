from ..persistence import yaml
from .athlete import Athlete
from ..clubs.club import Club

import collections
import pydantic
import typing

import cerberus


class AthleteModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid", strict=True)

    id: str | None = None
    name: str
    surname: str
    born: int = pydantic.Field(ge=1900, le=2100)
    sex: typing.Literal["f", "m"]
    club: str | None = None


class AthletesModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid", strict=True)

    version: typing.Literal["1.0"]
    athletes: list[AthleteModel]

    ## id uniqueness check
    @pydantic.model_validator(mode="after")
    def check_unique_ids(self) -> "AthletesModel":
        idCounter = collections.Counter(
            map(lambda x: x.id, filter(lambda x: x.id is not None, self.athletes))
        )
        for athlete_id, count in idCounter.items():
            if athlete_id != "0" and count > 1:
                raise ValueError(
                    f"Athletes file athlete id {athlete_id} defined {count} times"
                )
        return self

    ## unique key check
    @pydantic.model_validator(mode="after")
    def check_unique_key(self) -> "AthletesModel":
        uniqueCounter = collections.Counter(
            map(lambda x: (x.name, x.surname, x.born), self.athletes)
        )
        for athlete, count in uniqueCounter.items():
            if count > 1:
                raise ValueError(f"Athlete {athlete} defined {count} times")
        return self


def load(clubs: dict[str, Club]) -> list[Athlete]:
    """return a tuple of Athlete instances"""
    raw = yaml.load("athletes.yaml")
    try:
        validated = AthletesModel(**raw)
    except pydantic.ValidationError as e:
        print(e.errors())
        raise
    else:
        athletes = []
        for a in validated.athletes:
            athlete = a.model_dump()

            # associate club
            club = None
            if a.club is not None:
                if a.club in clubs:
                    club = clubs[a.club]
                else:
                    raise ValueError(
                        f"Club {a.club} of athlete {a.surname} not defined in clubs"
                    )
            athlete["club"] = club

            athletes.append(Athlete(**athlete))
        return athletes


def validate(raw):
    schema = {
        "version": {"type": "string", "allowed": ["1.0"]},
        "athletes": {
            "type": "list",
            "minlength": 1,
            "schema": {
                "type": "dict",
                "schema": {
                    "born": {"type": "integer", "min": 1900, "max": 2100},
                    "club": {
                        "type": "string",
                        "minlength": 4,
                        "maxlength": 4,
                        "required": False,
                    },
                    "id": {"type": "string", "required": False},
                    "name": {"type": "string"},
                    "sex": {"type": "string", "allowed": ["f", "m"]},
                    "surname": {"type": "string"},
                },
            },
        },
    }

    v = cerberus.Validator(schema, require_all=True)
    if not v.validate(raw):
        print(v.errors)
        raise Exception("Athletes file does not validate")
    return v.document


def dump(athletes, filename):
    """write athletes"""
    o = dict()
    o["version"] = "1.0"
    o["athletes"] = list()
    for athlete in athletes:
        a = dict()
        if athlete.id is not None:
            a["id"] = athlete.id
        a["name"] = athlete.name
        a["surname"] = athlete.surname
        a["born"] = athlete.born
        a["sex"] = athlete.sex
        if athlete.club is not None:
            a["club"] = athlete.club.id
        o["athletes"].append(a)

    yaml.dump(o, filename)
