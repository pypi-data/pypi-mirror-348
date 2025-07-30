from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Reservation import Reservation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Reservation import Reservation
from typing import Optional, Union, Dict, List, Any


class ReservationPackage(Reservation):
    """A group of multiple reservations with common values for all sub-reservations."""
    type: str = field(default_factory=lambda: "ReservationPackage", name="@type")
    subReservation: Union[List['Reservation'], 'Reservation', None] = None