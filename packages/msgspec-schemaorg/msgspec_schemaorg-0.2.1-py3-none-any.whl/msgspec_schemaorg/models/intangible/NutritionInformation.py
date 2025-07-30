from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Energy import Energy
    from msgspec_schemaorg.models.intangible.Mass import Mass
from typing import Optional, Union, Dict, List, Any


class NutritionInformation(StructuredValue):
    """Nutritional information about the recipe."""
    type: str = field(default_factory=lambda: "NutritionInformation", name="@type")
    saturatedFatContent: Union[List['Mass'], 'Mass', None] = None
    unsaturatedFatContent: Union[List['Mass'], 'Mass', None] = None
    sodiumContent: Union[List['Mass'], 'Mass', None] = None
    fatContent: Union[List['Mass'], 'Mass', None] = None
    transFatContent: Union[List['Mass'], 'Mass', None] = None
    servingSize: Union[List[str], str, None] = None
    sugarContent: Union[List['Mass'], 'Mass', None] = None
    proteinContent: Union[List['Mass'], 'Mass', None] = None
    calories: Union[List['Energy'], 'Energy', None] = None
    carbohydrateContent: Union[List['Mass'], 'Mass', None] = None
    fiberContent: Union[List['Mass'], 'Mass', None] = None
    cholesterolContent: Union[List['Mass'], 'Mass', None] = None