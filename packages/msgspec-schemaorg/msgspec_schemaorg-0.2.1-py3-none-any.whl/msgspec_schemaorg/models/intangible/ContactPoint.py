from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.ContactPointOption import ContactPointOption
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.OpeningHoursSpecification import OpeningHoursSpecification
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.product.Product import Product
from typing import Optional, Union, Dict, List, Any


class ContactPoint(StructuredValue):
    """A contact point&#x2014;for example, a Customer Complaints department."""
    type: str = field(default_factory=lambda: "ContactPoint", name="@type")
    serviceArea: Union[List[Union['Place', 'AdministrativeArea', 'GeoShape']], Union['Place', 'AdministrativeArea', 'GeoShape'], None] = None
    email: Union[List[str], str, None] = None
    contactType: Union[List[str], str, None] = None
    contactOption: Union[List['ContactPointOption'], 'ContactPointOption', None] = None
    telephone: Union[List[str], str, None] = None
    areaServed: Union[List[Union[str, 'AdministrativeArea', 'Place', 'GeoShape']], Union[str, 'AdministrativeArea', 'Place', 'GeoShape'], None] = None
    productSupported: Union[List[Union[str, 'Product']], Union[str, 'Product'], None] = None
    availableLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    hoursAvailable: Union[List['OpeningHoursSpecification'], 'OpeningHoursSpecification', None] = None
    faxNumber: Union[List[str], str, None] = None