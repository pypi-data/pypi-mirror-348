from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Place import Place
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BedDetails import BedDetails
    from msgspec_schemaorg.models.intangible.BedType import BedType
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.FloorPlan import FloorPlan
    from msgspec_schemaorg.models.intangible.LocationFeatureSpecification import LocationFeatureSpecification
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class Accommodation(Place):
    """An accommodation is a place that can accommodate human beings, e.g. a hotel room, a camping pitch, or a meeting room. Many accommodations are for overnight stays, but this is not a mandatory requirement.
For more specific types of accommodations not defined in schema.org, one can use [[additionalType]] with external vocabularies.
<br /><br />
See also the <a href="/docs/hotels.html">dedicated document on the use of schema.org for marking up hotels and other forms of accommodations</a>.
"""
    type: str = field(default_factory=lambda: "Accommodation", name="@type")
    permittedUsage: Union[List[str], str, None] = None
    floorLevel: Union[List[str], str, None] = None
    yearBuilt: Union[List[int | float], int | float, None] = None
    accommodationFloorPlan: Union[List['FloorPlan'], 'FloorPlan', None] = None
    numberOfFullBathrooms: Union[List[int | float], int | float, None] = None
    occupancy: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    leaseLength: Union[List[Union['Duration', 'QuantitativeValue']], Union['Duration', 'QuantitativeValue'], None] = None
    numberOfPartialBathrooms: Union[List[int | float], int | float, None] = None
    tourBookingPage: Union[List['URL'], 'URL', None] = None
    floorSize: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    numberOfBedrooms: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    numberOfRooms: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    numberOfBathroomsTotal: Union[List[int], int, None] = None
    amenityFeature: Union[List['LocationFeatureSpecification'], 'LocationFeatureSpecification', None] = None
    petsAllowed: Union[List[Union[bool, str]], Union[bool, str], None] = None
    accommodationCategory: Union[List[str], str, None] = None
    bed: Union[List[Union[str, 'BedDetails', 'BedType']], Union[str, 'BedDetails', 'BedType'], None] = None