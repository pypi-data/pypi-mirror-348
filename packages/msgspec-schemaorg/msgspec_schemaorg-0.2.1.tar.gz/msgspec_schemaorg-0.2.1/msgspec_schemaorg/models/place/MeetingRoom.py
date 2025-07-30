from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Room import Room
from typing import Optional, Union, Dict, List, Any


class MeetingRoom(Room):
    """A meeting room, conference room, or conference hall is a room provided for singular events such as business conferences and meetings (source: Wikipedia, the free encyclopedia, see <a href="http://en.wikipedia.org/wiki/Conference_hall">http://en.wikipedia.org/wiki/Conference_hall</a>).
<br /><br />
See also the <a href="/docs/hotels.html">dedicated document on the use of schema.org for marking up hotels and other forms of accommodations</a>.
"""
    type: str = field(default_factory=lambda: "MeetingRoom", name="@type")