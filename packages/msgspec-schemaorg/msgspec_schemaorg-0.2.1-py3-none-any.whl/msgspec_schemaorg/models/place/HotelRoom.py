from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Room import Room
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BedDetails import BedDetails
    from msgspec_schemaorg.models.intangible.BedType import BedType
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class HotelRoom(Room):
    """A hotel room is a single room in a hotel.
<br /><br />
See also the <a href="/docs/hotels.html">dedicated document on the use of schema.org for marking up hotels and other forms of accommodations</a>.
"""
    type: str = field(default_factory=lambda: "HotelRoom", name="@type")
    occupancy: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    bed: Union[List[Union[str, 'BedDetails', 'BedType']], Union[str, 'BedDetails', 'BedType'], None] = None