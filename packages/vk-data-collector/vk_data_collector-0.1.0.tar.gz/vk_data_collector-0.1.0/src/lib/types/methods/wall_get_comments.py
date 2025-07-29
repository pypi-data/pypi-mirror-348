from typing import TypedDict

from lib.types.objects.comment import Comment, TreadComment
from lib.types.objects.group import Group
from lib.types.objects.user import User


class Response(TypedDict):
    count: int
    items: list[Comment | TreadComment]
    current_level_count: int
    can_post: bool
    show_reply_button: bool
    groups_can_post: bool
    # extended flag
    profiles: list[User]
    groups: list[Group]


class WallGetComments(TypedDict):
    """https://dev.vk.com/ru/method/wall.getComments"""

    response: Response
