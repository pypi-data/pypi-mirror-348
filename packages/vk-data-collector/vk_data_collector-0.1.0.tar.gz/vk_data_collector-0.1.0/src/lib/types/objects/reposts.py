from typing import Literal, TypedDict


class Reposts(TypedDict):
    count: int
    user_reposted: Literal[0, 1]
