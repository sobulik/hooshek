import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class Club:
    """Club domain class"""

    id: str
    name: str = ""
    abb15: str = ""
    is_sokol: bool = False
