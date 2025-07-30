from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class UpdateAction(Action):
    """The act of managing by changing/editing the state of the object."""
    type: str = field(default_factory=lambda: "UpdateAction", name="@type")
    collection: Union[List['Thing'], 'Thing', None] = None
    targetCollection: Union[List['Thing'], 'Thing', None] = None