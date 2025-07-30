from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.CivicStructure import CivicStructure
from typing import Optional, Union, Dict, List, Any


class Campground(CivicStructure):
    """A camping site, campsite, or [[Campground]] is a place used for overnight stay in the outdoors, typically containing individual [[CampingPitch]] locations. \\n\\n
In British English a campsite is an area, usually divided into a number of pitches, where people can camp overnight using tents or camper vans or caravans; this British English use of the word is synonymous with the American English expression campground. In American English the term campsite generally means an area where an individual, family, group, or military unit can pitch a tent or park a camper; a campground may contain many campsites (source: Wikipedia, see [https://en.wikipedia.org/wiki/Campsite](https://en.wikipedia.org/wiki/Campsite)).\\n\\n

See also the dedicated [document on the use of schema.org for marking up hotels and other forms of accommodations](/docs/hotels.html).
"""
    type: str = field(default_factory=lambda: "Campground", name="@type")