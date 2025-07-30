from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.DeliveryMethod import DeliveryMethod
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class DeliveryChargeSpecification(PriceSpecification):
    """The price for the delivery of an offer using a particular delivery method."""
    type: str = field(default_factory=lambda: "DeliveryChargeSpecification", name="@type")
    eligibleRegion: Union[List[Union[str, 'Place', 'GeoShape']], Union[str, 'Place', 'GeoShape'], None] = None
    areaServed: Union[List[Union[str, 'AdministrativeArea', 'Place', 'GeoShape']], Union[str, 'AdministrativeArea', 'Place', 'GeoShape'], None] = None
    ineligibleRegion: Union[List[Union[str, 'Place', 'GeoShape']], Union[str, 'Place', 'GeoShape'], None] = None
    appliesToDeliveryMethod: Union[List['DeliveryMethod'], 'DeliveryMethod', None] = None