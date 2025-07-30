from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Accommodation import Accommodation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class House(Accommodation):
    """A house is a building or structure that has the ability to be occupied for habitation by humans or other creatures (source: Wikipedia, the free encyclopedia, see <a href="http://en.wikipedia.org/wiki/House">http://en.wikipedia.org/wiki/House</a>)."""
    type: str = field(default_factory=lambda: "House", name="@type")
    numberOfRooms: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None