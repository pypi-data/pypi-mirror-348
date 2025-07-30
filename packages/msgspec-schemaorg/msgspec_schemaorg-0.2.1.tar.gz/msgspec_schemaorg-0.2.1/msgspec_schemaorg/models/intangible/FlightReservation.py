from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Reservation import Reservation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
from typing import Optional, Union, Dict, List, Any


class FlightReservation(Reservation):
    """A reservation for air travel.\\n\\nNote: This type is for information about actual reservations, e.g. in confirmation emails or HTML pages with individual confirmations of reservations. For offers of tickets, use [[Offer]]."""
    type: str = field(default_factory=lambda: "FlightReservation", name="@type")
    boardingGroup: Union[List[str], str, None] = None
    securityScreening: Union[List[str], str, None] = None
    passengerPriorityStatus: Union[List[Union[str, 'QualitativeValue']], Union[str, 'QualitativeValue'], None] = None
    passengerSequenceNumber: Union[List[str], str, None] = None