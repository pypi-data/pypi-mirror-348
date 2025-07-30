from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Reservation import Reservation
from typing import Optional, Union, Dict, List, Any


class EventReservation(Reservation):
    """A reservation for an event like a concert, sporting event, or lecture.\\n\\nNote: This type is for information about actual reservations, e.g. in confirmation emails or HTML pages with individual confirmations of reservations. For offers of tickets, use [[Offer]]."""
    type: str = field(default_factory=lambda: "EventReservation", name="@type")