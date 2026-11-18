import dataclasses
import datetime


@dataclasses.dataclass(frozen=True, slots=True)
class RaceEvaluation:
    age_min: int
    age_max: int


@dataclasses.dataclass(frozen=True, slots=True)
class RaceInterval:
    athlete: datetime.timedelta
    groupby: int


@dataclasses.dataclass(slots=True)  # fiks missing frozen
class Race:
    """Race domain class"""

    age_min: int
    age_max: int
    sex: str
    name: str
    distance: str
    slcr_name: str
    eval: tuple[RaceEvaluation, ...] | None = None
    start: datetime.time | None = None
    interval: RaceInterval | None = None
    athletes: list | None = None

    @property
    def interval_athlete(self) -> datetime.timedelta | None:
        return self.interval.athlete if self.interval else None

    @property
    def interval_groupby(self) -> int | None:
        return self.interval.groupby if self.interval else None


@dataclasses.dataclass(frozen=True, slots=True)
class EventInterval:
    start: datetime.time
    race: datetime.timedelta
    athlete: datetime.timedelta
    groupby: int


@dataclasses.dataclass(frozen=True, slots=True)
class Event:
    """Event domain class"""

    version: str
    name: str
    date: datetime.date
    races: tuple[Race, ...]
    location: str | None = None  # fiks versions did disappear?
    organizer: str | None = None
    slcr_event_id: int | None = None
    style: str | None = None
    encoding_print: str = "utf-8"  # fiks is the default ok?
    interval: EventInterval | None = None

    @property
    def eff_year(self) -> int:
        y = self.date.year
        if self.date.month < 7:
            y -= 1
        return y

    @property
    def mass(self) -> bool:
        return self.interval is None

    @property
    def start(self) -> datetime.time | None:
        return self.interval.start if self.interval else None

    @property
    def interval_race(self) -> datetime.timedelta | None:
        return self.interval.race if self.interval else None

    @property
    def interval_athlete(self) -> datetime.timedelta | None:
        return self.interval.athlete if self.interval else None

    @property
    def interval_groupby(self) -> int | None:
        return self.interval.groupby if self.interval else None
