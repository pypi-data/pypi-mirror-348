from typing import Literal, TypedDict


class Likes(TypedDict):
    can_like: Literal[0, 1]
    count: int
    user_likes: Literal[0, 1]
    can_publish: Literal[0, 1]
    repost_disabled: bool
