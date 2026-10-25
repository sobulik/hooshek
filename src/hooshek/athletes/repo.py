import collections
import typing

import pydantic

from ..clubs.club import Club
from ..persistence import yaml
from .athlete import Athlete


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
            x.id for x in filter(lambda x: x.id is not None, self.athletes)
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
            (x.name, x.surname, x.born) for x in self.athletes
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


def dump(athletes, filename):
    """write athletes"""
    athlete_models = []
    for athlete in athletes:
        athlete_models.append(
            AthleteModel(
                id=athlete.id,
                name=athlete.name,
                surname=athlete.surname,
                born=athlete.born,
                sex=athlete.sex,
                club=athlete.club.id if athlete.club is not None else None,
            )
        )

    try:
        validated = AthletesModel(version="1.0", athletes=athlete_models)
    except pydantic.ValidationError as e:
        print(e.errors())
        raise
    else:
        yaml.dump(validated.model_dump(exclude_none=True), filename)
