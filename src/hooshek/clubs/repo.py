from hooshek.persistence import yaml
from hooshek.clubs.club import Club

import collections
import pydantic
import typing


class ClubModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid", strict=True)

    id: str = pydantic.Field(
        pattern="^[A-Z]{4}$",
        min_length=4,
        max_length=4,
        description="Four letter club id assigned by czech-ski.com",
    )
    name: str
    abb15: str = pydantic.Field(
        max_length=15, description="Club name abbreviation to 15 chars max"
    )
    is_sokol: bool = pydantic.Field(
        default=False, alias="isSokol", description="Is club a member of sokol.eu?"
    )


class ClubsModel(pydantic.BaseModel):
    version: typing.Literal["1.0"]
    clubs: list[ClubModel]

    ## id uniqueness check
    @pydantic.model_validator(mode="after")
    def check_unique_ids(self) -> "ClubsModel":
        id_counter = collections.Counter(club.id for club in self.clubs)
        for club_id, count in id_counter.items():
            if count > 1:
                raise ValueError(f"Clubs file club id {club_id} defined {count} times")
        return self


def load() -> dict[str, Club]:
    """return a dictionary of Club instances"""
    raw = yaml.load("clubs.yaml")
    try:
        validated = ClubsModel(**raw)
        return {
            club.id: Club(club.id, club.name, club.abb15, club.is_sokol)
            for club in validated.clubs
        }
    except pydantic.ValidationError as e:
        print(e.errors())
        raise
