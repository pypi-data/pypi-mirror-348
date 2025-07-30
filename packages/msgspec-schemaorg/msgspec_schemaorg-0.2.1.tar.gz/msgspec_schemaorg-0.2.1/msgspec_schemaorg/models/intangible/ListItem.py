from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.ListItem import ListItem
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class ListItem(Intangible):
    """An list item, e.g. a step in a checklist or how-to description."""
    type: str = field(default_factory=lambda: "ListItem", name="@type")
    nextItem: Union[List['ListItem'], 'ListItem', None] = None
    position: Union[List[Union[int, str]], Union[int, str], None] = None
    item: Union[List['Thing'], 'Thing', None] = None
    previousItem: Union[List['ListItem'], 'ListItem', None] = None