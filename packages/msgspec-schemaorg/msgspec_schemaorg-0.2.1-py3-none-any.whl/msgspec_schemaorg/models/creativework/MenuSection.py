from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MenuSection import MenuSection
    from msgspec_schemaorg.models.intangible.MenuItem import MenuItem
from typing import Optional, Union, Dict, List, Any


class MenuSection(CreativeWork):
    """A sub-grouping of food or drink items in a menu. E.g. courses (such as 'Dinner', 'Breakfast', etc.), specific type of dishes (such as 'Meat', 'Vegan', 'Drinks', etc.), or some other classification made by the menu provider."""
    type: str = field(default_factory=lambda: "MenuSection", name="@type")
    hasMenuItem: Union[List['MenuItem'], 'MenuItem', None] = None
    hasMenuSection: Union[List['MenuSection'], 'MenuSection', None] = None