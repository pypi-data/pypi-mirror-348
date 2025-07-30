from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Residence import Residence
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class ApartmentComplex(Residence):
    """Residence type: Apartment complex."""
    type: str = field(default_factory=lambda: "ApartmentComplex", name="@type")
    tourBookingPage: Union[List['URL'], 'URL', None] = None
    numberOfAvailableAccommodationUnits: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    numberOfAccommodationUnits: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    numberOfBedrooms: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    petsAllowed: Union[List[Union[bool, str]], Union[bool, str], None] = None