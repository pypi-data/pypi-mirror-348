from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.MoveAction import MoveAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Distance import Distance
from typing import Optional, Union, Dict, List, Any


class TravelAction(MoveAction):
    """The act of traveling from a fromLocation to a destination by a specified mode of transport, optionally with participants."""
    type: str = field(default_factory=lambda: "TravelAction", name="@type")
    distance: Union[List['Distance'], 'Distance', None] = None