from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.ListItem import ListItem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class HowToItem(ListItem):
    """An item used as either a tool or supply when performing the instructions for how to achieve a result."""
    type: str = field(default_factory=lambda: "HowToItem", name="@type")
    requiredQuantity: Union[List[Union[int | float, str, 'QuantitativeValue']], Union[int | float, str, 'QuantitativeValue'], None] = None