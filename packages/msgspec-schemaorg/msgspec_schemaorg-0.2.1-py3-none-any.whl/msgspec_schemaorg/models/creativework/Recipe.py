from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.HowTo import HowTo
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.intangible.NutritionInformation import NutritionInformation
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.enums.intangible.RestrictedDiet import RestrictedDiet
from typing import Optional, Union, Dict, List, Any


class Recipe(HowTo):
    """A recipe. For dietary restrictions covered by the recipe, a few common restrictions are enumerated via [[suitableForDiet]]. The [[keywords]] property can also be used to add more detail."""
    type: str = field(default_factory=lambda: "Recipe", name="@type")
    recipeCuisine: Union[List[str], str, None] = None
    recipeInstructions: Union[List[Union[str, 'ItemList', 'CreativeWork']], Union[str, 'ItemList', 'CreativeWork'], None] = None
    ingredients: Union[List[str], str, None] = None
    nutrition: Union[List['NutritionInformation'], 'NutritionInformation', None] = None
    recipeIngredient: Union[List[str], str, None] = None
    recipeCategory: Union[List[str], str, None] = None
    cookingMethod: Union[List[str], str, None] = None
    recipeYield: Union[List[Union[str, 'QuantitativeValue']], Union[str, 'QuantitativeValue'], None] = None
    suitableForDiet: Union[List['RestrictedDiet'], 'RestrictedDiet', None] = None
    cookTime: Union[List['Duration'], 'Duration', None] = None