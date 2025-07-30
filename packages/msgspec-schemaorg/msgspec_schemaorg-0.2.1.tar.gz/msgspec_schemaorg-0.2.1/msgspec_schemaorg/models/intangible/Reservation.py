from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.intangible.ProgramMembership import ProgramMembership
    from msgspec_schemaorg.enums.intangible.ReservationStatusType import ReservationStatusType
    from msgspec_schemaorg.models.intangible.Ticket import Ticket
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import datetime
from typing import Optional, Union, Dict, List, Any


class Reservation(Intangible):
    """Describes a reservation for travel, dining or an event. Some reservations require tickets. \\n\\nNote: This type is for information about actual reservations, e.g. in confirmation emails or HTML pages with individual confirmations of reservations. For offers of tickets, restaurant reservations, flights, or rental cars, use [[Offer]]."""
    type: str = field(default_factory=lambda: "Reservation", name="@type")
    provider: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    totalPrice: Union[List[Union[int | float, str, 'PriceSpecification']], Union[int | float, str, 'PriceSpecification'], None] = None
    priceCurrency: Union[List[str], str, None] = None
    modifiedTime: Union[List[datetime], datetime, None] = None
    reservedTicket: Union[List['Ticket'], 'Ticket', None] = None
    bookingAgent: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    reservationStatus: Union[List['ReservationStatusType'], 'ReservationStatusType', None] = None
    underName: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    reservationFor: Union[List['Thing'], 'Thing', None] = None
    broker: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    programMembershipUsed: Union[List['ProgramMembership'], 'ProgramMembership', None] = None
    bookingTime: Union[List[datetime], datetime, None] = None
    reservationId: Union[List[str], str, None] = None