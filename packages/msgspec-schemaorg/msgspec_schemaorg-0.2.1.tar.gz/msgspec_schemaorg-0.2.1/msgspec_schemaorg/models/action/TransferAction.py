from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class TransferAction(Action):
    """The act of transferring/moving (abstract or concrete) animate or inanimate objects from one place to another."""
    type: str = field(default_factory=lambda: "TransferAction", name="@type")
    fromLocation: Union[List['Place'], 'Place', None] = None
    toLocation: Union[List['Place'], 'Place', None] = None