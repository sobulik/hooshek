import collections
import datetime
import typing

import pydantic

import hooshek.persistence.yaml
from hooshek.exceptions import ValidationError

from ..util.util import parseTime
from .event import Event, EventInterval
from .race import Race, RaceEvaluation, RaceInterval


class RaceEvaluationModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid", strict=True)
    age_min: int = pydantic.Field(ge=0)
    age_max: int = pydantic.Field(ge=0)


class RaceIntervalModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid", strict=True)
    start: str = pydantic.Field(pattern=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$")
    athlete: int = pydantic.Field(ge=1)
    groupby: int = pydantic.Field(ge=1)


class RaceModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid", strict=True)
    age_min: int = pydantic.Field(ge=0)
    age_max: int = pydantic.Field(ge=0)
    name: str
    sex: typing.Literal["f", "m"]
    distance: str
    slcr_name: str | None = None
    eval: list[RaceEvaluationModel] | None = None
    start: str | None = pydantic.Field(
        default=None, pattern=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$"
    )
    interval: RaceIntervalModel | None = None

    @pydantic.model_validator(mode="after")
    def validate_ages(self) -> "RaceModel":
        if self.age_min > self.age_max:
            raise ValueError("age_min higher than age_max for a race")
        if self.eval:
            for e in self.eval:
                if e.age_min > e.age_max:
                    raise ValueError("age_min higher than age_max for an evaluation")
                if e.age_min < self.age_min:
                    raise ValueError(
                        "age_min in evaluation lower than age_min for a race"
                    )
                if e.age_max > self.age_max:
                    raise ValueError(
                        "age_max in evaluation higher than age_max for a race"
                    )
        return self


class EventIntervalModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid", strict=True)
    start: str = pydantic.Field(pattern=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$")
    race: int = pydantic.Field(ge=1)
    athlete: int = pydantic.Field(ge=1)
    groupby: int = pydantic.Field(ge=1)


class EventModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid", strict=True)
    version: typing.Literal["1.0", "1.1"]
    name: str
    date: datetime.date
    location: str | None = None
    organizer: str | None = None
    slcr_event_id: int | None = None
    style: typing.Literal["Přespolní běh", "klasicky", "volně"] | None = None
    encoding_print: str | None = "utf-8"
    interval: EventIntervalModel | None = None
    races: list[RaceModel] = pydantic.Field(min_length=1)

    @pydantic.model_validator(mode="after")
    def check_unique_races(self) -> "EventModel":
        unique_counter = collections.Counter(
            (r.age_min, r.age_max, r.sex) for r in self.races
        )
        for key, count in unique_counter.items():
            if count > 1:
                raise ValueError(f"Event file race {key} defined {count} times")
        return self


def load() -> Event:
    """return Event instance"""
    raw = hooshek.persistence.yaml.load("event.yaml")
    try:
        validated = EventModel(**raw)
    except pydantic.ValidationError as e:
        print(e.errors())
        raise ValidationError("Event file does not validate")

    interval = None
    if validated.interval:
        interval = EventInterval(
            start=parseTime(validated.interval.start),
            race=datetime.timedelta(seconds=validated.interval.race),
            athlete=datetime.timedelta(seconds=validated.interval.athlete),
            groupby=validated.interval.groupby,
        )

    races = []
    for r in validated.races:
        evals = (
            tuple(RaceEvaluation(age_min=e.age_min, age_max=e.age_max) for e in r.eval)
            if r.eval
            else None
        )
        r_interval = (
            RaceInterval(
                athlete=datetime.timedelta(seconds=r.interval.athlete),
                groupby=r.interval.groupby,
            )
            if r.interval
            else None
        )
        races.append(
            Race(
                age_min=r.age_min,
                age_max=r.age_max,
                sex=r.sex,
                name=r.name,
                distance=r.distance,
                slcr_name=r.slcr_name if r.slcr_name is not None else r.name,
                eval=evals,
                start=parseTime(r.start) if r.start else None,
                interval=r_interval,
            )
        )

    return Event(
        version=validated.version,
        name=validated.name,
        date=validated.date,
        location=validated.location,
        organizer=validated.organizer,
        slcr_event_id=validated.slcr_event_id,
        style=validated.style,
        encoding_print=validated.encoding_print or "utf-8",
        interval=interval,
        races=tuple(races),
    )
