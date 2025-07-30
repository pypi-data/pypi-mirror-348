from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.ItemListOrderType import ItemListOrderType
    from msgspec_schemaorg.models.intangible.ListItem import ListItem
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class ItemList(Intangible):
    """A list of items of any sort&#x2014;for example, Top 10 Movies About Weathermen, or Top 100 Party Songs. Not to be confused with HTML lists, which are often used only for formatting."""
    type: str = field(default_factory=lambda: "ItemList", name="@type")
    aggregateElement: Union[List['Thing'], 'Thing', None] = None
    itemListOrder: Union[List[Union[str, 'ItemListOrderType']], Union[str, 'ItemListOrderType'], None] = None
    numberOfItems: Union[List[int], int, None] = None
    itemListElement: Union[List[Union[str, 'ListItem', 'Thing']], Union[str, 'ListItem', 'Thing'], None] = None