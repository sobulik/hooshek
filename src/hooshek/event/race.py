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


@dataclasses.dataclass(slots=True)
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

    def toString(self):
        pass
