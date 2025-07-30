from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MenuSection import MenuSection
    from msgspec_schemaorg.models.intangible.MenuItem import MenuItem
from typing import Optional, Union, Dict, List, Any


class Menu(CreativeWork):
    """A structured representation of food or drink items available from a FoodEstablishment."""
    type: str = field(default_factory=lambda: "Menu", name="@type")
    hasMenuItem: Union[List['MenuItem'], 'MenuItem', None] = None
    hasMenuSection: Union[List['MenuSection'], 'MenuSection', None] = None