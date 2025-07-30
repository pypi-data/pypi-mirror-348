from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.HowToItem import HowToItem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
from typing import Optional, Union, Dict, List, Any


class HowToSupply(HowToItem):
    """A supply consumed when performing the instructions for how to achieve a result."""
    type: str = field(default_factory=lambda: "HowToSupply", name="@type")
    estimatedCost: Union[List[Union[str, 'MonetaryAmount']], Union[str, 'MonetaryAmount'], None] = None