from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class MoveAction(Action):
    """The act of an agent relocating to a place.\\n\\nRelated actions:\\n\\n* [[TransferAction]]: Unlike TransferAction, the subject of the move is a living Person or Organization rather than an inanimate object."""
    type: str = field(default_factory=lambda: "MoveAction", name="@type")
    fromLocation: Union[List['Place'], 'Place', None] = None
    toLocation: Union[List['Place'], 'Place', None] = None