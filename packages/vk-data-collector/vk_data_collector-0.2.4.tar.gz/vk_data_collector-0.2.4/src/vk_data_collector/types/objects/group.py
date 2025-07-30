from typing import Literal, TypedDict


class Group(TypedDict):
    id: int
    name: str
    screen_name: str
    is_closed: Literal[0, 1, 2]
    deactivated: Literal["deleted", "banned"]
    type: Literal["group", "page", "event"]
    photo_50: str
    photo_100: str
    photo_200: str
