from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.UpdateAction import UpdateAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class ReplaceAction(UpdateAction):
    """The act of editing a recipient by replacing an old object with a new object."""
    type: str = field(default_factory=lambda: "ReplaceAction", name="@type")
    replacee: Union[List['Thing'], 'Thing', None] = None
    replacer: Union[List['Thing'], 'Thing', None] = None