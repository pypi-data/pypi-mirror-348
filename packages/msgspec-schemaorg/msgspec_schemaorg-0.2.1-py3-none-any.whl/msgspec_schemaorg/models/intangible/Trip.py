from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.Trip import Trip
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Place import Place
from datetime import datetime, time
from typing import Optional, Union, Dict, List, Any


class Trip(Intangible):
    """A trip or journey. An itinerary of visits to one or more places."""
    type: str = field(default_factory=lambda: "Trip", name="@type")
    offers: Union[List[Union['Demand', 'Offer']], Union['Demand', 'Offer'], None] = None
    tripOrigin: Union[List['Place'], 'Place', None] = None
    provider: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    subTrip: Union[List['Trip'], 'Trip', None] = None
    departureTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None
    itinerary: Union[List[Union['ItemList', 'Place']], Union['ItemList', 'Place'], None] = None
    arrivalTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None
    partOfTrip: Union[List['Trip'], 'Trip', None] = None