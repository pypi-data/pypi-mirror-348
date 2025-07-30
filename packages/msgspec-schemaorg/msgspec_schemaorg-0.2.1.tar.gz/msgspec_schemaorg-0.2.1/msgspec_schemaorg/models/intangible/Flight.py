from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Trip import Trip
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.BoardingPolicyType import BoardingPolicyType
    from msgspec_schemaorg.models.intangible.Distance import Distance
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Airport import Airport
    from msgspec_schemaorg.models.product.Vehicle import Vehicle
from datetime import datetime
from typing import Optional, Union, Dict, List, Any


class Flight(Trip):
    """An airline flight."""
    type: str = field(default_factory=lambda: "Flight", name="@type")
    flightNumber: Union[List[str], str, None] = None
    mealService: Union[List[str], str, None] = None
    estimatedFlightDuration: Union[List[Union[str, 'Duration']], Union[str, 'Duration'], None] = None
    webCheckinTime: Union[List[datetime], datetime, None] = None
    boardingPolicy: Union[List['BoardingPolicyType'], 'BoardingPolicyType', None] = None
    carrier: Union[List['Organization'], 'Organization', None] = None
    seller: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    arrivalGate: Union[List[str], str, None] = None
    departureTerminal: Union[List[str], str, None] = None
    arrivalAirport: Union[List['Airport'], 'Airport', None] = None
    departureGate: Union[List[str], str, None] = None
    aircraft: Union[List[Union[str, 'Vehicle']], Union[str, 'Vehicle'], None] = None
    flightDistance: Union[List[Union[str, 'Distance']], Union[str, 'Distance'], None] = None
    arrivalTerminal: Union[List[str], str, None] = None
    departureAirport: Union[List['Airport'], 'Airport', None] = None