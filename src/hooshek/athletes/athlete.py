import dataclasses
import typing

from ..clubs.club import Club


@dataclasses.dataclass(frozen=True, slots=True)
class Athlete:
    """Athlete domain class"""

    id: str | None
    name: str
    surname: str
    born: int
    sex: typing.Literal["f", "m"]
    club: Club | None
    start: typing.Any = None  # fiks should this be here?
    finish: typing.Any = None  # fiks should this be here?
    time: typing.Any = None  # fiks this should not be here
    rank: int | None = None  # fiks this should not be here
    rank_sokol: int | None = None  # fiks this should not be here
