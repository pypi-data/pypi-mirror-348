from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.intangible.MediaSubscription import MediaSubscription
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.enums.intangible.PhysicalActivityCategory import PhysicalActivityCategory
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date, datetime, time
from typing import Optional, Union, Dict, List, Any


class ActionAccessSpecification(Intangible):
    """A set of requirements that must be fulfilled in order to perform an Action."""
    type: str = field(default_factory=lambda: "ActionAccessSpecification", name="@type")
    eligibleRegion: Union[List[Union[str, 'Place', 'GeoShape']], Union[str, 'Place', 'GeoShape'], None] = None
    requiresSubscription: Union[List[Union[bool, 'MediaSubscription']], Union[bool, 'MediaSubscription'], None] = None
    ineligibleRegion: Union[List[Union[str, 'Place', 'GeoShape']], Union[str, 'Place', 'GeoShape'], None] = None
    availabilityStarts: Union[List[Union[datetime, date, time]], Union[datetime, date, time], None] = None
    availabilityEnds: Union[List[Union[datetime, date, time]], Union[datetime, date, time], None] = None
    category: Union[List[Union['URL', str, 'Thing', 'PhysicalActivityCategory', 'CategoryCode']], Union['URL', str, 'Thing', 'PhysicalActivityCategory', 'CategoryCode'], None] = None
    expectsAcceptanceOf: Union[List['Offer'], 'Offer', None] = None