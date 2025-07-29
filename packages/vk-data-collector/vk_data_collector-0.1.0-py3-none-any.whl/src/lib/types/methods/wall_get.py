from typing import TypedDict

from lib.types.objects.group import Group
from lib.types.objects.post import Post
from lib.types.objects.user import User


class Response(TypedDict):
    count: int
    items: list[Post]
    # extended flag
    profiles: list[User]
    groups: list[Group]


class WallGet(TypedDict):
    """https://dev.vk.com/ru/method/wall.get"""

    response: Response
