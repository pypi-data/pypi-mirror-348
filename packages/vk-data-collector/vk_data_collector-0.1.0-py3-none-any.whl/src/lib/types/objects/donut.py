from typing import Any, Literal, TypedDict


class Donut(TypedDict):
    is_donut: bool
    paid_duration: int
    placeholder: dict[str, Any]
    can_publish_free_copy: bool
    edit_mode: Literal["all", "duration"]
