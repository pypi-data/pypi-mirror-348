from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Trip import Trip
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.place.BoatTerminal import BoatTerminal
from typing import Optional, Union, Dict, List, Any


class BoatTrip(Trip):
    """A trip on a commercial ferry line."""
    type: str = field(default_factory=lambda: "BoatTrip", name="@type")
    departureBoatTerminal: Union[List['BoatTerminal'], 'BoatTerminal', None] = None
    arrivalBoatTerminal: Union[List['BoatTerminal'], 'BoatTerminal', None] = None