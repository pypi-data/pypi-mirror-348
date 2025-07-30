from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Accommodation import Accommodation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class Apartment(Accommodation):
    """An apartment (in American English) or flat (in British English) is a self-contained housing unit (a type of residential real estate) that occupies only part of a building (source: Wikipedia, the free encyclopedia, see <a href="http://en.wikipedia.org/wiki/Apartment">http://en.wikipedia.org/wiki/Apartment</a>)."""
    type: str = field(default_factory=lambda: "Apartment", name="@type")
    occupancy: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    numberOfRooms: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None