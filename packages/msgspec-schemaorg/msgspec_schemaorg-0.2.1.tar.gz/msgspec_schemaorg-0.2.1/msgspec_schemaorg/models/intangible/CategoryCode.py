from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CategoryCodeSet import CategoryCodeSet
from typing import Optional, Union, Dict, List, Any


class CategoryCode(DefinedTerm):
    """A Category Code."""
    type: str = field(default_factory=lambda: "CategoryCode", name="@type")
    codeValue: Union[List[str], str, None] = None
    inCodeSet: Union[List[Union['URL', 'CategoryCodeSet']], Union['URL', 'CategoryCodeSet'], None] = None