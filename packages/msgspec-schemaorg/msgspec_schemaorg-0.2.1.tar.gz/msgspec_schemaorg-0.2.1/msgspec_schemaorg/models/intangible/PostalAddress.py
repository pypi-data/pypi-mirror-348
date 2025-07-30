from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.place.Country import Country
from typing import Optional, Union, Dict, List, Any


class PostalAddress(ContactPoint):
    """The mailing address."""
    type: str = field(default_factory=lambda: "PostalAddress", name="@type")
    postOfficeBoxNumber: Union[List[str], str, None] = None
    streetAddress: Union[List[str], str, None] = None
    postalCode: Union[List[str], str, None] = None
    extendedAddress: Union[List[str], str, None] = None
    addressLocality: Union[List[str], str, None] = None
    addressCountry: Union[List[Union[str, 'Country']], Union[str, 'Country'], None] = None
    addressRegion: Union[List[str], str, None] = None