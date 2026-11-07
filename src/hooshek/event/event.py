import dataclasses
import datetime

from .race import Race


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
    location: str | None = None
    organizer: str | None = None
    slcr_event_id: int | None = None
    style: str | None = None
    encoding_print: str = "utf-8"
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

    def toString(self):
        return "Event name: {}, date: {}, effective year: {}, start: {}, mass: {}, interval_race: {}".format(
            self.name,
            self.date,
            self.eff_year,
            self.start if self.start else "",
            self.mass,
            self.interval_race if self.interval_race else "",
        )
