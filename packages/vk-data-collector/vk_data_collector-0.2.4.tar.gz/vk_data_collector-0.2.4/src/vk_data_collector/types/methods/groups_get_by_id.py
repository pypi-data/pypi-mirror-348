from typing import TypedDict

from vk_data_collector.types.objects.group import Group
from vk_data_collector.types.objects.user import User


class Response(TypedDict):
    groups: list[Group]
    # extended flag
    profiles: list[User]


class GroupsGetById(TypedDict):
    """https://dev.vk.com/ru/method/groups.getById"""

    response: Response
