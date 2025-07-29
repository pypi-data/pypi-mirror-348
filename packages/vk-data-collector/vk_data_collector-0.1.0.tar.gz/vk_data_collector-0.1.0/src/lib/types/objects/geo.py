from typing import TypedDict

from lib.types.objects.place import Place


class Geo(TypedDict):
    type: str
    coordinates: str
    place: Place
