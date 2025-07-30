from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Reservation import Reservation
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.place.Place import Place
from datetime import datetime
from typing import Optional, Union, Dict, List, Any


class RentalCarReservation(Reservation):
    """A reservation for a rental car.\\n\\nNote: This type is for information about actual reservations, e.g. in confirmation emails or HTML pages with individual confirmations of reservations."""
    type: str = field(default_factory=lambda: "RentalCarReservation", name="@type")
    pickupLocation: Union[List['Place'], 'Place', None] = None
    dropoffTime: Union[List[datetime], datetime, None] = None
    dropoffLocation: Union[List['Place'], 'Place', None] = None
    pickupTime: Union[List[datetime], datetime, None] = None