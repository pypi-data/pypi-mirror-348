from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Accommodation import Accommodation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BedDetails import BedDetails
    from msgspec_schemaorg.models.intangible.BedType import BedType
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class Suite(Accommodation):
    """A suite in a hotel or other public accommodation, denotes a class of luxury accommodations, the key feature of which is multiple rooms (source: Wikipedia, the free encyclopedia, see <a href="http://en.wikipedia.org/wiki/Suite_(hotel)">http://en.wikipedia.org/wiki/Suite_(hotel)</a>).
<br /><br />
See also the <a href="/docs/hotels.html">dedicated document on the use of schema.org for marking up hotels and other forms of accommodations</a>.
"""
    type: str = field(default_factory=lambda: "Suite", name="@type")
    occupancy: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    numberOfRooms: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    bed: Union[List[Union[str, 'BedDetails', 'BedType']], Union[str, 'BedDetails', 'BedType'], None] = None