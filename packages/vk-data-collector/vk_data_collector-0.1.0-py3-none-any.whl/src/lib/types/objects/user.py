from typing import Literal, TypedDict


class User(TypedDict):
    """https://dev.vk.com/ru/reference/objects/user"""

    id: int
    first_name: str
    last_name: str
    deactivated: Literal["deleted", "banned"]
    is_closed: bool
    can_access_closed: bool
