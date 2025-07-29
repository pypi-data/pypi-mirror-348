from typing import Literal, TypedDict


class PostSource(TypedDict):
    type: Literal["vk", "widget", "api", "res", "sms"]
    platform: Literal["android", "iphone", "wphone"]
    data: Literal[
        "profile_activity", "profile_photo", "comments", "like", "poll"
    ]
    url: str
