from typing import Any, Literal, TypedDict

from vk_data_collector.types.objects.comments import Comments
from vk_data_collector.types.objects.copyright import Copyright
from vk_data_collector.types.objects.donut import Donut
from vk_data_collector.types.objects.geo import Geo
from vk_data_collector.types.objects.likes import Likes
from vk_data_collector.types.objects.post_source import PostSource
from vk_data_collector.types.objects.reposts import Reposts
from vk_data_collector.types.objects.views import Views


class Post(TypedDict):
    """https://dev.vk.com/ru/reference/objects/post"""

    id: int
    owner_id: int
    from_id: int
    created_by: int
    date: int
    text: str
    reply_owner_id: int
    reply_post_id: int
    friends_only: int
    comments: Comments
    copyright: Copyright
    likes: Likes
    reposts: Reposts
    views: Views
    post_type: Literal["post", "copy", "reply", "postpone", "suggest"]
    post_source: PostSource
    attachments: list[dict[str, Any]]
    geo: Geo
    signer_id: int
    copy_history: list[dict[str, Any]]
    can_pin: Literal[0, 1]
    can_delete: Literal[0, 1]
    can_edit: Literal[0, 1]
    is_pinned: int
    marked_as_ads: Literal[0, 1]
    is_favorite: bool
    donut: Donut
    postponed_id: int
