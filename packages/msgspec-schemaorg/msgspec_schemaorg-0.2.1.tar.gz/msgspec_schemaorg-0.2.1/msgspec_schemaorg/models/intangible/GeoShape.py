from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.place.Country import Country
from typing import Optional, Union, Dict, List, Any


class GeoShape(StructuredValue):
    """The geographic shape of a place. A GeoShape can be described using several properties whose values are based on latitude/longitude pairs. Either whitespace or commas can be used to separate latitude and longitude; whitespace should be used when writing a list of several such points."""
    type: str = field(default_factory=lambda: "GeoShape", name="@type")
    polygon: Union[List[str], str, None] = None
    address: Union[List[Union[str, 'PostalAddress']], Union[str, 'PostalAddress'], None] = None
    postalCode: Union[List[str], str, None] = None
    box: Union[List[str], str, None] = None
    addressCountry: Union[List[Union[str, 'Country']], Union[str, 'Country'], None] = None
    line: Union[List[str], str, None] = None
    elevation: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    circle: Union[List[str], str, None] = None