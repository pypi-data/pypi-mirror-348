from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LocalBusiness import LocalBusiness
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Menu import Menu
    from msgspec_schemaorg.models.intangible.Rating import Rating
from typing import Optional, Union, Dict, List, Any


class FoodEstablishment(LocalBusiness):
    """A food-related business."""
    type: str = field(default_factory=lambda: "FoodEstablishment", name="@type")
    menu: Union[List[Union['URL', str, 'Menu']], Union['URL', str, 'Menu'], None] = None
    servesCuisine: Union[List[str], str, None] = None
    acceptsReservations: Union[List[Union['URL', bool, str]], Union['URL', bool, str], None] = None
    starRating: Union[List['Rating'], 'Rating', None] = None
    hasMenu: Union[List[Union['URL', str, 'Menu']], Union['URL', str, 'Menu'], None] = None