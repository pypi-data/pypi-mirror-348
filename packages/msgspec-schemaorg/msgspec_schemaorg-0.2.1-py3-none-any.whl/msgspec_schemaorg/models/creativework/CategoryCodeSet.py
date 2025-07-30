from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.DefinedTermSet import DefinedTermSet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
from typing import Optional, Union, Dict, List, Any


class CategoryCodeSet(DefinedTermSet):
    """A set of Category Code values."""
    type: str = field(default_factory=lambda: "CategoryCodeSet", name="@type")
    hasCategoryCode: Union[List['CategoryCode'], 'CategoryCode', None] = None