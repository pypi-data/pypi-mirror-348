from typing import TypedDict

from vk_data_collector.types.objects.place import Place


class Geo(TypedDict):
    type: str
    coordinates: str
    place: Place
