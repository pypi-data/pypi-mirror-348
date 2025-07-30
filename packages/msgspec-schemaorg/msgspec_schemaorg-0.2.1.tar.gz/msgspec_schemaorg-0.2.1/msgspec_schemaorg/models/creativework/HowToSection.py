from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
from typing import Optional, Union, Dict, List, Any


class HowToSection(CreativeWork):
    """A sub-grouping of steps in the instructions for how to achieve a result (e.g. steps for making a pie crust within a pie recipe)."""
    type: str = field(default_factory=lambda: "HowToSection", name="@type")
    steps: Union[List[Union[str, 'ItemList', 'CreativeWork']], Union[str, 'ItemList', 'CreativeWork'], None] = None