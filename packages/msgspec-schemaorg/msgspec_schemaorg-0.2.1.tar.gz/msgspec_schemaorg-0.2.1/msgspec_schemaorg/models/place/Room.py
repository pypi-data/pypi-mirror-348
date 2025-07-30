from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Accommodation import Accommodation
from typing import Optional, Union, Dict, List, Any


class Room(Accommodation):
    """A room is a distinguishable space within a structure, usually separated from other spaces by interior walls (source: Wikipedia, the free encyclopedia, see <a href="http://en.wikipedia.org/wiki/Room">http://en.wikipedia.org/wiki/Room</a>).
<br /><br />
See also the <a href="/docs/hotels.html">dedicated document on the use of schema.org for marking up hotels and other forms of accommodations</a>.
"""
    type: str = field(default_factory=lambda: "Room", name="@type")