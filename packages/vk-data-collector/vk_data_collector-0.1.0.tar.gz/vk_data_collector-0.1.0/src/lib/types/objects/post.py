from typing import Any, Literal, TypedDict

from lib.types.objects.comments import Comments
from lib.types.objects.copyright import Copyright
from lib.types.objects.donut import Donut
from lib.types.objects.geo import Geo
from lib.types.objects.likes import Likes
from lib.types.objects.post_source import PostSource
from lib.types.objects.reposts import Reposts
from lib.types.objects.views import Views


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
