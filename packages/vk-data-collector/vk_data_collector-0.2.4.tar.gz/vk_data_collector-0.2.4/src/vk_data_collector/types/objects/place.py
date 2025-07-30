from typing import TypedDict


class Place(TypedDict):
    id: int
    title: str
    latitude: int
    longitude: int
    created: int
    icon: str
    checkins: int
    updated: int
    type: int
    city: int
    address: str
