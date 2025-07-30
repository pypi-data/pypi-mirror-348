from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.place.Country import Country
from typing import Optional, Union, Dict, List, Any


class GeoCoordinates(StructuredValue):
    """The geographic coordinates of a place or event."""
    type: str = field(default_factory=lambda: "GeoCoordinates", name="@type")
    longitude: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    address: Union[List[Union[str, 'PostalAddress']], Union[str, 'PostalAddress'], None] = None
    postalCode: Union[List[str], str, None] = None
    latitude: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    addressCountry: Union[List[Union[str, 'Country']], Union[str, 'Country'], None] = None
    elevation: Union[List[Union[int | float, str]], Union[int | float, str], None] = None