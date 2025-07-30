from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LocalBusiness import LocalBusiness
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.LocationFeatureSpecification import LocationFeatureSpecification
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.Rating import Rating
from datetime import datetime, time
from typing import Optional, Union, Dict, List, Any


class LodgingBusiness(LocalBusiness):
    """A lodging business, such as a motel, hotel, or inn."""
    type: str = field(default_factory=lambda: "LodgingBusiness", name="@type")
    numberOfRooms: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    availableLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    checkoutTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None
    audience: Union[List['Audience'], 'Audience', None] = None
    amenityFeature: Union[List['LocationFeatureSpecification'], 'LocationFeatureSpecification', None] = None
    petsAllowed: Union[List[Union[bool, str]], Union[bool, str], None] = None
    starRating: Union[List['Rating'], 'Rating', None] = None
    checkinTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None