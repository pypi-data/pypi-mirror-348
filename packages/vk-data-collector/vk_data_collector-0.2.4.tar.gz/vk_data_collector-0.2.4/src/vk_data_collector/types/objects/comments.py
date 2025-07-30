from typing import Literal, TypedDict


class Comments(TypedDict):
    count: int
    can_post: Literal[0, 1]
    groups_can_post: bool
    can_close: bool
    can_open: bool
