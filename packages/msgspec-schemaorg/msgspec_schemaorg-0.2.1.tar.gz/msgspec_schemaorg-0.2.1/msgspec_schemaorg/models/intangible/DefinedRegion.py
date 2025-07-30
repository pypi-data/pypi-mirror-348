from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.PostalCodeRangeSpecification import PostalCodeRangeSpecification
    from msgspec_schemaorg.models.place.Country import Country
from typing import Optional, Union, Dict, List, Any


class DefinedRegion(StructuredValue):
    """A DefinedRegion is a geographic area defined by potentially arbitrary (rather than political, administrative or natural geographical) criteria. Properties are provided for defining a region by reference to sets of postal codes.

Examples: a delivery destination when shopping. Region where regional pricing is configured.

Requirement 1:
Country: US
States: "NY", "CA"

Requirement 2:
Country: US
PostalCode Set: { [94000-94585], [97000, 97999], [13000, 13599]}
{ [12345, 12345], [78945, 78945], }
Region = state, canton, prefecture, autonomous community...
"""
    type: str = field(default_factory=lambda: "DefinedRegion", name="@type")
    postalCodeRange: Union[List['PostalCodeRangeSpecification'], 'PostalCodeRangeSpecification', None] = None
    postalCode: Union[List[str], str, None] = None
    addressCountry: Union[List[Union[str, 'Country']], Union[str, 'Country'], None] = None
    addressRegion: Union[List[str], str, None] = None
    postalCodePrefix: Union[List[str], str, None] = None