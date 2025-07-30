from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.AddAction import AddAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class InsertAction(AddAction):
    """The act of adding at a specific location in an ordered collection."""
    type: str = field(default_factory=lambda: "InsertAction", name="@type")
    toLocation: Union[List['Place'], 'Place', None] = None