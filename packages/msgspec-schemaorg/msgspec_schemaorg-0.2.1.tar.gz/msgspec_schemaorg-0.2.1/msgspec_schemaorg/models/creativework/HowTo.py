from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.HowToSection import HowToSection
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.HowToStep import HowToStep
    from msgspec_schemaorg.models.intangible.HowToSupply import HowToSupply
    from msgspec_schemaorg.models.intangible.HowToTool import HowToTool
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class HowTo(CreativeWork):
    """Instructions that explain how to achieve a result by performing a sequence of steps."""
    type: str = field(default_factory=lambda: "HowTo", name="@type")
    totalTime: Union[List['Duration'], 'Duration', None] = None
    step: Union[List[Union[str, 'CreativeWork', 'HowToSection', 'HowToStep']], Union[str, 'CreativeWork', 'HowToSection', 'HowToStep'], None] = None
    tool: Union[List[Union[str, 'HowToTool']], Union[str, 'HowToTool'], None] = None
    performTime: Union[List['Duration'], 'Duration', None] = None
    supply: Union[List[Union[str, 'HowToSupply']], Union[str, 'HowToSupply'], None] = None
    prepTime: Union[List['Duration'], 'Duration', None] = None
    steps: Union[List[Union[str, 'ItemList', 'CreativeWork']], Union[str, 'ItemList', 'CreativeWork'], None] = None
    estimatedCost: Union[List[Union[str, 'MonetaryAmount']], Union[str, 'MonetaryAmount'], None] = None
    yield_: Union[List[Union[str, 'QuantitativeValue']], Union[str, 'QuantitativeValue'], None] = None