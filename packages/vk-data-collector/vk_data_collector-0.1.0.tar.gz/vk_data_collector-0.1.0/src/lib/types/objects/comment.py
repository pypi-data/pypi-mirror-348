from typing import Any, Optional, TypedDict

from lib.types.objects.donut import Donut


class TreadComment(TypedDict):
    id: int
    from_id: int
    date: int
    text: str
    post_id: int
    owner_id: int
    parents_stack: list[int]
    reply_to_user: Optional[int]
    reply_to_comment: Optional[int]


class Thread(TypedDict):
    count: int
    items: list[TreadComment]
    can_post: bool
    show_reply_button: bool
    groups_can_post: bool
    next_from: str


class Comment(TypedDict):
    id: int
    from_id: int
    date: int
    text: str
    donut: Optional[Donut]
    attachments: Optional[list[dict[str, Any]]]
    parents_stack: list[int]
    thread: Thread
    reply_to_user: Optional[int]
    reply_to_comment: Optional[int]
